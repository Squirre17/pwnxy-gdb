from enum import Enum
from typing import (Any, ByteString, Callable, Dict, Generator, Iterable,
                    Iterator, List, NoReturn, Optional, Sequence, Set, Tuple, Type,
                    Union, NewType)
import pwnxy.file
from pwnxy.cmds import (Cmd, register)
from pwnxy.utils.debugger import (unwrap, assert_eq, assert_ne, todo)
from pwnxy.utils.output import (xy_print, info, err, note, dbg)
from pwnxy.utils.color import Color

# IDEA: maybe can add more info in prompt
PWNXY_PROMPT : List[str] = [
    Color.purpleify('# ')  + Color.redify('pwnxy ') + Color.blueify('@ ') + Color.yellowify('function') + Color.greenify(' > '), 
]

# DEBUG: HACK: 

ICOV_SYMS = {
    "banner"               : "─",
    "left-square-bracket"  : "[",
    "right-square-bracket" : "]",
    "right-arrow"          : "→",
    "cross"                : "✘",
    "tick"                 : "✓",
    "breakpoint"           : "●",
    "trun-right-arrow"     : "╰→",
}