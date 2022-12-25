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


import gdb
import os
import termios
__sym = {
    "banner"               : "-",
    "left-square-bracket"  : "[",
    "right-square-bracket" : "]",
    "right-arrow"          : "→",
}

def banner(title : str) -> str:
    height ,width = get_window_size()
    num = width // 2 - 6
    TITLE = "[ %s ]" % title
    # TEMP: temporary use sketchy algo to gen banner...
    retstr = ""
    for _ in range(num):
        retstr += "-"
    return Color.blueify(retstr + TITLE + retstr)

def get_window_size() -> Tuple[int ,int]:
    # os.environ.get second argu is default val if first argu can't find
    linesz, colosz = (int(os.environ.get("LINES", 20)), int(os.environ.get("COLUMNS", 80)))
    # TODO: check tty argu passed is a target like stdin
    dbg(linesz)
    dbg(colosz)
    # TODO: use termios
    return (linesz, colosz)
