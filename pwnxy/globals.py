from typing import (Any, ByteString, Callable, Dict, Generator, Iterable,
                    Iterator, List, NoReturn, Optional, Sequence, Set, Tuple, Type,
                    Union, NewType)
from pwnxy.cmds import Cmd
# ------ GLOBAL REGION ------ 
__registered_cmds__ : Set[Type["Cmd"]] = set()
# ---------  END  -----------


