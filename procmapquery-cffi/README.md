`PROCMAP_QUERY` with CFFI
===

This is an example of using [CFFI](https://cffi.readthedocs.io) to interact with the `PROCMAP_QUERY` API. See the [base `PROCMAP_QUERY` example](../procmapquery) for more details on the API itself.

APIs and ABIs
---

When working with interoperability in compiled languages, we distinguish the "API," application programming interface, and the "ABI," application binary interface. In particular, in C, the API is defined by header files that you `#include`; the ABI is then calculated in the compilation process. So, for instance, if the same compiled binary continues working with new versions of a library, then the library is ABI-compatible with the old version. If you have to recompile, but you don't need to change the code, then the new version is API-compatible with the old version. This could happen if, for instance, the size of a structure changed but all the old fields remained, or if the values of constants changed but their names did not, or if certain compiler options changed—of if you are running on an entirely new CPU architecture.

The Linux kernel aims for both ABI and API backwards compatibility. The fact that the kernel promises ABI compatibility is what allowed us to copy the value of `fcntl`/`ioctl` operations or the layout of `struct procmap_query` into our Python code without worrying too much about kernel versions; if our Python code works _on a certain platform_, it should keep working on newer versions of the kernel. Note that this does not mean any sort of promise of compatibility between platforms/architectures, though the kernel often tries for this as a convenience.

However, as we saw, this requires us to make sure we get the values and layout exactly right. For more complicated APIs, it would be better to lean on the C compiler to interpret the headers for us and figure out the right ABI. In addition, because the kernel API is shared accross architectures (whenever some functionality is indeed present on multiple architectures), working at the API level means we do not have to include architecture-specific conditionals or checks.

CFFI modes
---

CFFI supports being used in either "ABI mode" or "API mode". In ABI mode, CFFI accepts a subset of C syntax, parses it on its own, and attempts to determine what the ABI should be. This is very similar to how we used the `struct` module; the syntax is just closer to C.

In "API mode," CFFI calls an actual C compiler to determine the ABI. This has the advantage of letting us be very confident about the ABI. In particular, you can use `#include` to get the C headers just as a C user would see them, avoiding the risk of getting a definition wrong. Also, in API mode, [CFFI lets you write in `...` in place of certain types and values](https://cffi.readthedocs.io/en/stable/cdef.html#letting-the-c-compiler-fill-the-gaps), such as the exact value of the `ioctl`. We will still need to write out the names of the structure fields, as we did in the pure-Python version, but it will figure out the sizes and layout of those fields.

CFFI can also be used in "in-line" or "out-of-line" mode. In in-line mode, CFFI does the work of binding to the C interface every time you run your program. In out-of-line mode, you write a separate Python file that invokes CFFI, which generates a compiled Python module.

We want to use API mode, and CFFI recommends out-of-line mode for API usage; in-line API mode is deprecated. Out-of-line mode is advantageous for API mode anyway, in that it means CFFI is not running a C compiler every time you import the module. You can compile the module on your system (or in CI) and distribute a wheel to your users, who do not need a C compiler to be installed.

Using out-of-line API mode
---

We need to write a little bit of Python code to get CFFI to generate the compiled module, and make sure that code runs before using the library. While I used [uv](https://astral.sh/uv/) to create and manage this example project, nothing in this code assumes uv, and you should be able to use any other Python project manager you like to run the code here.

For this example, I used `uv init --package procmapquery_cffi` to create a project, which defaults to using the [Hatchling](https://hatch.pypa.io/latest/config/build/) build backend. Hatchling supports build hooks for doing operations like compiling code as part of the build. While there isn't a [premade build hook](https://hatch.pypa.io/latest/plugins/build-hook/reference/) for CFFI, the [built-in `custom` build hook](https://hatch.pypa.io/latest/plugins/build-hook/custom/) lets us write Python code, which is exactly what we need to use CFFI.

(If you're setting up CFFI on your own, there are other approaches; CFFI's own documentation covers how to use it with the venerable setuptools build backend, and you can also manually run the Python code to invoke CFFI and not use a build system or project manager at all.)

To the `pyproject.toml` file that `uv init --package` created, we add

```toml
dependencies = ["cffi"]

[build-system]
requires = ["hatchling", "cffi", "setuptools"]

[tool.hatch.build.hooks.custom]
```

The `cffi` Python package is both a build-time and runtime dependency, because the generated code does an `import _cffi_backend`, which lives in the `cffi` package, as noted in [CFFI's docs on distributing modules](https://cffi.readthedocs.io/en/stable/cdef.html). Also, CFFI uses setuptools internally when generating the module, so while we aren't using setuptools ourselves, we do need to list it as a requirement. Finally, we need to tell Hatchling to activate the `custom` build hook, though we don't need to configure it. The only setting is the filename for our build hook code; the default `hatch_build.py` is fine.

In [`hatch_build.py`](hatch_build.py), if we are asked to build code, we create a CFFI builder object. We use `set_source()` to pass actual C source that provides context to the compiler; for us, this is just the Linux-provided header file, though we could write extra C code here, such as wrapper functions, if we needed to. Then we use `cdef()` to define the things we want to see in Python, using `...` to let CFFI work its magic to fill in the right values. (We could have left the intehger constants for the enum in place and CFFI would have checked them, too.) Note the syntax `...;` in a struct means that there might be more fields in the struct, and CFFI should consider this okay; this lets us handle API compatibility on our end.

We then instruct CFFI to compile the extension into the right directory (why this argument is called `tmpdir` I do not know). While `compile()` throws an exception if it fails, I find the stack trace very noisy, so I chose to print the error message alone on failure. Finally, we need to tell Hatch that the wheel it is building is platform-specific.

[`src/procmapquery_cffi/__init__.py`](src/procmapquery_cffi/__init__.py) contains our actual code, using the `_procmapquery` helper module that CFFI built. There are two objects in that module, `lib`, which has the items (constants, variables, functions) we wanted to bind, and `ffi`, which has some standard CFFI-provided functions for working with our data types. Note that there is still a little bit of syntactic overhead corresponding to `pack`/`unpack`, both for the structure itself and for the buffer. If we were also using CFFI to bind the `ioctl` C function ourselves, we could just pass the CFFI pointer object directly, and CFFI would know what to do. But because we are using Python's existing `fcntl.ioctl` wrapper, we need to convert CFFI's wrapper type to `bytes`.

You can run the main program with e.g. `uv run procmapquery-cffi`. Note the presence of our CFFI-built module in the output!

System requirements
---

As a reminder, you will need a working C compiler on the machine where you build the module. On Debian/Ubuntu, `sudo apt install build-essential` is a good starting point.

You will also need the Python development headers in order to compile an extension, or you will see errors about `pyconfig.h` or `Python.h` missing. If you're using an OS-provided version of Python, this may be in a separate OS package like `python3-dev`. Alternatively, you can force uv to install its own Python version with e.g. `uv --managed-python run procmapquery-cffi`.
