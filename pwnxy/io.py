'''
core fearure, forward msg to other terminal
'''
from collections import Queue
import sys
class IO:
    queue : "Queue"
    def __init__(self):
        self.queue = Queue()

    def __enter__(self):
        self.queue.append([sys.stdin, sys.stdout, sys.stderr])
    
    def __exit__(self) :
        sys.stdin, sys.stdout, sys.stderr = self.queue.pop()

io = IO()