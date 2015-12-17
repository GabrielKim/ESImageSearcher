# -*- coding: utf-8 -*-

__author__ = 'Doohoon Kim'

import numpy as np

class util:
    def __init__(self):
        pass

    # Float to np.float32
    def floatToNpfloat32(self, obj):
        return np.float32(obj)

    def arrayTondarray(self, obj):
        return np.array(obj)

    # convert 2D Array to 1D Array
    def conv2DArrayTo1DArray(self, obj):
        return np.reshape(obj, (1,np.product(obj.shape)))

    # convert 1D Array to 2D Array
    def conv1DArrayTo2Darray(self, obj, len):
        return np.reshape(obj, (-1, len))

    # convert binary to 1D Array
    def binToArray(self, obj, type):
        return np.fromstring(obj, dtype=type)

    # convert 1D Array to binary
    def arrayToBin(self, obj):
        return obj.tobytes()

    def fdArrayToStrArray(self, obj):
        array = obj.tolist()
        array = str(array).strip('[]')
        return array.replace(' ', '')

    def StrArrayTofArray(self, obj):
        return map(float, obj.split(","))
