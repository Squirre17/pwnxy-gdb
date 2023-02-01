'''
type info from gdb
'''
from typing import (Any, ByteString, Callable, Dict, Generator, Iterable,
                    Iterator, List, NoReturn, Optional, Sequence, Set, Tuple, Type,
                    Union, NewType)

import pwnxy.file
import pwnxy.memory
import gdb
from pwnxy.cmds import (Cmd, register)
from pwnxy.utils.debugger import (unwrap, assert_eq, assert_ne, todo)
from pwnxy.utils.output import (info, err, note, dbg)
from pwnxy.utils.color import Color

def lookup_types(*types):
    for type_str in types:
        try:
            return gdb.lookup_type(type_str)
        except Exception as e:
            exc = e
    raise exc

class TypeSet:
    def __init__(self):
        self.update()

    def update(self):
        self.char = gdb.lookup_type('char')
        self.ulong  = lookup_types('unsigned long', 'uint', 'u32', 'uint32')
        self.long   = lookup_types('long', 'int', 'i32', 'int32')
        self.uchar  = lookup_types('unsigned char', 'ubyte', 'u8', 'uint8')
        self.ushort = lookup_types('unsigned short', 'ushort', 'u16', 'uint16')
        self.uint   = lookup_types('unsigned int', 'uint', 'u32', 'uint32')
        self.void   = lookup_types('void', '()')
    
        self.uint8  = self.uchar
        self.uint16 = self.ushort
        self.uint32 = self.uint
        self.uint64 = lookup_types('unsigned long long', 'ulong', 'u64', 'uint64')
        self.unsigned = {
            1: self.uint8,
            2: self.uint16,
            4: self.uint32,
            8: self.uint64
        }

        self.int8   = lookup_types('char', 'i8', 'int8')
        self.int16  = lookup_types('short', 'i16', 'int16')
        self.int32  = lookup_types('int', 'i32', 'int32')
        self.int64  = lookup_types('long long', 'long', 'i64', 'int64')
        self.signed = {
            1: self.int8,
            2: self.int16,
            4: self.int32,
            8: self.int64
        }

        self.pvoid  = self.void.pointer()
        self.ppvoid = self.pvoid.pointer()
        self.pchar  = self.char.pointer()

        self.ptrsize = self.pvoid.sizeof

        if self.pvoid.sizeof == 4: 
            self.ptrdiff = self.uint32
            self.size_t  = self.uint32
            self.ssize_t = self.int32
        elif self.pvoid.sizeof == 8: 
            self.ptrdiff = self.uint64
            self.size_t  = self.uint64
            self.ssize_t = self.int64
        else:
            raise Exception('Pointer size not supported')
        self.null = gdb.Value(0).cast(self.void)

        
        
typeset = TypeSet()

# updata after events happen like new objfile loaded
def update():
    typeset.update()