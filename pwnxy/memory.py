




class Page:
    '''
    one page of virtual memory space and page permission and so on
    '''
    def __init__(
        self, start : int, end : int, 
        perm : int, offset : int, path : str
    ): 
        # perm = 4 2 1 : rwx
        self.__start  : int        = start
        self.__end    : int        = end
        self.__offset : int        = offset
        self.__path   : str        = path
        self.__rwx    : List[bool] = [perm & 4, perm & 2, perm & 1]

        dbg(self.__rwx)
        
    
    @property
    def start(self) -> int:
        return self.__start

    @property
    def end(self) -> int:
        return self.__end

    @property
    def perm(self) -> int:
        return self.__perm
    
    @property
    def offset(self) -> int:
        return self.__offset
    
    @property
    def path(self) -> str:
        return self.__path
    
    @property
    def can_read() -> bool :
        return self.__rwx[0]
    
    @property
    def can_write() -> bool :
        return self.__rwx[1]
    
    @property
    def can_exec() -> bool :
        return self.__rwx[2]
    
    def perm_str() -> str :
        assert self.__rwx

        return .join([
            'r' if self.__rwx[0] else '-',
            'w' if self.__rwx[1] else '-',
            'x' if self.__rwx[2] else '-',
        ])# omit 'p' ,seemings like no use

    def __str__(self) -> str:
        
        

