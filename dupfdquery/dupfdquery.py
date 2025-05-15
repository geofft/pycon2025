import fcntl
import sys


F_DUPFD_QUERY = 1027

# All fcntl operations take a file descriptor, so fcntl.fcntl()
# automatically calls fileno() on its first argument. However, the types
# and meanings of the other arguments vary between calls, so there is no
# automatic processing for files. We need to call fileno() ourselves on
# the other argument ourselves.
if fcntl.fcntl(sys.stdout, F_DUPFD_QUERY, sys.stderr.fileno()):
    print("This is the same as stderr")
else:
    print("This is not the same as stderr")
