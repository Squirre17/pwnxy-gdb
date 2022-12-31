from enum import Enum
from typing import (Any, ByteString, Callable, Dict, Generator, Iterable,
                    Iterator, List, NoReturn, Optional, Sequence, Set, Tuple, Type,
                    Union, NewType)
import pwnxy.file
import pwnxy.memory
from pwnxy.cmds import (Cmd, register)
from pwnxy.utils.debugger import (unwrap, assert_eq, assert_ne, todo)
from pwnxy.utils.output import (xy_print, info, err, note, dbg)
from pwnxy.utils.color import Color
from pwnxy.memory import Page
import gdb
'''GDB API
Programs which are being run under GDB are called inferiors
Python scripts can access information about and manipulate inferiors controlled by GDB via objects of the gdb.Inferior class.
'''

# NOTE: vmmap must be executed after program run
def vmmap():

    # TODO: considering to creat another pid class to get pid
    # TODO: add legend refer pwndbg

    pid = gdb.selected_inferior().pid
    if pid == 0:
        ...
        # TODO: rt err : program not running, errmsg refer other full-fledged gdb-plugin
    if pid is None:
        err("gdb.selected_inferior().pid")
    vmmap_path = '/proc/%s/maps' % pid
    dbg(f"pid is {int(pid)}")

    data : ByteString = unwrap(pwnxy.file.get(vmmap_path))
    # if data_tmp is None:
    #     err("file.get(vmmap_path) failed")
    # data : ByteString = data_tmp

    lines = [line for line in data.decode().split('\n') if line != '' ]

    cat_vmmap_example = '''
    [XYPRINT] : '00400000-00401000 r--p 00000000 08:20 102905                             /home/squ/prac/a.out'
    [XYPRINT] : '00401000-00402000 r-xp 00001000 08:20 102905                             /home/squ/prac/a.out'
    [XYPRINT] : '00402000-00403000 r--p 00002000 08:20 102905                             /home/squ/prac/a.out'
    [XYPRINT] : '00403000-00404000 r--p 00002000 08:20 102905                             /home/squ/prac/a.out'
    [XYPRINT] : '00404000-00405000 rw-p 00003000 08:20 102905                             /home/squ/prac/a.out'
    [XYPRINT] : '7ffff7dc1000-7ffff7de3000 r--p 00000000 08:20 33557850                   /usr/lib/x86_64-linux-gnu/libc-2.31.so'
    [XYPRINT] : '7ffff7de3000-7ffff7f5b000 r-xp 00022000 08:20 33557850                   /usr/lib/x86_64-linux-gnu/libc-2.31.so'
    [XYPRINT] : '7ffff7f5b000-7ffff7fa9000 r--p 0019a000 08:20 33557850                   /usr/lib/x86_64-linux-gnu/libc-2.31.so'
    [XYPRINT] : '7ffff7fa9000-7ffff7fad000 r--p 001e7000 08:20 33557850                   /usr/lib/x86_64-linux-gnu/libc-2.31.so'
    [XYPRINT] : '7ffff7fad000-7ffff7faf000 rw-p 001eb000 08:20 33557850                   /usr/lib/x86_64-linux-gnu/libc-2.31.so'
    [XYPRINT] : '7ffff7faf000-7ffff7fb5000 rw-p 00000000 00:00 0 '
    [XYPRINT] : '7ffff7fca000-7ffff7fce000 r--p 00000000 00:00 0                          [vvar]'
    [XYPRINT] : '7ffff7fce000-7ffff7fcf000 r-xp 00000000 00:00 0                          [vdso]'
    [XYPRINT] : '7ffff7fcf000-7ffff7fd0000 r--p 00000000 08:20 33557842                   /usr/lib/x86_64-linux-gnu/ld-2.31.so'
    [XYPRINT] : '7ffff7fd0000-7ffff7ff3000 r-xp 00001000 08:20 33557842                   /usr/lib/x86_64-linux-gnu/ld-2.31.so'
    [XYPRINT] : '7ffff7ff3000-7ffff7ffb000 r--p 00024000 08:20 33557842                   /usr/lib/x86_64-linux-gnu/ld-2.31.so'
    [XYPRINT] : '7ffff7ffc000-7ffff7ffd000 r--p 0002c000 08:20 33557842                   /usr/lib/x86_64-linux-gnu/ld-2.31.so'
    [XYPRINT] : '7ffff7ffd000-7ffff7ffe000 rw-p 0002d000 08:20 33557842                   /usr/lib/x86_64-linux-gnu/ld-2.31.so'
    [XYPRINT] : '7ffff7ffe000-7ffff7fff000 rw-p 00000000 00:00 0 '
    [XYPRINT] : '7ffffffdd000-7ffffffff000 rw-p 00000000 00:00 0                          [stack]'
    '''

    headers = ["Start", "End", "Offset", "Perm", "Path"]
    xy_print(
        Color.blueify(
            "{:<{w}s}{:<{w}s}{:<{w}s}{:<4s} {:s}"
                        .format(*headers, w = 19)
        ))
    for ln in lines:
        # TODO: understand dev and inode 
        # dev => master:slave dev number
        # inode => TODO:
        # NOTE: can have some lines missing path
        maps, perm, offset, dev, inode_path = ln.split(None ,4)
        inode_path = inode_path.split()
        if len(inode_path) == 1:
            path = ''
            inode = inode_path[0]
        else:
            inode, path = inode_path[0], inode_path[1]

        flag : int = 0
        if 'r' in perm : flag |= 4
        if 'w' in perm : flag |= 2
        if 'x' in perm : flag |= 1

        start, end = maps.split('-')
        start  = int(start, 16)
        end    = int(end, 16)
        offset = int(offset, 16)
        page : Type["Page"] = pwnxy.memory.Page(start, end, flag, offset, path)
        
        xy_print(page)

    '''
    ideal output like gef :

    Start              End                Offset             Perm Path
    0x0000000000400000 0x0000000000401000 0x0000000000000000 r-- /home/squ/prac/a.out
    '''

    # TODO: colorify it

@register
class VmmapCmd(Cmd):
    cmdname = "vmmap"
    
    def __init__(self) :
        super().__init__(self.cmdname)
    # TODO: what's args
    def do_invoke(self, args : List[str]) -> None:
        argc = len(args)
        # TODO:
        vmmap()
    # After registered to gdb, type 'cmd' will invoke this function
    def invoke(self, args : List[str], from_tty : bool = False) -> None :
        self.do_invoke(args)

    ...
    # TODO:
    
