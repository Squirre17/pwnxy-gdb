from typing import (Union,)
from pwnxy.utils.output import *
from pwnxy.utils.decorator import *

class Address:
    '''
    accept addr of int, str, hexstr repr
    '''
    
    def __init__(self, addr : Union[str, int]):
        if isinstance(addr, str):
            if addr.startswith("0X") or addr.startswith("0x"):
                self.__addr = int(addr, 16)
            else:
                self.__addr = int(addr, 10)
        elif isinstance(addr, int):
            self.__addr = addr
        else:
            err("TypeErr in Address")

    def __str__(self) -> str:
        return hex(self.__addr)
    
    def __int__(self) -> int:
        return self.__addr

if __name__ == "__main__":
    addr = Address(12345)
    print(int(addr))