'''
abstract out stream for STDIN or Client 
'''
from enum import Enum
from abc import ABC, abstractmethod
from pwnxy.cmds import gcm
from typing import List, Optional, Union, Type

class OutType(Enum):
    STAND = 1
    FILE  = 2
    CLI   = 3

class OutStream(ABC):

    @abstractmethod
    def printout(self, data): pass

class Cliout(OutStream):
    '''
    Out to external client, context manager wrapper
    '''
    def __init__(self, name) -> None:
        self.name = name


    def printout(self, data : str):
        cliobj = gcm.getobj("cli")
        cliobj.send(self.name ,data)

    ...

class Stdout(OutStream):
    ...
    def printout(self, data : str):
        print(data)
    

class Filout(OutStream):
    '''
    Out to file
    '''
    # TODO: implement
    pass

# export function
def select_ops(type : OutType = OutType.STAND, name : str = ""):
    '''
    select outputs, default is STDOUT
    '''
    if type == OutType.STAND:
        return Stdout()
    elif type == OutType.CLI:
        return Cliout(name)
    elif type == OutType.FILE:
        raise NotImplementedError