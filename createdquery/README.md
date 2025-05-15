`F_CREATED_QUERY`
===

When you open a file for writing, it is created if it does not exist. The `F_CREATED_QUERY` `fcntl` operation determines whether it was in fact created, or an existing file was opened for writing.

* LWN article: "[The 6.12 merge window begins](https://lwn.net/Articles/990750/)"
* Git commit: 820a185896b77814 [`fcntl: add F_CREATED_QUERY`](torvalds/linux@820a185896b77814)
* Linux manual page on [`fcntl()`](https://man7.org/linux/man-pages/man2/fcntl.2.html) (also `man 2 fcntl`)
* Python docs on the [`fcntl`](https://docs.python.org/3/library/fcntl.html) module

This API is easy to test at a Python interactive session, a notebook, etc.:

```pycon
>>> F_CREATED_QUERY = 1028
>>> import fcntl
>>> a = open("foo.txt", "w")
>>> fcntl.fcntl(a, F_CREATED_QUERY)
1
>>> a.close()
>>> b = open("foo.txt", "w")
>>> fcntl.fcntl(b, F_CREATED_QUERY)
0
```

See [`createdquery.py`](createdquery.py) for a very small library wrapping this function, and [`createdquery_test.py`](createdquery_test.py) for a test case, which you can run with `python3 -m unittest createdquery_test.py`.
