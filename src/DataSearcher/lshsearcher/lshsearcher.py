__author__ = 'Doohoon Kim'

import numpy
import scipy
import unittest
import time

from nearpy import Engine
from nearpy.distances import CosineDistance

from nearpy.hashes import RandomBinaryProjections, HashPermutations, HashPermutationMapper

class lshsearcher:
    def __init__(self):
        self.__dimension = None
        self.__engine_perm = None
        self.__permutations = None

    def _set_confval(self, dimension=None):
        if dimension is None:
            return None
        else:
            self.__dimension = dimension

    def _engine_on(self):
        # Create permutations meta-hash
        self.__permutations = HashPermutations('permut')

        # Create binary hash as child hash
        rbp_perm = RandomBinaryProjections('rbp_perm', 14)
        rbp_conf = {'num_permutation':50,'beam_size':10,'num_neighbour':100}

        # Add rbp as child hash of permutations hash
        self.__permutations.add_child_hash(rbp_perm, rbp_conf)

        # Create engine
        self.__engine_perm = Engine(self.__dimension, lshashes=[self.__permutations], distance=CosineDistance())

    def conf(self, dimension):
        self._set_confval(dimension)
        self._engine_on()

    def getData(self, v):
        if self.__engine_perm is not None:
            self.__engine_perm.store_vector(v)

    def commitData(self):
        if self.__permutations is not None:
            self.__permutations.build_permuted_index()

    def find(self, v):
        if self.__engine_perm is not None:
            return self.__engine_perm.neighbours(v)