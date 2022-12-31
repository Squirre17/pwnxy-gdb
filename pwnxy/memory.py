'''
memory peek poke operations, 
'''
import traceback
import pwnxy.memory

from typing import (List, Optional, Union)


from pwnxy.utils.debugger import (unwrap, assert_eq, assert_ne, todo)
from pwnxy.utils.output import (err_print_exc, xy_print, info, err, note, dbg)
from pwnxy.utils.color import Color

import gdb
import traceback

def read(addr : int, size : int) -> bytearray :
    assert size > 0 and size <= 8, "size error"
    try :
        val : memoryview = gdb.selected_inferior().read_memory(addr, size)
    except Exception as e :
        err(f"TODO {e}")
        traceback.print_exc()
    return bytearray(val)

# TODO: gdbtype became a enum
'''GDB API
    Value.cast (type): hat is the result of casting this instance to the type ,type must be a `gdb.Type` object. 
    Value.dereference(): get content of given addr
'''
def read_by_type(addr, gdb_type) -> int:
    value = gdb.Value(addr)
    try:
        value = value.cast(gdb_type)
    except gdb.error as e:
        err_print_exc(e)

    return int(value.dereference())

def write(addr : int, size : int, value : Union[int, str, bytes]) -> None :
    assert size > 0 and size <= 8, "size error"
    if isinstance(value, int) :
        # TODO: Considering byte order according to arch
        assert value <= 0xffffffffffffffff
        data = int.to_bytes(value, byteorder = "little")
    elif isinstance(value, str) :
        assert len(value) <= 8
        data = bytes(value, "utf-8")
    elif isinstance(value, bytes) :
        assert len(value) <= 8
        data = value
    else :
        err("TypeError")
    try :
        gdb.selected_inferior().write_memory(addr, data, size)
    except Exception as e :
        err_print_exc(e)
        

def is_access(addr : int) -> bool:
    '''
    check whether access in given memory address
    '''
    try : 
        read(addr, 1)
        return True
    except : 
        return False

# write a bytes
def poke():
    ...

class Page:
    '''
    one page of virtual memory space and page permission and so on
    '''
    def __init__(
        self, start : int, end : int, 
        perm : int, offset : int, path : str
    ): 
        # perm = 4 2 1 : rwx
        self.__start  : int        = start
        self.__end    : int        = end
        self.__offset : int        = offset
        self.__path   : str        = path
        self.__rwx    : List[bool] = [perm & 4, perm & 2, perm & 1]
    
    @property
    def start(self) -> int:
        return self.__start

    @property
    def end(self) -> int:
        return self.__end
    
    @property
    def offset(self) -> int:
        return self.__offset
    
    @property
    def path(self) -> str:
        return self.__path
    
    @property
    def can_read(self) -> bool :
        return self.__rwx[0]
    
    @property
    def can_write(self) -> bool :
        return self.__rwx[1]
    
    @property
    def can_exec(self) -> bool :
        return self.__rwx[2]

    @property
    def perm_str(self) -> str :
        assert self.__rwx

        return ''.join([
            'r' if self.__rwx[0] else '-',
            'w' if self.__rwx[1] else '-',
            'x' if self.__rwx[2] else '-',
        ])# omit 'p' ,seemings like no use

    def __str__(self) -> str:
        # TODO: considering heap
        # Colorify each page line

        color = None
        if self.can_exec :
            color = "red"

        if "stack" in self.path:
            color = "purple"

        return Color.colorify(" ".join(
            list(map(
                lambda addr : self.fmt_addr(addr),
                [ self.start, self.end, self.offset ] 
            ))+ [ "{:<4s}{}".format(self.perm_str, self.path) ]
        ), color)

    def fmt_addr(self, addr : int):
        # format to 0xffffffffffffffff
        # TODO: current only considering 64-bit
        return f"0x{addr:016x}"
        
        
        
        

