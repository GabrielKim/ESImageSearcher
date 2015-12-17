# -*- coding: utf-8 -*-

__author__ = 'Doohoon Kim'

import sys
import struct

import cv2
import numpy as np

class improc:
    def __init__(self):
        pass

    def doProc(self, path, featureSize):
        img = cv2.imread(path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        des = None
        sift = cv2.SIFT(40)
        kp, des = sift.detectAndCompute(gray, None)

        if len(kp) == 0:
            return None

        return des

    def imgView(self, img):
        cv2.imshow('result', img)