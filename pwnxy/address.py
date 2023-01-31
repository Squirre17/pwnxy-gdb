from typing import (Union,)
from pwnxy.utils.output import *
from pwnxy.utils.decorator import *
import pwnxy.memory
from loguru import logger

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
            logger.error("TypeErr in Address")

        # if not pwnxy.memory.can_access(self.__addr):
        #     logger.error(f"address {addr} cant access") # return a None for error handle
        #     return None


    def __str__(self) -> str:
        return hex(self.__addr)
    
    def __int__(self) -> int:
        return self.__addr
    
    def __add__(self, other) -> int:
        assert isinstance(other, int)
        return self.__addr + other

if __name__ == "__main__":
    addr = Address(12345)
    print(int(addr))