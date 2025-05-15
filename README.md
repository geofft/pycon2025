What's New in the Linux Kernel... from Python
===

This is the companion repo for [my 2025 PyCon talk](https://us.pycon.org/2025/schedule/presentation/12/), with all the code examples from the slides as well as pointers to more info.

System requirements
---

As the subject of this talk is how to use _new features_ in the Linux kernel, you will need to be running a relatively recent Linux kernel. You can check your kernel version with the command `uname -r` (or `uname -a` for more details).

The live talk discussed two features: `F_CREATED_QUERY`, which was added in Linux 6.12, released in November 2024, and `PROCMAP_QUERY`, which was added in Linux 6.11, released in September 2024. In this repo is also an example of `PIDFD_GET_INFO`, which was added in Linux 6.13, released January 2025.

Some OSes that have new enough kernel versions are Ubuntu 25.04 "Plucky Penguin," all currently supported versions of Fedora, and all currently supported versions of Arch, all of which have kernel 6.13 or newer. Debian 12 "bookworm" has kernel 6.12 available in [backports](https://backports.debian.org/).

Because these are _kernel_ features, it is not enough to run a _container_, which gets you the userspace files of another OS image on your existing kernel. You also must be running Linux, not another OS like macOS. (WSL 2 does use an actual Linux kernel, but the current version seems to be 6.6. iSH does some very cool stuff to emulate a Linux kernel, but it is not actually Linux.) You can, however, use a _virtual machine_, which runs its own kernel. All the examples in here were tested on the Ubuntu 25.04 desktop live CD.

None of the Python language features are particularly new, so any Python version you have should work—but I do wholeheartedly recommend [uv](https://docs.astral.sh/uv/), which will install and manage its own copy of a recent Python version for you and keep your project's dependencies separate from system dependencies. All the examples in this repo are designed to work with uv.

Examples
---

* [createdquery](createdquery): the `F_CREATED_QUERY` example from the talk
* [dupfdquery](dupfdquery): a similar example of `F_DUPFD_QUERY`, cut for time
* [procmapquery](procmapquery): the `PROCMAP_QUERY` example from the talk (using `struct`)
* [procmapquery-cffi](procmapquery-cffi): an alternative approach to `PROCMAP_QUERY`, using CFFI

Further reading
---

[Talk slides with presenter notes](https://ldpreload.com/p/pycon-2025-whats-new-in-the-linux-kernel.pdf) are available on my website. I will also link the video as soon as it's posted.

In my talk I recommended the following code search options:

* [GitHub search](https://github.com/search) (also available at the top of this page if you're reading on GitHub), which requires you to be logged in
* [Sourcegraph public code search](https://sourcegraph.com/search), which attempts to index a bit more than just GitHub, and supports some more advanced search syntax
* [Debian code search](http://codesearch.debian.org), which searches everything packaged in the Debian OS, even if the source isn't in Git
* [`git grep`](https://git-scm.com/docs/git-grep)

Try them out - the only way to get good at it is practice!

I also recommended the following resources for learning what's going on in the Linux kernel:

* [LWN](https://lwn.net), which has [summaries of the "merge windows" for upcoming kernel releases](https://lwn.net/Kernel/Index/#Releases), as well as a lot of coverage of major features, ongoing discussions, and things besides the Linux kernel itself. I am very happy to support them by subscribing, but all their paywalled content is free after a week.
* [KernelNewbies](https://kernelnewbies.org) is a website / community aiming to help people who are new to contributing to the Linux kernel. They publish [detailed changelogs of each kernel release](https://kernelnewbies.org/LinuxVersions) with info on basically every change, linking to LWN articles or other blog posts if they exist, or just to the commit message at worst.

Finally, depending on your needs, you might want to investigate the following approaches:

* There is much more of the [ctypes](https://docs.python.org/3/library/ctypes.html) module than what was used in this talk. It is very commonly used for binding to other C libraries; you may also find it useful for binding to the C standard library's own wrappers of system calls, though new system calls are rare.
* [Cython](https://cython.org/) lets you write in a Python-like language with some extensions for talking about C types.
* If you need full control, there is always the [C API to Python](https://docs.python.org/3/c-api/index.html), which lets you write Python modules in C. This is how standard library modules like `fcntl` are themselves written.
* If you need full control but do not want to write C, a compelling option is using [PyO3](https://pyo3.rs), which lets you write Python modules in Rust, plus tools like [bindgen](https://rust-lang.github.io/rust-bindgen/) to make C functions and data types available in Python.

Contact and copyright
---

If you have any questions about this material, feel free to open an issue in this repo and I will try to reply soon.

To the extent possible under law, I waive all copyright and related or neighboring rights to all source code in this repo (that is, all inline Python snippets in Markdown files and all non-Markdown files) under the terms of [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/). All other content in this repo, as well as the slides and presentation itself, are &copy; 2025 Geoffrey Thomas and licensed under [CC BY-SA 4.0](http://creativecommons.org/licenses/by-sa/4.0/).  This work is published from the United States.

Enjoy!
