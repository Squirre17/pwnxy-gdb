from enum import Enum
from typing import (Any, ByteString, Callable, Dict, Generator, Iterable,
                    Iterator, List, NoReturn, Optional, Sequence, Set, Tuple, Type,
                    Union, NewType)
import pwnxy.file
from pwnxy.cmds import (Cmd, register, AliasCmd)
from pwnxy.utils.debugger import (unwrap, assert_eq, assert_ne, todo)
from pwnxy.utils.output import (err_print_exc, info, err, note, dbg, warn)
from pwnxy.utils.color import Color
from pwnxy.utils.hightlight import highlight_src
import gdb
from pwnxy.arch import curarch
import pwnxy.ui
from pwnxy.registers import AMD64_REG
from pwnxy.config.parameters import Parameter
from pwnxy.disasm import disassembler, Instruction
from pwnxy.utils.decorator import *
from pwnxy.breakpoint import BPs
from pwnxy.address import Address
from pwnxy.config import ICOV_SYMS
from pwnxy.outs import select_ops, OutStream, OutType

import gdb
import functools

# REF: https://getdocs.org/Gdb/docs/latest/gdb/Events-In-Python#:~:text=GDB%20provides%20a%20general%20event%20facility%20so%20that,vary%20depending%20on%20the%20details%20of%20the%20change.

registered_event2handler = {
    gdb.events.exited        : [],
    gdb.events.cont          : [],
    gdb.events.new_objfile   : [],
    gdb.events.stop          : [],
    gdb.events.start         : [],
    gdb.events.before_prompt : [],  # TODO: don't understand now
}

def connect(handler, event, name=''):

    dbg("Connecting", handler.__name__, event)

    @functools.wraps(handler)
    def caller(*a):

        dbg('%r %s.%s %r\n' % (name, handler.__module__, handler.__name__, a))

        '''
        TODO: refer pwndbg , cache all new object file
        '''

        try:
            handler()
        except Exception as e:
            import pwnxy.exception
            pwnxy.exception.handle()
            raise e

    registered_event2handler[event].append(caller)
    event.connect(caller)
    return handler

# TODO: decorator
def reg_changed(func): return connect(func, gdb.events.register_changed, 'reg_changed')

def mem_changed(func): return connect(func, gdb.events.memory_changed, 'mem_changed')

