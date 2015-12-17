# -*- coding: utf-8 -*-

'''
'''
__author__ = 'Doohoon Kim'

import ctypes as t_ctypes

class libconn:
    def __init__(self):
        self._path = None
        self._libobject = None

    # public methods
    def connCDLL(self, path):
        if path is not None:
            self._libobject = t_ctypes.CDLL(path)
            return self._libobject
        else:
            return None
