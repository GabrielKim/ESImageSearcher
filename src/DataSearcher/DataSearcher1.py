# -*- coding: utf-8 -*-

__author__ = 'Doohoon Kim'

import sys
import os

import time
import numpy as np

from improc.improc import improc as ima
from database.mysqlconn import mysqlconn as mc
from util.util import util as utl
from lshsearcher.lshsearcher import lshsearcher as lss

DIM = 5120
FeatureSize=40

dbhost = 'localhost'
dbuser = 'root'
dbport = 3306
dbpasswd = '1q2w3e'
dbdatabase = 'image_test'
dbcharset = 'utf8'

table_name = 'repo'
my = mc()
im = ima()
ut = utl()
ls = lss()

DataTable = None

argv = None

def prepare():
    try:
        conn = my.connect(dbhost, dbuser, dbport, dbpasswd, dbdatabase, dbcharset)
        if conn is None:
            print "Error as sql connect"
        else:
            ls.conf(DIM)
    finally:
        print "pass"
    return conn

def confirmTableStatus():
    try:
        print 'DB에서 불러오기...'
        t0 = time.time()

        cnt = my.execQuery("SELECT * FROM " + table_name + ";")

        t1 = time.time()
        print 'DB에서 불러오는 시간 : %f seconds' % (t1-t0)

        if cnt is 0:
            print "Error : No import Datas."
            return False
        else:
            pass

        return True
    except:
        print "except"
        return False

def insDatabaseDatas():
    print '데이터 삽입...'
    t0 = time.time()

    x = my.getRowCnt()
    # DB에서 불러온 데이터를 삽입.
    for i in range(x):
        data = my.fetchOne()
        array = ut.StrArrayTofArray(data[3])

        """
            Data를 Insert 한다고 해도, 길이가 다를수 있기 때문에 길이가 다른 것에 대한 문제를 처리함.
        """
        # 길이가 맞지 않는다면..(inserter도 동일한 처리)
        if len(array) > DIM:
            # 클 때, 잘라서 없에버린다
            del array[DIM:]
        elif len(array) < DIM:
            # 작을 때, 추가해준다..(inserter도 동일한 처리)
            dummy = [0.0] * (DIM - len(array))
            array.extend(dummy)

        conv_array = np.float32(array)
        ls.getData(conv_array)

    t1 = time.time()
    print '데이터 삽입 시간 : %f seconds' % (t1-t0)

    print '데이터 커밋...'
    t0 = time.time()

    ls.commitData()

    t1 = time.time()
    print '데이터 커밋 시간 : %f seconds' % (t1-t0)

    return True

def imageInput(path):
    feature = im.doProc(path, FeatureSize)
    if feature is None:
        pass
    else:
        return feature

def findData(path):
    # 데이터 불러오기 및 비교부.
    print '비교 데이터 삽입 및 검색 찾기...'
    t0 = time.time()
    feature = imageInput(path)

    # Feature는 변환해서 넣어준다.
    # 2d Array -> 1d Array.
    darray = ut.conv2DArrayTo1DArray(ut.floatToNpfloat32(feature))

    # darray -> str array -> float array
    strArray = ut.fdArrayToStrArray(darray)
    darray = ut.StrArrayTofArray(strArray)

    # 길이가 맞지 않는다면..(Searcher도 동일한 처리)
    if len(darray) > DIM:
        # 클 때, 잘라서 없에버린다..(Searcher도 동일한 처리)
        del darray[DIM:]
    elif len(darray) < DIM:
        # 작을 때, 추가해준다..(Searcher도 동일한 처리)
        dummy = [0.0] * (DIM - len(darray))
        darray.extend(dummy)

    # 값의 정규화를 위해 처리.
    # 자세한 설명은 datains에 있다.
    darray[:] = [x / 255.0 for x in darray]

    result = ls.find(darray)
    t1 = time.time()
    print '데이터 검색 시간 : %f seconds' % (t1-t0)
    print "%s" % (result)

if __name__ == '__main__':
    # Sys Argument
    argv = str(sys.argv[0])
    #it's debug pass
    argv = "00000.jpg"

    if argv == '' or None:
        print "No Argument.\nEnd."
        pass
    else:
        imageDataPath = argv
         # connecting mysql.
        if prepare() is not None:
            if confirmTableStatus() is True:
                if insDatabaseDatas() is True:
                    findData(imageDataPath)
                print "End."
            else:
                print "Error. Exit."
        else:
            print "Exit."