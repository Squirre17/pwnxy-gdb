import os 
import sys

# NOTE: remember specify PYTHONPATH
from pwnxy.utils.output import (err_print_exc,info, err, note, dbg)
from pwnxy.utils.debugger import (assert_eq, assert_ne)

import gdb

# ---- decorator function ----- 


# ------ gdb execute cmds in advance ------

pre_exec_cmds = """
    set confirm off
    set verbose off
    set print pretty on
    set pagination off
    set follow-fork-mode child
""" # TODO: considering width????

# TODO: not yet 
'''
    set backtrace past-main on
    set step-mode on

    set height 0
    set history expansion on
    set history save on

    handle SIGALRM nostop print nopass
    handle SIGBUS  stop   print nopass
    handle SIGPIPE nostop print nopass
    handle SIGSEGV stop   print nopass
'''

for cmd in pre_exec_cmds.strip().splitlines():
    gdb.execute(cmd)
    info(f"gdb executed `{cmd}`")

from pwnxy.config import PWNXY_PROMPT # TODO : RM this
# TODO: temporary to choice
# gdb.execute(f"set prompt {PWNXY_PROMPT[0]}")

# TODO: maybe sometime can't disasm to intel format ?
try:
    gdb.execute("set disassembly-flavor intel")
except gdb.error:
    pass

# ------ test region ------
def from_addr(cls, p):
    try :
        ptr = gdb.Value(p)
        ptr = ptr.cast(cls.gdb_type())
    except Exception as e:
        err_print_exc(e)

    return cls(ptr)

lines_tmp = gdb.execute("show commands", from_tty = False, to_string = True)
if lines_tmp is not None:
    lines = lines_tmp.splitlines()

for ln in lines:
    dbg(ln)

dbg("--------------DBG-TEST-----------------")


# ------- all cmd load by import ------
# TODO: move to cmd __init__ and import cmd
import pwnxy.cmds.aslr
import pwnxy.cmds.vmmap
import pwnxy.cmds.x
import pwnxy.cmds.context
import pwnxy.cmds.checksec
# -------------------------------------

# aslr()
# assert_eq(b"a\n".strip(), b"a")
# dbg(int(b"1"))


from pwnxy.cmds import show_registered_cmds, PwnxyCmd

pcmd = PwnxyCmd()
pcmd.__inst_all__() # TODO: maybe can register & instantiate at same time?

# gdb.execute("b final")
# gdb.execute("c")


from pwnxy.config.parameters import Parameter
Parameter("squ", 1, "123", "456")
from pwnxy.hook import register_all_hooks
register_all_hooks()
from pwnxy.utils.decorator import debug, timer
# gdb.execute("start")

import pwnxy.breakpoint as breakpoint

# dbg(breakpoint.get())
gdb.execute("b final")
# gdb.execute("b *0x12345")
# gdb.execute("b *12345")
breakpoint.print_location()

from pwnxy.client import pwnxy_cli
# pwnxy_cli.connect()
pwnxy_cli.send("fffffff" * 10)
# ------ ---------- ------

# WARN: asdasdasd

# TODO: asdasdasd

# FIXME: asdasdasd

# REF:

# HACK:

# TEMP:

# NOTE: 

# DEPRE: 

# PUZZ: 

# IDEA:
