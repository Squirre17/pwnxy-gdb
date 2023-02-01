from enum import Enum
from typing import (Any, ByteString, Callable, Dict, Generator, Iterable,
                    Iterator, List, NoReturn, Optional, Sequence, Set, Tuple, Type,
                    Union, NewType)
import pwnxy.file
from pwnxy.cmds import (Cmd, register, AliasCmd)
from pwnxy.utils.debugger import (assert_eq, assert_ne, todo)
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
from pwnxy.monitor import memory_monitor
from loguru import logger

debug = 1

@register
class MonitorMem(Cmd):
    cmdname  = 'monitormem'
    syntax   = 'mm [subcmd] [:optional arguments]'
    examples = (
        "mm show                             (show current Monitored memory)",
        "mm add 0xdeadbeef                   (add a mm in given address)",
        "mm rm  0xdeadbeef",
        "mm add 0xdeadbeef [wordlen] [count] (specify word length and count of given address)",
    )
    aliases  = ['mm']

    @handle_exception
    @only_if_running
    def invoke(self, args : List[str], from_tty : bool = False) -> None:

        argv = args.split() 
        argn = len(argv)
        self.do_invoke(argv, argn, from_tty)

    mmtab : List[Tuple[int, Address]] = [] # store (hash, Address) for query to memory_monitor

    def show(self, argv : List[str], argc : int):

        if self.mmtab == []:
            if debug:
                note("No monitored memory now")
            return
        
        single_fmt = "0x{:016x}"
        fmt = "{a:<18} : {b:>18} {c:>18}"

        _c = lambda x, f : Color.underlineify(Color.highlightify(single_fmt.format(x))) if f else single_fmt.format(x)
        
        lines = []

        for hash, addr in self.mmtab:

            mems : List[Tuple[int, bool]] = memory_monitor.read(hash)
            line_count = len(mems) // 2

            for i in range(line_count):
                
                lines.append(fmt.format(
                    a = Color.blueify("{:#x}".format(int(addr) + 16 * i)),
                    b = _c(int(mems[i*2][0]), mems[i*2][1]),
                    c = _c(int(mems[i*2+1][0]), mems[i*2+1][1]),
                ))

        result = pwnxy.ui.banner("MM") + "\n".join(lines) + "\n"

        self.outstream.printout(result)
        
    def mm_cli_set(self, name : str, op = "on") -> None:
        '''
        expose a interface to cli
        '''
        if op == "on":
            self.outstream = select_ops(OutType.CLI, name)
        elif op == "off":
            self.outstream = select_ops()
        else:
            logger.error("unreachable")
        
        note(f"monitor mem is relay ({op})")
    
    def add(self, argv : List[str], argc : int):
        
        # TODO: if user pass a crafted address will cause a crash
        if argc == 1:
            addr = Address(argv[0])
            wordlen = 8
            count = 8
        if argc == 2:
            addr ,wordlen = Address(argv[0]), argv[1]
            count = 8
        if argc == 3:
            addr ,wordlen ,count = Address(argv[0]), argv[1], argv[2]
            # for simplify subsequent processing use even
            count = (count + 1) if count % 1 else count
        
        # TODO: only support 8 word lengh currently
        wordlen = 8
        hashval = memory_monitor.add(addr, wordlen, count)
        self.mmtab.append((hashval,addr))
        
    
    def rm(self, argv : List[str], argc : int):
        raise NotImplementedError
    
    op2fn = {
        "show" : show ,
        "add"  : add  ,
        "rm"   : rm   ,
    }
    optab : Tuple[str]

    def do_invoke(self, argv : List[str], argn : int, from_tty : bool = False) -> None:
        
        if argn > 5:
            warn(f"arguments too many")
            self.usage(self)
            return
        
        if argn < 1:
            warn(f"arguments too few")
            self.usage(self)
            return

        self.optab = (k for k, _ in self.op2fn.items())

        if argv[0] not in self.optab:
            warn(f"subcmd must in ({','.join(self.optab)}), but found `{argv[0]}`")
            self.usage(self)
            return
        
        
        op ,argv = argv[0], argv[1:]

        self.op2fn[op](self, argv, len(argv))

        # TODO: register to event and print to screen
    
    def __init__(self):
        # PUZZ: why not generate optab here
        self.optab = (k for k, _ in self.op2fn.items())
        # for i in self.optab:
        self.outstream = select_ops()

        super().__init__(self.cmdname)
        for alias in self.aliases:
            AliasCmd(alias, self.cmdname)