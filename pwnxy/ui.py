from enum import Enum
from typing import (Any, ByteString, Callable, Dict, Generator, Iterable,
                    Iterator, List, NoReturn, Optional, Sequence, Set, Tuple, Type,
                    Union, NewType)
import pwnxy.file
from pwnxy.cmds import (Cmd, register)
from pwnxy.utils.debugger import (unwrap, assert_eq, assert_ne, todo)
from pwnxy.utils.output import (info, err, note, dbg)
from pwnxy.utils.color import Color
from pwnxy.config import ICOV_SYMS

import gdb
import os
import termios


def banner(title : str) -> str:
    # height ,width = get_window_size()
    # num = width // 2 - 6
    TITLEl = Color.blueify("[ ")
    TITLEr = Color.blueify(" ] >>> ----------------" )
    TITLEm = Color.greenify(title.upper())
    # TEMP: temporary use sketchy algo to gen banner...
    retstr = ""
    # for _ in range(num):
        # retstr += ICOV_SYMS["banner"]
    return Color.blueify(TITLEl + TITLEm + TITLEr) + '\n'

def get_window_size() -> Tuple[int ,int]:
    # os.environ.get second argu is default val if first argu can't find
    linesz, colosz = (int(os.environ.get("LINES", 20)), int(os.environ.get("COLUMNS", 80)))
    # TODO: check tty argu passed is a target like stdin
    # TODO: use termios
    return (linesz, colosz)
