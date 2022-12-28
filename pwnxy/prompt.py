from typing import (Any, ByteString, Callable, Dict, Generator, Iterable,
                    Iterator, List, NoReturn, Optional, Sequence, Set, Tuple, Type,
                    Union, NewType)
from pwnxy.globals import __registered_cmds_cls__
import pwnxy.file
from pwnxy.cmds import (Cmd, register)
from pwnxy.utils.debugger import (deprecated ,unwrap, assert_eq, assert_ne, todo)
from pwnxy.utils.output import (xy_print, info, err, note, dbg)
from pwnxy.utils.color import Color
from pwnxy.utils.hightlight import highlight_src
import gdb
from pwnxy.arch import curarch
from pwnxy.ui import banner
from pwnxy.registers import AMD64_REG
from pwnxy.config.parameters import Parameter
from collections import defaultdict


# TODO: not alive???
def current_prompt(gdb_prompt) -> str:
    try:
        funcname = str(gdb.newest_frame().function())
    except Exception as e:
        err(e)
    
    return Color.purpleify('# ')       + \
           Color.redify('pwnxy ')      + \
           Color.blueify('@ ')         + \
           Color.yellowify(funcname)   + \
           Color.greenify(' > ')