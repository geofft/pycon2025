`PROCMAP_QUERY`
===

The `/proc/*/maps` files list the virtual memory areas (VMAs) of a process and what, if anything, they are mapped to. A process typically has its own program executable and the libraries it needs mapped in, as well as VMAs for storing data, including the stack and the heap. If you read this file in the ordinary way, you get a sequential list of all VMAs in a text format.

* Linux manual page on [`/proc/`_pid_`/maps`](https://man7.org/linux/man-pages/man5/proc_pid_maps.5.html) (also `man 5 proc_pid_maps`)
* Kernel documentation on [the /proc filesystem](https://docs.kernel.org/filesystems/proc.html)

The `PROCMAP_QUERY` `ioctl` operation, added in kernel 6.11, lets you query for a specific VMA in various ways and get the response back as structured data.

* LWN article: "[The rest of the 6.11 merge window](https://lwn.net/Articles/982605/)"
* Git commit: ed5d583a88a9207b [`fs/procfs: implement efficient VMA querying API for /proc/<pid>/maps`](torvalds/linux@ed5d583a88a9207b) (see also the other two commits mentioned in the LWN article)
* API comments: see [`include/uapi/linux/fs.h` from kernel 6.11, starting at line 401](https://github.com/torvalds/linux/blob/v6.11/include/uapi/linux/fs.h#L401) (also likely on your system at `/usr/include/linux/fs.h`)
* Python docs on the [`fcntl`](https://docs.python.org/3/library/fcntl.html) module, including the `ioctl` operation

The file [`procmapquery.py`](procmapquery.py) implements a `get_libraries()` function that takes an open `/proc/*/maps` file and returns a set of mapped files. There is a brief `main` block, so you can run it with `python3 procmapquery.py`.
