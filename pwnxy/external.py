'''
interactive with external program like linux command utilities
'''
from typing import (List, Optional)
from subprocess import Popen, PIPE
from pwnxy.utils.output import dbg
import os
class Shell:
    '''
    abstract class shouldn't be instantiated.
    In charge of communicate with external program like linux command utilities.
    and pipe so on
    '''
    @staticmethod
    def execute_cmd(cmd : str) -> Optional[str]:
        result = os.popen(cmd).read()
        return result if result else None

if __name__ == "__main__":
    cmd = "readelf -s /bin/ls | grep __stack_chk_fail"
    print(Shell.execute_cmd(cmd))