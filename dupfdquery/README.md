`F_DUPFD_QUERY`
===

File descriptors can be duplicated with the [`dup`(2)](https://man7.org/linux/man-pages/man2/dup.2.html) system call. In particular, an application that runs in a terminal typically runs with the same open file for the terminal as standard input, output, and error, all duplicates of each other, unless you redirect I/O. If you use redirection syntax like `2>&1`, this also duplicates file descriptors.

The `F_DUPFD_QUERY` `fcntl` operation determines whether one file descriptor is a duplicate of another.

When you open a file for writing, it is created if it does not exist. The `F_CREATED_QUERY` `fcntl` operation determines whether it was in fact created, or an existing file was opened for writing.

* LWN article: "[The first half of the 6.10 merge window](https://lwn.net/Articles/973687/)"
* Git commit: c62b758bae6af16f [`fcntl: add F_DUPFD_QUERY fcntl()`](torvalds/linux@c62b758bae6af16f)
* Linux manual page on [`fcntl()`](https://man7.org/linux/man-pages/man2/fcntl.2.html) (also `man 2 fcntl`)
* Python docs on the [`fcntl`](https://docs.python.org/3/library/fcntl.html) module

The file [`dupfdquery.py`](dupfdquery.py) prints, to standard output, whether standard output is a duplicate of standard error.

```sh-session
$ python3 dupfdquery.py 
This is the same as stderr
$ python3 dupfdquery.py > stdout.txt
$ cat stdout.txt
This is not the same as stderr
$ python3 dupfdquery.py 2> stderr.txt
This is not the same as stderr
$ python3 dupfdquery.py > stdout.txt 2>&1
$ cat stdout.txt
This is the same as stderr
$ python3 dupfdquery.py > stdout.txt 2> stdout.txt
$ cat stdout.txt
This is not the same as stderr
```

(Note that `> stdout.txt 2> stdout.txt` opens `stdout.txt` twice, as opposed to opening it once and duplicating it. The distinction is significant if you write to _both_ standard output and standard error; each open file will independently keep track of its location in the file, meaning that writes will overwrite each other! Try it out and see what happens.)
