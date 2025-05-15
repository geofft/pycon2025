import fcntl
import os

from ._procmapquery import ffi, lib


def get_libraries(proc_maps):
    libraries = set()
    buf = ffi.new("char[]", 1024)
    query = ffi.new("struct procmap_query *", dict(
        size=ffi.sizeof("struct procmap_query"),
        query_flags=lib.PROCMAP_QUERY_COVERING_OR_NEXT_VMA | lib.PROCMAP_QUERY_FILE_BACKED_VMA,
        query_addr=0,
        vma_name_addr=ffi.cast("__u64", buf),
        vma_name_size=1024,
    ))
    while True:
        try:
            response = ffi.from_buffer("struct procmap_query *", fcntl.ioctl(proc_maps, lib.PROCMAP_QUERY, bytes(ffi.buffer(query))))
        except FileNotFoundError:
            break
        libraries.add(os.fsdecode(ffi.unpack(buf, response.vma_name_size)))
        query.query_addr = response.vma_end
    return libraries


def main():
    for library in get_libraries(open("/proc/self/maps")):
        print(library)
