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

# IDEA: maybe can add more info in prompt
PWNXY_PROMPT : List[str] = [
    Color.purpleify('# ')  + Color.redify('pwnxy ') + Color.blueify('@ ') + Color.yellowify('function') + Color.greenify(' > '), 
]

# DEBUG: HACK: 

