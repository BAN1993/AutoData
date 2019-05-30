#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import MySQLdb
import MySQLdb.cursors as cursors
import base

class MysqlManager(object):
    def __init__(self):
        self.m_ip = ''
        self.m_port = 0
        self.m_user = ''
        self.m_pwd = ''
        self.m_datatable = ''
        self.dbConn = None
        self.isConnected = False


    def init(self, ip, port, user, pwd, database, cursorclass=cursors.DictCursor):
        try:
            self.m_ip = ip
            self.m_port = port
            self.m_user = user
            self.m_pwd = pwd
            self.m_datatable = database
            self.dbConn = MySQLdb.Connect(host=self.m_ip, port=self.m_port, user=self.m_user, passwd=self.m_pwd,
                                          db=self.m_datatable, cursorclass=cursorclass)
            self.isConnected = True
            #cur = self.dbConn.cursor()
            #cur.execute('set names latin1')
            return True, ""
        except BaseException as e:
            print "[%s]%s" % (base.getTimeStr(), str(e))
            return False, str(e)

    def close(self):
        if self.dbConn and self.isConnected:
            self.dbConn.close()

    def ping(self):
        if not self.dbConn or not self.isConnected:
            try:
                self.dbConn = MySQLdb.Connect(host=self.m_ip, port=self.m_port, user=self.m_user, passwd=self.m_pwd,
                                              db=self.m_datatable)
                self.isConnected = True
            except BaseException as e:
                print "[%s]%s" % (base.getTimeStr(), str(e))
                self.isConnected = False
                return
        try:
            self.dbConn.ping()
        except:
            self.dbConn.ping(True)


    def select(self, sqlstr=''):
        self.ping()
        if not self.isConnected:
            return False, 0, "mysql is unconnected"
        try:
            tmpCursor = self.dbConn.cursor()
            row = tmpCursor.execute(sqlstr)
            result = tmpCursor.fetchall()
            tmpCursor.close()
            return True, row, result
        except BaseException as e:
            print "[%s]%s" % (base.getTimeStr(), str(e))
            tmpCursor.close()
            return False, 0, str(e)


    # unuse
    def querry(self, sqlstr = ''):
        self.ping()
        if not self.isConnected:
            return False, 0, []
        try:
            tmpCursor = self.dbConn.cursor()
            row = tmpCursor.execute(sqlstr)
            self.dbConn.commit()
            result = tmpCursor.fetchall()
            tmpCursor.close()
            return True, row, result
        except BaseException as e:
            print "[%s]%s" % (base.getTimeStr(), str(e))
            self.dbConn.rollback()
            tmpCursor.close()
            return False, 0, []