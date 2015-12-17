# -*- coding: utf-8 -*-

__author__ = 'Doohoon Kim'

import sys
import os

sys.path.insert(0, os.path.abspath('..'))

from database.mysqlconn import mysqlconn
#import unittest

def test_conn():
    try:
        mydb = mysqlconn()
        mydb.connect('localhost','root', 3306, '1q2w3e', 'image_test')
        mydb.execQuery("select * from im_test")
        mydb.close()
    finally:
        print "pass"

if __name__ == '__main__':
    # test code
    test_conn()