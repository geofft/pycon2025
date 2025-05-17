import ctypes
import dataclasses
import fcntl
import os
import struct


# Definitions in this file are from <linux/fs.h>.

# #define PROCMAP_QUERY  _IOWR(PROCFS_IOCTL_MAGIC, 17, struct procmap_query)
# Expanded to an integer by hand; this value is the one in v6.11 and is still
# valid as of v6.14. The value is potentially architecture-specific, but
# this is the right value on x86_64 and aarch64, at least.
PROCMAP_QUERY = 3228067345


# struct procmap_query
@dataclasses.dataclass
class ProcmapQuery:
    _STRUCT = struct.Struct("@9L4I2L")

    size: int = _STRUCT.size
    query_flags: int = 0
    query_addr: int = 0
    vma_start: int = 0
    vma_end: int = 0
    vma_flags: int = 0
    vma_page_size: int = 0
    vma_offset: int = 0
    inode: int = 0
    dev_major: int = 0
    dev_minor: int = 0
    vma_name_size: int = 0
    build_id_size: int = 0
    vma_name_addr: int = 0
    build_id_addr: int = 0

    def pack(self) -> bytes:
        return self._STRUCT.pack(*dataclasses.astuple(self))

    @classmethod
    def unpack(cls, packed: bytes) -> "Self":
        return cls(*cls._STRUCT.unpack(packed))

    def ioctl(self, fd: int) -> "Self":
        return self.unpack(fcntl.ioctl(fd, PROCMAP_QUERY, self.pack()))
        

# enum procmap_query_flags
PROCMAP_QUERY_VMA_READABLE		= 0x01
PROCMAP_QUERY_VMA_WRITABLE		= 0x02
PROCMAP_QUERY_VMA_EXECUTABLE		= 0x04
PROCMAP_QUERY_VMA_SHARED		= 0x08
PROCMAP_QUERY_COVERING_OR_NEXT_VMA	= 0x10
PROCMAP_QUERY_FILE_BACKED_VMA		= 0x20


def get_libraries(proc_maps):
    libraries = set()
    buf = ctypes.create_string_buffer(1024)
    query = ProcmapQuery(
        query_flags=PROCMAP_QUERY_COVERING_OR_NEXT_VMA | PROCMAP_QUERY_FILE_BACKED_VMA,
        query_addr=0,
        vma_name_addr=ctypes.addressof(buf),
        vma_name_size=1024,
    )
    while True:
        try:
            response = query.ioctl(proc_maps)
        except FileNotFoundError:
            break
        libraries.add(os.fsdecode(buf[:response.vma_name_size]))
        query.query_addr = response.vma_end
    return libraries


if __name__ == "__main__":
    for library in get_libraries(open("/proc/self/maps")):
        print(library)
