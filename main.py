#!/usr/local/bin/python
# -*- coding: utf-8 -*-

"""
1.支持Linux和Windows

2.只支持中文文件名,不支持中文内容

3.只支持往下累加,不支持多次执行填充同一行的多列数据

3.需要安装 MySQLdb, xlwt, xlrd, xlutils, matplotlib, pandas, numpy

4.需要安装中包,执行前需要设置语言 export LANG=zh_CN.GB18030

4.需要配合数据库,配置表结构为:
        CREATE TABLE `config` (
            id` int(11) NOT NULL AUTO_INCREMENT,
            flag` int(11) NOT NULL DEFAULT '0' COMMENT '0-off 1-on 2-test',
            `needSVNCommit` int(11) NOT NULL DEFAULT '0' COMMENT '1-yes',
            `desc` varchar(1024) NOT NULL DEFAULT '',
            `path` varchar(1024) NOT NULL DEFAULT '',
            `filename` varchar(1024) NOT NULL DEFAULT '',
            `dbip` varchar(256) NOT NULL DEFAULT '',
            `dbport` int(11) NOT NULL DEFAULT '0',
            `dbuser` varchar(256) NOT NULL DEFAULT '',
            `dbpwd` varchar(256) NOT NULL DEFAULT '',
            `dbname` varchar(256) NOT NULL DEFAULT '',
            `sql` varchar(2048) NOT NULL DEFAULT '',
            `drawconfig` varchar(1024) NOT NULL DEFAULT '',
            `control` varchar(4096) NOT NULL,
        PRIMARY KEY (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8;

            - By jxc
"""

import MySQLdb.cursors as cursors
import MysqlManager
import ExcelManager
import base

# 方便测试,windows下拉取flag=2的数据
import platform
gFlag = 1
if platform.system() == "Windows":
    gFlag = 2

gConfigDBIp = "127.0.0.1"
gConfigDBPort = 3306
gConfigDBUser = 'sa1'
gConfigDBPwd = 'sa1'
gConfigDBName = "autodata_config"

if __name__ == '__main__':
    # connect to config mysql
    config = MysqlManager.MysqlManager()
    config.init(gConfigDBIp, gConfigDBPort, gConfigDBUser, gConfigDBPwd, gConfigDBName, cursors.Cursor)

    # get configs
    ret, row, tdata2 = config.select("show variables like '%character%';")
    ret, row, retconfig = config.select("SELECT id,path,filename,dbip,dbport,dbuser,dbpwd,dbname,`sql`,needSVNCommit,drawconfig FROM config WHERE flag=%d ORDER BY id DESC" % (gFlag))
    if not ret:
        print "[%s]can not get config" % base.getTimeStr()
        exit()
    configs = base.parseConfigs(retconfig)

    for i in range(len(configs)):

        # connect to data mysql
        mysqlbegin = base.getNanoSecond()
        print "[%s]begin task,id=%d" % (base.getTimeStr(), configs[i]['id'])
        svnstr = "[BEGIN]taskid=%d;file={%s};" % (configs[i]['id'], (configs[i]['path'] + configs[i]['filename']))
        mysql = MysqlManager.MysqlManager()

        ret, errstr = mysql.init(configs[i]['dbip'], configs[i]['dbport'], configs[i]['dbuser'], configs[i]['dbpwd'], configs[i]['dbname'])
        if not ret:
            svnstr = "%s[MYSQL]initerr={%s};" % (svnstr, errstr)
        else:
            # get mysql data
            ret, row, dbdata = mysql.select(str(configs[i]['sql']))
            mysqlend = base.getNanoSecond()
            mysqltime = mysqlend - mysqlbegin
            if ret and row > 0:

                ####################################### excel file
                # svn update first
                if configs[i]['needSVNCommit'] == 1:
                    base.svnUpdate(configs[i]['path'] + configs[i]['filename'])

                # open excel file
                excelbegin = base.getNanoSecond()
                excel = ExcelManager.ExcelManager()
                excel.init(configs[i]['path'], configs[i]['filename'])
                excel.setSheetByIndex(0)

                # write line
                for data in dbdata:
                    svnstr += excel.writeLine(data)
                excel.save()
                exceltime = base.getNanoSecond() - excelbegin
                svnstr = "%s[MYSQL]usetime=%fs;[EXCEL]usetime=%fs[DONE]" % (svnstr, mysqltime.total_seconds(), exceltime.total_seconds())

                # svn commit
                if configs[i]['needSVNCommit'] == 1:
                    base.svnCommit(configs[i]['path'] + configs[i]['filename'], svnstr)
                else:
                    print "[%s]no need commit,msg={%s}" % (base.getTimeStr(), svnstr)

                ####################################### draw pic
                cfgtable = base.parseDrawConfigs(configs[i]['drawconfig'])
                for drawconfig in cfgtable.items():

                    # svn update first
                    drawsvnstr = ""
                    if configs[i]['needSVNCommit'] == 1:
                            base.svnUpdate(configs[i]['path']+drawconfig[1]['fname'])

                    # draw pic
                    drawbegin = base.getNanoSecond()
                    try:
                        excel.drawGraph(drawconfig[1])
                    except BaseException as e:
                        drawsvnstr = "%s[DRAWERR]%s" % (drawsvnstr, str(e))
                    drawtime = base.getNanoSecond() - drawbegin
                    drawsvnstr = "%s[DRAW]name=%s,usetime=%fs" % (drawsvnstr, drawconfig[1]['fname'], drawtime.total_seconds())

                    # svn commit
                    if configs[i]['needSVNCommit'] == 1:
                        base.svnCommit(configs[i]['path']+drawconfig[1]['fname'], drawsvnstr)
                    else:
                        print "[%s]no need commit,msg={%s}" % (base.getTimeStr(), drawsvnstr)

            elif ret and row <= 0:
                print "[%s][MYSQL]select success but no data;" % base.getTimeStr()
            else:
                print "[%s][MYSQL]select err={%s};" % (base.getTimeStr(), dbdata)
            ## if ret and row > 0:
        ## if not ret:

        print "[%s]end sleep:%d" % (base.getTimeStr(), 1)
        mysql.close()
        base.sleep(1)

    ##for i in range(len(configs)):
    print "[%s]all done!bye!" % base.getTimeStr()

