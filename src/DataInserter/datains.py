# -*- coding: utf-8 -*-

__author__ = 'Doohoon Kim'

"""
최대한 간단하게 작성.
"""

import sys
import os

from improc.improc import improc as ima
from database.mysqlconn import mysqlconn as mc
from util.util import util as utl

FeatureSize=40

imageDataPath = str(sys.argv[0])

dbhost = 'localhost'
dbuser = 'root'
dbport = 3306
dbpasswd = '1q2w3e'
dbdatabase = 'image_test'
dbcharset = 'utf8'

table_name = None#'repo'
my = mc()
im = ima()
ut = utl()

DIM = 5120
argv = None
arg_insMath = False

def prepare():
    # 데이터를 넣기 위한 준비.
    try:
        conn = my.connect(dbhost, dbuser, dbport, dbpasswd, dbdatabase, dbcharset)
        if conn is None:
            print "Error as sql connect"
    finally:
        print "pass"
    return conn

def searchFileAndimproc(initroot):
    # File을 리커시브하게 탐색하기 위한 처리.
    for (path, dir, files) in os.walk(initroot):
        for filename in files:
            ext = os.path.splitext(filename)[-1]
            # jpg 파일 일 때,
            if ext == '.jpg':
                full_path = os.path.join(path, filename)
                if os.stat(full_path).st_size is not 0:
                    print full_path
                    # get Feature descrition data.
                    feature = im.doProc(os.path.join(path, filename), FeatureSize)
                    if feature is None:
                        # 피쳐 정보가 안나오는 이미지는 삭제.
                        os.remove(full_path)
                    else:
                        # Feature는 변환해서 넣어준다.
                        # 2d Array -> 1d Array.
                        darray = ut.conv2DArrayTo1DArray(ut.floatToNpfloat32(feature))

                        # darray -> str array -> float array
                        strArray = ut.fdArrayToStrArray(darray)
                        darray = ut.StrArrayTofArray(strArray)

                        """
                            영상 이미지를 LSH로 비교하기 위해선 우선은 이미지에서 Feature를 생성해야 하는데,
                            이 Feature에 대한 생성을 할 경우에 간혹가다가 원래 생성하려고 하는 Feature의 갯수보다 크거나,
                            아니면 이미지 자체가 Feature를 많이 발견하지 못하기 때문에 배열을 늘이거나 혹은 줄이는 작업을 해야한다
                        """
                        # 길이가 맞지 않는다면..(Searcher도 동일한 처리)
                        if len(darray) > DIM:
                            # 클 때, 잘라서 없에버린다..(Searcher도 동일한 처리)
                            del darray[DIM:]
                        elif len(darray) < DIM:
                            # 작을 때, 추가해준다..(Searcher도 동일한 처리)
                            dummy = [0.0] * (DIM - len(darray))
                            darray.extend(dummy)

                        """
                            # 공통 사항
                            영상을 Sift로 변환하여 만든 Feature 정보는 항상 Scale invarient하다.
                            따라서 LSH를 썼을때 어떠한 벡터의 일부분은 비교하는 이미지와 거의 동일한 Document일 것이고,
                            따라서 hash값이 일치 할 가능성이 높다(Hash의 Collision 현상을 최대한 활용).
                            또한, sift의 벡터의 각도는 0부터 255 미만(영상에서 생성되는 벡터의 최소 및 최대값)이며 따라서 배열이 정수로 나오게 된다.

                            # 1. for DataSearcher1
                            이를 nearpy에 집어넣어 유사성을 찾기 위해서는, 1미만의 부동소숫점이 되어야 하는데, 이를 처리하기 위해서
                            일부러 Array를 1 미만으로 정규화 시켜주어야 한다.

                            # 2. for DataSearcher2
                            별도의 Inserter를 구현하였기 때문에, 정규화의 처리 없이 그냥 넘어가도 상관없다.
                        """
                        if arg_insMath is False:
                            # 값의 정규화를 위해 처리.
                            darray[:] = [x / 255.0 for x in darray]
                            # 위를 그대로 쓰면 BLOB 최대 값인 64k를 넘으므로 오류가 발생.
                            darray = [round(elem, 6) for elem in darray]

                        # DB에 넣을 최종 Feature Data 생성
                        featurebin_data = str(darray).strip('[]')

                        # store binary string and Filename to MySQL DB(파일 이름 정규화).
                        s = path.replace(initroot, '')

                        # DB에 넣음
                        my.execQuery("INSERT INTO " + table_name + " (last_path, file_name, im_feature)" + "VALUES ('" + s + "', '" + filename + "', '" + featurebin_data + "');")
                else:
                    # 파일의 크기가 0인것은 모두 삭제(이상한 Dummy Data 방지)
                    os.remove(full_path)

def intoMySqlDBData():
    # search image data and extract feature to finded images.
    print "Searching Image and Feature initialize.."
    searchFileAndimproc(imageDataPath)

def confirmTableStatus():
    try:
        table = my.execQuery("SHOW TABLE FROM " + dbdatabase + " like " + table_name + ";")

        # 테이블 없을 때 생성.
        if table is None:
            s = "CREATE TABLE " + table_name + " (idx INT NOT NULL AUTO_INCREMENT, last_path VARCHAR(255), file_name VARCHAR(255), im_feature BLOB(65535), PRIMARY KEY (idx));"
            my.execQuery(s)

        # 테이블 확인.
        rowcnt = my.execQuery("SHOW TABLE " + table_name + ";")

        # 테이블 자료 확인.
        if rowcnt is 0:
            pass
        elif rowcnt is None:
            pass
        else:
            dataRowCnt = my.execQuery("SELECT * FROM " + table_name + ";")

            # 테이블 자료 없을 때 집어넣고 생성.
            if dataRowCnt is 0:
                # 자료 생성.
                intoMySqlDBData()

        return True
    except:
        print "except"
        return False

if __name__ == '__main__':
    # Sys Argument
    argv = ['', '', '']

    for i in range(len(sys.argv)):
        argv[i] = str(sys.argv[i])

    #it's debug pass
    #argv[0] = 'repo'
    argv[1] = "/Users/invi/Downloads/goods_classify_11st_sample/"
    #argv[2] = '-NoReg'

    if argv[0] == '':
        print "you must setting on DB Table name."
        pass
    else:
        table_name = argv[0]

    if argv[2] == '-NoReg':
        arg_insMath = True

    if (argv[0] == '' or argv[1] == ''):
        # 아규먼트가 없을 경우
        print "No input Argument.\nEnd."
        pass
    else:
        # 아규먼트가 있을 경우 처리.
        imageDataPath = argv[1]

        if imageDataPath is '' or None:
            # 데이터의 Path가 없는 경우.
            print "No Argument. Exit"
        else:
            print "Preparing..\nusing image data path is %s" % (imageDataPath)

            # connecting mysql.
            if prepare() is not None:
                # sql connection이 준비되어 있을 경우, 테이블의 상태를 확인.
                if confirmTableStatus() is True:
                    print "End."
                else:
                    print "Error. Exit."
            else:
                print "Exit."
