#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from os import path

dir = path.dirname(path.abspath(__file__))
sys.path.append(dir)

import pwnxy
if __name__ == '__main__':
    print("__main__")