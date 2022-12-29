'''
current only support ELF64
'''
from typing import (Dict, Type)
from enum import Enum
import gdb
import elftools
import pathlib
from pwnxy.external import Shell
from pwnxy.utils.decorator import debug
from pwnxy.utils.output import dbg
class ELF:
    __sec_protection : Dict[str, bool] = {}
    # DEPRE: 
    class Sec(Enum):
        Canary   = 0x1 
        NX       = 0x2
        PIE      = 0x3
        Fortify  = 0x4
        RelRO    = 0x5

    def __init__(self, filepath : str) :
        self.path = pathlib.Path(filepath).expanduser()
        if not self.path.exists() :
            raise FileNotFoundError(f"{self.path} does not exist/readable")
        
        with self.path.open("rb") as fd :
            # TODO: check magic
            ...
    def checksec(self) -> Dict[str, bool]:
        # TODO: seemings like only GNU have canary
        # NOTE: we don't distinguish partial relro and no relro
        # REF: https://ctf101.org/binary-exploitation/relocation-read-only/
        path = self.path
        canary_cmd  = f"readelf -s {path} | grep __stack_chk_fail"
        nx_cmd      = f"readelf -W -l {path}  | grep 'GNU_STACK'"
        pie_cmd     = f"readelf -h {path} | grep Type"
        # relro_p_cmd = f"readelf -l {path} | grep 'GNU_RELRO'"
        relro_f_cmd = f"readelf -d {path} | grep 'BIND_NOW'"
        self.__sec_protection["CANARY"] = True if Shell.execute_cmd(canary_cmd) else False
        self.__sec_protection["NX"] = True if "RWE" not in Shell.execute_cmd(nx_cmd) else False
        self.__sec_protection["PIE"] = True if "DYN" in Shell.execute_cmd(pie_cmd) else False
        # self.__sec_protection["RELRO_P"] = True if Shell.execute_cmd(relro_p_cmd) else False
        self.__sec_protection["RELRO"] = True if Shell.execute_cmd(relro_f_cmd) else False
        self.__sec_protection["FORTIFY"] = False # TODO:

        return self.__sec_protection

