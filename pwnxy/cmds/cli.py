from enum import Enum
from typing import (Any, ByteString, Callable, Dict, Generator, Iterable,
                    Iterator, List, NoReturn, Optional, Sequence, Set, Tuple, Type,
                    Union, NewType)
import pwnxy.file
from pwnxy.cmds import (Cmd, register)
from pwnxy.utils.debugger import (unwrap, assert_eq, assert_ne, todo)
from pwnxy.utils.output import (err_print_exc, xy_print, info, err, note, dbg, warn)
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
from pwnxy.client import pwnxy_cli
from pwnxy.outs import select_ops, OutStream, OutType

# TODO: context + subcmd like `context bracktrace`
# def disasm_context() -> None: ...
# TODO: source code need syntax highlight

# TODO: add user context specify setting
# TODO: 
@register
class Cli(Cmd):
    cmdname  = 'context'
    syntax   = 'context [subcmd]'
    examples = (
        "context",
        "context regs/disasm/code/bt/ghidra/ws", # NOTE : This need to manual maintain...
        "context regs/disasm/code/bt/ghidra/ws on" # TODO: current not
    )
    aliases = []
