from enum import Enum
from typing import (Any, ByteString, Callable, Dict, Generator, Iterable,
                    Iterator, List, NoReturn, Optional, Sequence, Set, Tuple, Type,
                    Union, NewType)
import pwnxy.file
import pwnxy.memory
from pwnxy.cmds import (Cmd, register)
from pwnxy.utils.debugger import (unwrap, assert_eq, assert_ne, todo)
from pwnxy.utils.output import (info, err, note, dbg)
from pwnxy.utils.color import Color
from pwnxy.address import Address

import gdb

class Page:
    '''
    one page of virtual memory space and page permission and so on
    '''
    class Attribute(Enum):
        stack  = 1
        heap   = 2
        code   = 3
        data   = 4
        rodata = 5 
        # rwx    = 6

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

        '''
        NOTE: order here is important
        '''

        if "[stack" in self.__path: 
            self.__attr = self.Attribute.stack
        elif "[heap" in self.__path: 
            self.__attr = self.Attribute.heap
        elif self.rw:
            self.__attr = self.Attribute.data
        elif self.can_execute:
            self.__attr = self.Attribute.code
        else: 
            self.__attr = self.Attribute.rodata

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
    def can_execute(self) -> bool :
        return self.__rwx[2]

    @property
    def rw(self) -> bool :
        return self.can_read and self.can_write

    @property
    def rwx(self) -> bool :
        return self.can_read and self.can_write and self.can_execute

    @property
    def attr(self) -> Attribute :
        return self.__attr

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
        if self.can_execute :
            color = "red"

        if "stack" in self.path:
            color = "purple"

        return Color.colorify(" ".join(
            list(map(
                lambda addr : self.fmt_addr(addr),
                [ self.start, self.end, self.offset ] 
            ))+ [ "{:<4s}{}".format(self.perm_str, self.path) ]
        ), color)

    def __contains__(self, addr):
        '''
        for addr in page
        '''
        return self.start <= addr < self.end
        
    def fmt_addr(self, addr : int):
        # format to 0xffffffffffffffff
        # TODO: current only considering 64-bit
        return f"0x{addr:016x}"