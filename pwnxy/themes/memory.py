import pwnxy.themes as theme
from pwnxy.utils.color import Color
from pwnxy.address import Address
import pwnxy.vmmap 
from pwnxy.page import Page
from typing import Optional, Type, Tuple, Callable

# use pwndbg config
config_stack  = theme.InnerParameter('memory-stack-color', 'yellow', 'color for stack memory')
config_heap   = theme.InnerParameter('memory-heap-color', 'blue', 'color for heap memory')
config_code   = theme.InnerParameter('memory-code-color', 'red', 'color for executable memory')
config_data   = theme.InnerParameter('memory-data-color', 'purple', 'color for all other writable memory')
config_rodata = theme.InnerParameter('memory-rodata-color', 'normal', 'color for all read only memory')
config_rwx    = theme.InnerParameter('memory-rwx-color', 'underline', 'color added to all RWX memory')

def __stack(x):
    return Color.colorify(x, config_stack)

def __heap(x):
    return Color.colorify(x, config_heap)

def __code(x):
    return Color.colorify(x, config_code)

def __data(x):
    return Color.colorify(x, config_data)

def __rodata(x):
    return Color.colorify(x, config_rodata)

def __rwx(x):
    return Color.colorify(x, config_rwx)

def __select_color_func(page : Page) -> Callable:
    if not page:
        color = __rodata
    elif page.attr == Page.Attribute.code:
        color = __code
    elif page.attr == Page.Attribute.stack:
        color = __stack
    elif page.attr == Page.Attribute.heap:
        color = __heap
    elif page.attr == Page.Attribute.data:
        color = __data
    else:
        color = __rodata
    
    # rwx' underline is performed on the basis of dyeing 
    if page and page.rwx:
        color = lambda x : __rwx(color(x))
    return color

def dye(addr : Tuple[int, str]) -> str:
    '''
    return a colorized string of given addr.
    if only give a address , return a dyed address(str repr).
    '''

    page : Page = pwnxy.vmmap.find(Address(addr))

    color = __select_color_func(page)
    
    if isinstance(addr, int):
        return color("{:#x}".format(addr))
    elif isinstance(addr, str):
        return color(addr)
    else:
        raise TypeError

def dyetext(text : str, addr : Tuple[int, str]) -> str:
    '''
    dye the text base on addr' attribute
    '''
    page : Page = pwnxy.vmmap.find(Address(addr))

    color = __select_color_func(page)
    
    return color(text)


def legend():
    return 'LEGEND: ' + ' | '.join((
        __stack('STACK'),
        __heap('HEAP'),
        __code('CODE'),
        __data('DATA'),
        __rwx('RWX'),
        __rodata('RODATA')
    ))

