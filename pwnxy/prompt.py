from typing import (Any, ByteString, Callable, Dict, Generator, Iterable,
                    Iterator, List, NoReturn, Optional, Sequence, Set, Tuple, Type,
                    Union, NewType)
import pwnxy.file
from pwnxy.cmds import (Cmd, register)
from pwnxy.utils.debugger import (unwrap, assert_eq, assert_ne, todo)
from pwnxy.utils.output import (info, err, note, dbg)
from pwnxy.utils.color import Color
from pwnxy.utils.hightlight import highlight_src
import gdb
from pwnxy.arch import curarch
from pwnxy.ui import banner
from pwnxy.config.parameters import Parameter
from collections import defaultdict
from pwnxy.proc import proc 

def current_prompt(gdb_prompt) -> str:
    if proc.is_alive:
        try:
            funcname = str(gdb.newest_frame().function())
        except Exception as e:
            err(e)
    else :
        funcname = "inactive" 
    return Color.purpleify('# ')       + \
           Color.redify('pwnxy ')      + \
           Color.blueify('@ ')         + \
           Color.yellowify(funcname)   + \
           Color.greenify(' > ')