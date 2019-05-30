#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import os
import xlwt
#import xlsxwriter
import xlrd
from xlutils.copy import copy

import MatplotlibManager
import base

class ExcelManager:
    def __init__(self):
        self.m_isFileNone = True
        self.m_path = ''
        self.m_filename = ''
        self.m_readBook = None
        self.m_writeBook = None
        self.m_readSheet = None
        self.m_writeSheet = None
        self.m_sheetIndex = 0
        self.m_rows = 0
        self.m_cols = 0
        self.matpltManager = MatplotlibManager.MatplotlibManager()


    def init(self, path,filename):
        self.m_path = path
        self.matpltManager.init(self.m_path,filename.decode('gbk'))
        if not os.path.exists(path):
            os.makedirs(path)
        self.m_filename = path + filename.decode('gbk')
        self.open()


    def open(self):
        try:
            self.m_readBook = xlrd.open_workbook(self.m_filename)
            self.m_writeBook = copy(self.m_readBook)
            self.m_isFileNone = False
        except IOError as e:
            if e.errno == 2:
                print "[%s]create new file,filename=%s" % (base.getTimeStr(), self.m_filename)
                new = xlwt.Workbook(encoding='utf-8', style_compression=0)
                new.add_sheet('data', cell_overwrite_ok=True)

                new.save(self.m_filename)
                self.m_readBook = xlrd.open_workbook(self.m_filename)
                self.m_writeBook = copy(self.m_readBook)
                self.m_isFileNone = True


    def setSheetByIndex(self,index):
        self.m_sheetIndex = index
        self.m_readSheet = self.m_readBook.sheet_by_index(self.m_sheetIndex)
        self.m_writeSheet = self.m_writeBook.get_sheet(self.m_sheetIndex)
        self.m_rows = self.m_readSheet.nrows + 1
        self.m_cols = self.m_readSheet.ncols
        if self.m_cols <= 0:
            print "[%s]file is exists,but cols=%d" % (base.getTimeStr(), self.m_cols)
            self.m_isFileNone = True
        print "[%s]row=%d,col=%d" % (base.getTimeStr(), self.m_rows,self.m_cols)


    def getTitleCols(self):
        ret = {}
        for i in range(0,self.m_cols):
            key = self.m_readSheet.cell_value(0,i)
            ret[key] = chr(97+i)
        return ret


    def writeLine(self,datatable):
        # print "rows=%d,cols=%d" % (self.m_rows,self.m_cols)
        # print "data=", datatable
        retstr = ""
        try:
            if self.m_isFileNone:
                cols = 0
                for dbkey in datatable:
                    try:
                        self.m_writeSheet.write(0, cols, str(dbkey))
                        if str(dbkey) == "day":
                            self.m_writeSheet.write(1, cols, str(datatable[dbkey]))
                        else:
                            self.m_writeSheet.write(1, cols, datatable[dbkey])
                    except IndexError as e:
                        print "[%s]%s" % (base.getTimeStr(), str(e))
                        retstr = retstr + "[EXCEL]" + str(e) + ";"
                    cols += 1
                self.save()
                self.open()
                self.setSheetByIndex(self.m_sheetIndex)
                self.m_isFileNone = False
            else:
                for i in range(0,self.m_cols):
                    getflag = False
                    filekey = self.m_readSheet.cell_value(0, i)
                    for dbkey in datatable:
                        if str(dbkey) == str(filekey):
                            if str(dbkey) == "day":
                                self.m_writeSheet.write(self.m_rows - 1, i, str(datatable[dbkey]))
                            else:
                                self.m_writeSheet.write(self.m_rows - 1, i, datatable[dbkey])
                            getflag = True
                    if not getflag:
                        print "[%s]can not find key:filekey=%s,type=%s,dbkey=%s,type=%s" % (base.getTimeStr(), str(filekey),type(str(filekey)),dbkey,type(dbkey))
                        self.m_writeSheet.write(self.m_rows-1, i, "nodata")
                self.m_rows += 1
                # self.save() # 不再每写一行就保存,效率太低
        except IndexError as e:
            print "[%s]%s" % (base.getTimeStr(), str(e))
            retstr = retstr + "[EXCEL]" + str(e) + ";"
        return retstr
    ## def writeLine(self,datatable):


    def drawGraph(self,config):
        if config.__len__ <= 0:
            return
        self.matpltManager.draw(config)
    ## def drawGraph(self,configs):


    def save(self):
        #self.m_drawBook.close()
        self.m_writeBook.save(self.m_filename)
