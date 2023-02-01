from typing import (Any, ByteString, Callable, Dict, Generator, Iterable,
                    Iterator, List, NoReturn, Optional, Sequence, Set, Tuple, Type,
                    Union, NewType)
import pwnxy.file
from pwnxy.cmds import (Cmd, register)
from pwnxy.utils.debugger import (unwrap, assert_eq, assert_ne, todo)
from pwnxy.utils.output import (info, err, note, dbg)
from pwnxy.utils.color import Color

def highlight_src(content : List[str], genre : str = "C") -> List[str]:
    # TODO: highlight
    # TODO: genre str -> enum
    return content