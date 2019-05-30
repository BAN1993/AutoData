#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import platform
if platform.system() != "Windows":
	import sys
	reload(sys)
	sys.setdefaultencoding('utf-8')

import os
import commands
import time
import datetime
import ast

# 已手动删除太淡或太相似的颜色
gColorTable = [
    '#FF0000','#0000FF','#FF00FF','#000000','#9370DB','#00CED1','#C71585','#8B008B','#D2691E','#00FA9A',
    '#ADFF2F','#FFD700','#BDB76B','#696969','#008080','#808000','#4B0082','#7FFFD4','#FF69B4','#FFFF00',
    '#6495ED','#FA8072','#7FFF00','#66CDAA','#FF7F50','#708090','#191970','#800000','#A52A2A','#FAA460',
    '#EE82EE','#CD853F','#00FF7F','#1E90FF','#00BFFF','#4682B4','#FFC0CB','#0000CD','#A9A9A9','#BC8F8F',
    '#D2B48C','#3CB371','#8B0000','#228B22','#7CFC00','#00FF00','#A0522D','#000080','#D8BFD8','#00008B',
    '#FF00FF','#FFA500','#008000','#FF4500','#2F4F4F','#C0C0C0','#FF6347','#DAA520','#E9967A','#4169E1',
    '#EEE8AA','#483D8B','#556B2F','#98FB98','#BA55D3','#FF1493','#48D1CC','#DEB887','#8B4513','#CD5C5C',
    '#9932CC','#DA70D6','#2E8B57','#6A5ACD','#B22222','#87CEEB','#7B68EE','#B8860B','#9ACD32','#DB7093',
    '#800080','#FF8C00','#DDA0DD','#006400','#808080','#32CD32']

def getTimeStr():
    """ get Like : 2018-11-20 20:54:23 """
    return str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))


def getNanoSecond():
    """ get Like : 2018-11-20 20:54:23.803000 """
    return datetime.datetime.now()


def sleep(t):
    time.sleep(t)


def parseConfigs(configs):
    retTable = {}
    for i in range(len(configs)):
        tmp = {}
        tmp['id'] = int(configs[i][0])
        tmp['path'] = str(configs[i][1])
        tmp['filename'] = str(configs[i][2])
        tmp['dbip'] = str(configs[i][3])
        tmp['dbport'] = int(configs[i][4])
        tmp['dbuser'] = str(configs[i][5])
        tmp['dbpwd'] = str(configs[i][6])
        tmp['dbname'] = str(configs[i][7])
        tmp['sql'] = str(configs[i][8])
        tmp['needSVNCommit'] = int(configs[i][9])
        tmp['drawconfig'] = str(configs[i][10])
        retTable[i] = tmp
    return retTable


def parseDrawConfigs(configs):
    retTable = {}
    try:
        if len(configs) > 0:
            retTable = ast.literal_eval(configs)
    except:
        print "[%s]parseDrawConfigs error" % (getTimeStr())
    return retTable


def svnUpdate(filename):
    (status, output) = commands.getstatusoutput('svn up %s' % filename)
    print "[%s]status=%d;output={%s};" % (getTimeStr(), status, output)


def svnCommit(filename, logmsg):
    print "[%s]logmsg={%s};" % (getTimeStr(), logmsg)
    (status, output) = commands.getstatusoutput('svn add %s' % filename)
    print "[%s]status=%d;output={%s};" % (getTimeStr(), status, output)
    (status, output) = commands.getstatusoutput('svn ci -m "%s" %s' % (logmsg, filename))
    print "[%s]status=%d;output={%s};" % (getTimeStr(), status, output)


def getColor(index):
    if index < len(gColorTable):
        return gColorTable[index]
    else:
        fix = index % len(gColorTable)
        return gColorTable[fix]
