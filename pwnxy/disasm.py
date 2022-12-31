from typing import (Any, ByteString, Callable, Dict, Generator, Iterable,
                    Iterator, List, NoReturn, Optional, Sequence, Set, Tuple, Type,
                    Union, NewType)
import pwnxy.file
from pwnxy.cmds import (Cmd, register)
from pwnxy.utils.debugger import (unwrap, assert_eq, assert_ne, todo)
from pwnxy.utils.output import (err_print_exc, xy_print, info, err, note, dbg)
from pwnxy.utils.color import Color
from pwnxy.utils.hightlight import highlight_src
import gdb
from pwnxy.ui import banner
from pwnxy.config.parameters import Parameter
from collections import defaultdict
import pwnxy.symbol
import enum
# from pwnxy.arch import Arch, insttype
from pwnxy.address import Address
import pwnxy.reg
from pwnxy.instruction import Instruction
from pwnxy.utils.decorator import (debug)

# curarch = Arch() # TEMP: circular import
# abstract all arch instuction
# class insttype(enum.Enum): # TEMP:
#     COND_BRA = 1 # conditional branch
#     DIRE_BRA = 2 # directly branch
#     RET      = 2
#     CALL     = 3
#     OTHER    = 4
# class Instruction():
#     __bra_grp = [ insttype.COND_BRA,
#                   insttype.DIRE_BRA, 
#                   insttype.RET     ,
#                   insttype.CALL    , ]

#     def __init__(self, addr    : int, 
#                        mnem    : str, 
#                        operand : str, 
#                        length  : int):

#         self.__addr              = addr
#         self.__mnem              = mnem
#         self.__operand           = operand
#         self.__length            = length
#         self.__insttype          = self.gettype()
#         self.__dest    : Address = None             # e.g. jmp destination...  

#         # automatous get instruction symbol rather than outer argu pass
#         symbol = pwnxy.symbol.get(addr)
#         self.__symbol = str(symbol) if symbol else ""

#         if self.is_branch :
#             dbg(f"mnem = {self.mnem} ,branch operand = {self.operand}")
#             if self.is_ret:
#                 self.__dest = pwnxy.reg.get("rsp")
#             elif self.is_cond_branch or self.is_dire_branch or self.is_call:
#                 self.__dest = Address(self.__operand.split()[0].strip())
#             else :
#                 err("Unreachable")
#             dbg(f"destination is {self.__dest}")
        
#     # TEMP
#     def gettype(self) -> insttype:
#         dbg(f"inst.mnem is {self.mnem}")
#         if self.mnem.startswith("j"):
#             if self.mnem.startswith("jmp"):
#                 return insttype.DIRE_BRA
#             return insttype.COND_BRA
#         elif self.mnem == "ret":
#             return insttype.RET
#         elif self.mnem == "call":
#             return insttype.CALL
#         else:
#             return insttype.OTHER
#     @property
#     def is_taken(self) -> bool:
#         # TODO:
#         return False
#     @property
#     def addr(self) :
#         return self.__addr

#     @property
#     def dest(self) -> Optional[Address]:
#         return self.__dest
        
#     @property
#     def mnem(self) :
#         return self.__mnem

#     @property
#     def operand(self) :
#         return self.__operand

#     @property
#     def length(self) :
#         return self.__length

#     @property
#     def symbol(self) :
#         return self.__symbol
    
#     @property
#     def is_branch(self) -> bool :
#         return self.__insttype in self.__bra_grp
    
#     @property
#     def is_cond_branch(self) -> bool :
#         '''
#         whether is a conditional branch instruction
#         '''
#         return self.__insttype == insttype.COND_BRA
#     @property
#     def is_dire_branch(self) -> bool :
#         '''
#         whether is a direct branch instruction
#         '''
#         return self.__insttype == insttype.DIRE_BRA

#     @property
#     def is_call(self) -> bool :
#         '''
#         whether is a call instruction
#         '''
#         return self.__insttype == insttype.CALL
#     @property
#     def is_ret(self) -> bool :
#         '''
#         whether is a ret instruction
#         '''
#         return self.__insttype == insttype.RET    
#     @property
#     def branch_dest(self) -> Address :
#         '''
#         return a branch destination
#         '''
#         if self.is_cond_branch or self.is_dire_branch:
#             return Address(self.__operand)
#         elif self.is_call:
#             err(f"not impl yet ,operand is {self.__operand}")
#         elif self.is_ret :
#             err(f"not impl ret yet ,operand is {self.__operand}")

#     @addr.setter
#     def addr(self, addr : int) :
#         self.__addr = addr
        
#     ...

# TODO: internel use , add underscore
# instantiate it to object
class InstructionCache:
    '''
    instruction cache manager : map addr -> previous instruction
    '''
    addr2previnst : "defaultdict[int, Instruction]"
    def __init__(self) :
        self.addr2previnst = defaultdict(lambda : None)
    @debug
    def push2cache(self, insts : List[Instruction] = None) -> None:
        '''
        push a list of instruction into InstCacheMngr
        '''
        if len(insts) == 0 or len(insts) == 1 :
            return 

        prev_inst = insts[0]
        for inst in insts[1:] :
            self.addr2previnst[inst.addr] = prev_inst
            prev_inst = inst

        next_addr = prev_inst.addr + prev_inst.length
        self.addr2previnst[next_addr] = prev_inst
    @debug
    def backward_fetch(self, addr : int, count = 3) -> List[Instruction]:
        '''
        backward fetch instructions except instruction in addr
        '''
        insts : Instruction = []
        prev_inst = self.addr2previnst[addr]

        while count != 0 and prev_inst != None :
            insts.append(prev_inst)
            prev_inst = self.addr2previnst[prev_inst.addr]
            count -= 1
            
        return insts
    
class Disassembler(InstructionCache):
    '''
    interactive with gdb or externel disassembler
    In charge of instruction read 
    TODO: capstone
    '''
    def __init__(self) :
        super().__init__()
    @debug
    def get(self, addr : Address, count : int = 1) -> Union[List[Instruction], Instruction] :
        '''
        get can take in data of Address obj
        temporary use gdb internal disassembler
        if count not specify(default to 1), return a Instruction rather than a List
        '''
        addr = int(addr)
        
        # try to set flavor to intel
        try :
            gdb.execute("set disassembly-flavor intel")
        except gdb.error :
            err("TODO: intel flavor")
        try :
            arch = gdb.selected_frame().architecture()
        except Exception as e :
            err_print_exc(e)

        '''arch.disassemble return List[Dict[str, obj]]
        [
            {'addr': 4198742, 'asm': 'endbr64 ', 'length': 4},
            {'addr': 4198746, 'asm': 'push   %rbp', 'length': 1},
            {'addr': 4198747, 'asm': 'mov    %rsp,%rbp', 'length': 3}, 
            {'addr': 4198750, 'asm': 'mov    $0x8,%edx', 'length': 5}
        ]
        '''
        instructions : List[Type["Instruction"]] = []
        # + 10 for cache need
        for ins in arch.disassemble(start_pc = addr, count = count + 10):
            addr = ins["addr"]
            '''
            The rstrip() method removes any trailing characters (characters at the end a string), space is the default trailing character to remove.
            '''
            asm = ins["asm"].rstrip().split(None, 1)
            if len(asm) > 1:
                mnem, operand = asm
            else :
                mnem, operand = asm[0], ""
            length = ins["length"]
            # IDEA: maybe can create a address obj
            instructions.append(Instruction(addr, mnem, operand, length))
        
        self.push2cache(instructions)
        if count == 1:
            return instructions[0]
        return instructions[0 : count]
    @debug
    def nearpc(self) -> List[Instruction]:
        '''
        get instructions near the PC, backward is executed instructions
        forward
        '''
        # TODO: check the pc validity
        # TODO: maybe pc can directly obtain don't need of arg
        backward_num = 3 # TEMP:
        forward_num = 7
        try:
            pc = int(gdb.selected_frame().pc())
        except Exception as e:
            err_print_exc(e)
        '''
        NOTE: pwndbg use unicore to emulate execute for branch predict which I don't support now
              so I only get branch instruction in call
        '''
        passed_insts = self.backward_fetch(pc, backward_num)
        cur : Instruction = self.get(pc)
        fwd_insts : List[Instruction] = [cur]

        for _ in range(forward_num):
            if cur.is_call and cur.dest is not None:
                dbg(f"cur.dest = {str(cur.dest)}")
                cur = self.get(cur.dest)
            cur = self.get(cur.next_addr)
            fwd_insts.append(cur)
        
        return passed_insts + fwd_insts


disassembler = Disassembler()



