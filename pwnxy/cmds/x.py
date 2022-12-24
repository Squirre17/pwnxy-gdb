'''
custom address rw operation

original gdb x cmd:
x /[Length][Format] [Address expression]
x/4gx
output format :
    o - octal
    x - hexadecimal
    d - decimal
    u - unsigned decimal
    t - binary
    f - floating point
    a - address
    c - char
    s - string
    i - instruction

size :
    b - byte
    h - halfword (16-bit value)
    w - word (32-bit value)
    g - giant word (64-bit value)

custom x cmd:
    bx addr n = x/{n}bx addr
    hx addr n = x/{n}hx addr
    wx addr n = x/{n}wx addr
    gx addr n = x/{n}gx addr
'''
import re
import gdb
from enum import Enum
from typing import (Any, ByteString, Callable, Dict, Generator, Iterable,
                    Iterator, List, NoReturn, Optional, Sequence, Set, Tuple, Type,
                    Union, NewType)
from pwnxy.globals import __registered_cmds_cls__
import pwnxy.file
from pwnxy.cmds import (Cmd, register)
from pwnxy.utils.debugger import (unwrap, assert_eq, assert_ne, todo)
from pwnxy.utils.output import (xy_print, info, err, hint, dbg)
from pwnxy.utils.color import Color

class X(Cmd):
    # abstact class, shouldn't be instantiated
    def invoke(self) : ...
    def __usage__(self): ...

@register
class BX(X):
    cmdname = "bx"

    def __init__(self) : 
        super().__init__(self.cmdname)

    def do_invoke(self, args : List[str]) -> None : 
        self.invoke(args)

    # TODO: modify  all args ,not List[str], but str
    def invoke(self, args : str, from_tty : bool = False) -> None : 
        # assert len(args) == 1 or len(args) == 2

        argv = args.split()
        'bx 0x400000 4 => x/4gx 0x400000'
        if len(argv) == 0 :
            err("too few arguments") # TODO ERR type
            return 
        elif len(argv) == 1 :
            num = "10"      # default value
        elif len(argv) == 2 :
            num = argv[1]
        elif len(argv) == 3 :
            err("too much arguments") # TODO ERR type
            return 


        cmd = f"x/{num}bx {argv[0]}"
        dbg(cmd)
        gdb.execute(cmd)
    
    def __usage__(self):
        xy_print("bx usage : `bx 0x400000 4`\n"
                 "           get one byte from given addr 4 times")


        

