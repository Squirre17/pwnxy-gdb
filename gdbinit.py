#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from os import path

from typing import (Any, ByteString, Callable, Dict, Generator, Iterable,
                    Iterator, List, NoReturn, Optional, Sequence, Set, Tuple, Type,
                    Union, NewType)
from pwnxy.cmds import Cmd

dir = path.dirname(path.abspath(__file__))
sys.path.append(dir)

# ------ GLOBAL REGION ------ 
__registered_cmds__ : Set[Type["Cmd"]] = set()
# ---------  END  -----------

import pwnxy