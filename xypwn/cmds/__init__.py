from typing import (Any, ByteString, Callable, Dict, Generator, Iterable,
                    Iterator, List, NoReturn, Optional, Sequence, Set, Tuple, Type,
                    Union)
from xypwn.utils.asserter import (assert_eq, assert_ne, todo)
from xypwn.utils.output import (info, err, hint, dbg)

try:
    import gdb
except ModuleNotFoundError:
    hint("import gdb can't be standalon")

cmds : List[Type["Cmd"]] = []
cmds_name : Set[str] = set()


class Cmd:
    def __init__(self ,todo : List[Any]):
        todo()
    