import os 
import sys
    
# NOTE: remember specify PYTHONPATH
from xypwn.utils.output import (info, err, hint, dbg)
from xypwn.utils.asserter import (assert_eq, assert_ne)

try:
    import gdb
except ModuleNotFoundError:
    hint("import gdb can't be standalon")
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
hint("prefix with `0x` => %#x" % 123)

for cmd in pre_exec_cmds.strip().splitlines():
    gdb.execute(cmd)
    info(f"gdb executed `{cmd}`")

# TODO: maybe sometime can't disasm to intel format ?
try:
    gdb.execute("set disassembly-flavor intel")
except gdb.error:
    pass



