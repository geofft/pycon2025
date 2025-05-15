from typing import Any
import sys

from cffi import FFI
from hatchling.builders.hooks.plugin.interface import BuildHookInterface


class CustomBuildHook(BuildHookInterface):
    def initialize(self, version: str, build_data: dict[str, Any]) -> None:
        if self.target_name == "sdist":
            return

        ffibuilder = FFI()
        ffibuilder.set_source("_procmapquery", """
            #include <linux/fs.h>
        """)
        ffibuilder.cdef("""
            #define PROCMAP_QUERY ...

            enum procmap_query_flags {
                PROCMAP_QUERY_VMA_READABLE = ...,
                PROCMAP_QUERY_VMA_WRITABLE = ...,
                PROCMAP_QUERY_VMA_EXECUTABLE = ...,
                PROCMAP_QUERY_VMA_SHARED = ...,
                PROCMAP_QUERY_COVERING_OR_NEXT_VMA = ...,
                PROCMAP_QUERY_FILE_BACKED_VMA = ...,
            };

            typedef int... __u32;
            typedef int... __u64;

            struct procmap_query {
                    __u64 size;
                    __u64 query_flags;
                    __u64 query_addr;
                    __u64 vma_start;
                    __u64 vma_end;
                    __u64 vma_flags;
                    __u64 vma_page_size;
                    __u64 vma_offset;
                    __u64 inode;
                    __u32 dev_major;
                    __u32 dev_minor;
                    __u32 vma_name_size;
                    __u32 build_id_size;
                    __u64 vma_name_addr;
                    __u64 build_id_addr;
                    ...;
            };
        """)

        try:
            ffibuilder.compile(verbose=True, tmpdir="src/procmapquery_cffi")
        except Exception as e:
            sys.exit(e)

        build_data["infer_tag"] = True
        build_data["pure_python"] = False
