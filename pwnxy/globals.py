'''globals.py
for store all global variables
'''
from typing import (Any, ByteString, Callable, Dict, Generator, Iterable,
                    Iterator, List, NoReturn, Optional, Sequence, Set, Tuple, Type,
                    Union, NewType)
from pwnxy.cmds import Cmd
# ------ GLOBAL REGION ------ 
__registered_cmds_cls__ : Set[Type["Cmd"]] = set()
# ---------  END  -----------


