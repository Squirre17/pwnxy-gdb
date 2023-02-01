from enum import Enum
from typing import (Any, ByteString, Callable, Dict, Generator, Iterable,
                    Iterator, List, NoReturn, Optional, Sequence, Set, Tuple, Type,
                    Union, NewType)
import pwnxy.file
from pwnxy.cmds import (Cmd, register, AliasCmd)
from pwnxy.utils.debugger import (unwrap, assert_eq, assert_ne, todo)
from pwnxy.utils.output import (err_print_exc, info, err, note, dbg, warn)
from pwnxy.utils.color import Color
from pwnxy.utils.hightlight import highlight_src
import gdb
from pwnxy.arch import curarch
import pwnxy.ui
from pwnxy.registers import AMD64_REG
from pwnxy.config.parameters import Parameter
from pwnxy.disasm import disassembler, Instruction
from pwnxy.utils.decorator import *
from pwnxy.breakpoint import BPs
from pwnxy.address import Address
from pwnxy.config import ICOV_SYMS
from pwnxy.outs import select_ops, OutStream, OutType
from pwnxy.cmds.context import Context
import os
from pathlib import Path
from collections import defaultdict
import socket 
import requests
import base64

# TODO: context + subcmd like `context bracktrace`
# def disasm_context() -> None: ...
# TODO: source code need syntax highlight

# TODO: add user context specify setting
# TODO: 
@register
class Cli(Cmd):
    '''
    Cli instruction implementation
    '''
    cmdname  = 'cli'
    syntax   = 'cli [cli op] [cli name] [section] (on|off)'
    examples = (
        "cli set r regs on",
        "cli set b mm on       (cli terminal named named b, relay monitor memory on)",
        "cli show",
    )

    aliases = []

    enabled = False

    def __init__(self):
        super().__init__(self.cmdname)
        for alias in self.aliases:
            AliasCmd(alias, self.cmdname)
            
    
    def enable_decorater(func : Callable) -> Callable:
        '''
        cli must be enabled by user before use it
        '''
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            
            if args[0].enabled:
                return func(*args, **kwargs)
            else:
                warn("Cli is not enabled")
        return wrapper

    @property
    def is_enabled(self): return self.enabled

    @handle_exception
    @only_if_running
    def invoke(self, args : List[str], from_tty : bool = False) -> None:
        
        argv = args.split() 
        argn = len(argv)
        self.do_invoke(argv, argn, from_tty)

    @enable_decorater
    def set(self, argv : List[str]) -> None:

        from pwnxy.cmds import gcm
        argn = len(argv)

        # argv = r regs on
        if argn != 3:
            warn("cli set arguments not correct")
            return
        
        cliname, sec, op = (argv[i] for i in range(argn))
        # TODO cliname not used
        if sec != "mm":
            ctxobj : Type["Context"] = gcm.getobj("context")
            assert ctxobj is not None # TODO: error handle (cuz user input)
            ctxobj.ctx_cli_set(sec, op, cliname)
        else:
            mmobj = gcm.getobj("monitormem")
            assert mmobj is not None
            mmobj.mm_cli_set(cliname)

    @enable_decorater
    def show(self, argv : List[str]) -> None:

        if not self.name2port:
            warn("Not have cli currently")
            return 
            
        for n, p in self.name2port.items():
            print(f"{n:<8} ->\t{p}")

    def update_n2p(self):
        '''
        update name2port mapping table in every operations
        '''
        assert self.cli_sync_dir
        
        d = self.cli_sync_dir
        cli_name_list : List[Path] = [_ for _ in d.iterdir() if _.is_file()]
        
        if not cli_name_list:
            warn("seems like not files in {d}, maybe cli not luanched?")
            return

        # recording all files in $PWNXY_CLI_PATH/pwnxy_cli_sync
        for i in cli_name_list:
            
            p = d / i
            with open(p, 'r') as f:
                port = int(f.read().strip())
                self.name2port[i.name] = port

    name2port = dict()

    def on(self, argv : List[str]) -> None:

        pwnxy_cli_path = os.getenv("PWNXY_CLI_PATH")

        if pwnxy_cli_path is None:
            warn("env var PWNXY_CLI_PATH not set, cannot use cli")
            return
        
        d = Path(pwnxy_cli_path, "pwnxy_cli_sync")
        note(f"found sync dir in {d}")

        if not d.is_dir():
            warn("target {d} can't access as a directory")
            return

        self.enabled = True
        self.cli_sync_dir : Path = d
                    
        self.update_n2p()
        
    @enable_decorater
    def off(self, argv : List[str]) -> None:

        self.name2port.clear()
        self.enabled = False
        note("cli off")

    ops2f = { # TODO: construct ,simplify some operation
        "set" : set  , 
        "show": show , 
        "on"  : on   , 
        "off" : off  ,
    }

    def do_invoke(self, argv : List[str], argn : int, from_tty : bool = False) -> None:

        if argn > 4:
            warn("arguments number too many")
            self.usage(self)
            return

        if argn <= 0:
            warn("arguments number too few")
            self.usage(self)
            return

        op, argv = argv[0], argv[1:]
        # TODO: ops move
        optab = [k for k, _ in self.ops2f.items()] # optimize here
        if op not in optab:
            warn("op must in (%s), but found `%s`" %(",".join(optab), op))
            return 
        
        self.ops2f[op](self, argv)

    # ------ Above is send action 

    @enable_decorater
    @debug_wrapper
    def send(self, name: str, msg: str) -> bool:

        self.update_n2p()
        msg = base64.b64encode(msg.encode())

        port = self.name2port[name]
        if port is None:
            warn(f"{name} is not a recorded client name")
            return
        
        try :
            r = requests.post(url = f"http://127.0.0.1:{port}/echo", data = msg)
        except requests.exceptions.ConnectionError:
            err("connection error, can't use client send")
            return 

        dbg(f"{r.text}")
        return 

    def __TODO__(self):
        self.sd.close() # TODO: current alreadly not?