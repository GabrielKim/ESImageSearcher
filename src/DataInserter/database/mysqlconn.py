# -*- coding: utf-8 -*-

__author__ = 'Doohoon Kim'

import pymysql as mysql_py

class mysqlconn(object) :
    def __init__(self):
        """default connection setting"""
        self._host = None
        self._user = None
        self._port = 3306
        self._password = None
        self._database = None
        self._charset=''

        self._conn = None

        self._result_table = None

        self._cursor = None
        self._row_cnt = None

    def _SetConn(self, __host=None, __user=None, __port=None,
                 __password=None, __database=None, __charset=''):
        """This implements do setting MySQL connection function"""
        if __host is not None:
            self._host = __host
        if __user is not None:
            self._user = __user
        if __password is not None:
            self._password = __password
        if __database is not None:
            self._database = __database
        if __port is not None:
            self._port = __port
        if __charset is not None:
            self._charset = __charset

    # public methods
    def connect(self, host, user, port,
                password, database, charset=''):
        """

        :type database: object
        """
        self._SetConn(host, user, port,
                      password, database, charset)

        self._conn = mysql_py.connect(host=self._host, user=self._user, password=self._password,
                                      database=self._database, port=self._port,
                                      charset=self._charset, autocommit=True)
        return self._conn

    def cursor(self):
        return self._cursor

    def getRowCnt(self):
        return self._row_cnt

    def fetchOne(self):
        return self._cursor.fetchone()

    def execQuery(self, query):
        try:

            with self._conn.cursor() as cursor:
                cursor.execute(query)
                resstr = query.split(' ')[0]
                numrows = int(cursor.rowcount)
                self._cursor = cursor
                if resstr == 'UPDATE':
                    #cursor.commit()
                    return None
                elif resstr == '':
                    # include Except at ''
                    return None
                elif resstr == 'SELECT':
                    self._row_cnt = numrows
                    return numrows
        except mysql_py.MySQLError as e:
            # for debug
            print "error :{!r}, errno is {}".format(e, e.args[0])
            return None
        finally:
            pass

    def close(self):
        self._conn.close()