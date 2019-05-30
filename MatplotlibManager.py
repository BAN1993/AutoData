#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import base
import time
import sys
import pandas as pda
import numpy as np
from pandas import DataFrame
import matplotlib as mpl
import matplotlib.ticker as ticker

import platform
if platform.system() != "Windows":
    mpl.use('Agg')
import matplotlib.pyplot as plt

class MatplotlibManager:
    def __init__(self):
        self.m_path = ""
        self.m_excelName = ""
        self.m_savefig_dpi = 200        # 像素
        self.m_figsize_len = 10.0       # 长宽比:长
        self.m_figsize_wid = 4.0        # 长宽比:宽

        self.m_title_labelsize = 10     # 标题字体大小
        self.m_legend_loc = 3           # 图例位置(左下)
        self.m_legend_labelsize = 5     # 图例字体大小

        self.m_tick_labelsize = 5       # xy轴坐标字体大小
        self.m_ticktitle_labelsize = 8  # xy轴标题字体大小
        self.m_tick_linewidth = 1       # 曲线线宽
        self.m_tick_makersize = 1.5     # 数据标点大小
        self.m_yticks_step_base = 4     # y轴刻度在自动的基础上扩大N倍

    def init(self,path,excelname):
        self.m_path = path
        self.m_excelName = excelname
        plt.rcParams['savefig.dpi'] = self.m_savefig_dpi
        # length and width
        plt.rcParams['figure.figsize'] = (self.m_figsize_len,self.m_figsize_wid)
        # font size
        plt.rc('xtick', labelsize=self.m_tick_labelsize)
        plt.rc('ytick', labelsize=self.m_tick_labelsize)
        plt.rcParams['font.sans-serif'] = ['SimHei']
        # plt.rcParams['axes.formatter.useoffset'] = False # 关闭科学计数,好像没用

    def fixNumber(self, value):
        t = type(value)
        if isinstance(value,int) or isinstance(value,long) or isinstance(value,float):
            if value != value:
                return 0
            return value
        elif isinstance(value,str):
            if value.isdigit():
                return int(value)
            else:
                return 0
        return 0

    def draw(self,config):
        if config.has_key('columns') and len(config['columns']) > 0:
            self.drawPerspective(config)
        else:
            self.drawSimple(config)
        plt.close()

    def drawPerspective(self,config):
        print("[%s][DRAW]fname=%s,title=%s,index=%s,columns=%s,data=%s" % (
            base.getTimeStr(), config['fname'], config['title'], config['index'],
            config['columns'], config['data']))

        # pic file full path
        picFullName = "%s%s" % (self.m_path, config['fname'])

        # open file and get data
        data = DataFrame(pda.read_excel(self.m_path + self.m_excelName))
        data = data[[config['index'], config['columns'], config['data']]]

        # deal data
        dealdata = pda.pivot_table(data, index=config['index'], columns=config['columns'], aggfunc=np.sum)
        # print("-----------------------")
        # print("[%s]get:%s" % (base.getTimeStr(), dealdata))

        # draw
        minData = sys.maxint # 所有数据中最小的值
        maxData = -sys.maxint # 所有数据中最大的值
        day = []
        columns = {} # {columns,[data]}
        fig, ax = plt.subplots(1, 1)

        for a, b in dealdata.iterrows():
            # 是否有day限制
            if config.has_key('daylimit'):
                limitnum = time.mktime(time.strptime(config['daylimit'], '%Y-%m-%d'))
                tmpnum = time.mktime(time.strptime(a, '%Y-%m-%d'))
                if tmpnum < limitnum:
                    continue
            day.append(a)
            for aa, bb in b.items():
                key = aa[1]
                tmpnum = columns.get(key)
                if tmpnum is None:
                    tmpnum = []
                bb = self.fixNumber(bb)
                if bb < minData:
                    minData = bb
                elif bb > maxData:
                    maxData = bb
                tmpnum.append(bb)
                columns[key] = tmpnum

        # 如果配置了only,则只取出需要的col
        if config.has_key('only'):
            onlylist = config['only'].split(",", -1)
            for k in list(columns.keys()):
                if str(k) not in onlylist:
                    columns.pop(k)

        # 如果配置了top,则取最近一天数据前N名的列,其他过滤
        if config.has_key('top'):
            # 先将最后一天的 columns + data 组成字典
            tmpColumns = {}
            for a,b in columns.iteritems():
                if len(b) <= 0:
                    tmpColumns.clear()
                    break
                tmpColumns[a] = b[-1]
            if len(tmpColumns)>0 and len(tmpColumns) > config['top']:
                # 根据value排序
                tmpColumns = sorted(tmpColumns.items(), key=lambda x: x[1], reverse=True)
                index = config['top'] - len(tmpColumns)
                for i in range(index,0):
                    col = list(tmpColumns)[i]
                    if columns.has_key(col[0]):
                        columns.pop(col[0])

        # 根据最后一天的数据将colunms重新排序,这样颜色展示更加直观
        tmpColumns = {}
        for a,b in columns.iteritems():
            if len(b) <= 0:
                continue
            tmpColumns[a] = b[-1]
        if len(tmpColumns) > 0:
            tmpColumns = sorted(tmpColumns.items(), key=lambda  x: x[1], reverse=True) # 这里会将dic转换成list
            index = 0
            for i in range(0,len(tmpColumns)):
                data = columns[tmpColumns[i][0]]
                colname = tmpColumns[i][0]
                plt.plot(day, data, color=base.getColor(index), label=colname, linewidth=self.m_tick_linewidth, marker='.', markersize=self.m_tick_makersize)
                index += 1

        tick_spacing = 0
        if len(day) > 15 and len(day) <= 19:
            tick_spacing = 2
        elif len(day) >= 20:
            tick_spacing = len(day) / 10 + (len(day) % 10 / 10)

        # x轴间隔方案一:刻度线也省略
        if tick_spacing > 0:
            ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))

        # x轴间隔方案二:不省略刻度线
        #if tick_spacing > 0:
        #    for label in ax.get_xticklabels():
        #        label.set_visible(False)
        #    for label in ax.get_xticklabels()[::tick_spacing]:
        #        label.set_visible(True)

        # 设置y轴刻度间隔基数(自动的基础上*N)
        tmpyticks = ax.get_yticks()
        begin = tmpyticks[0]
        end = tmpyticks[-1]
        step =abs((abs(tmpyticks[1]) - abs(tmpyticks[0]))) / self.m_yticks_step_base
        print "[%s][DRAW]begin=%d,end=%d,step=%d,minData=%d,maxData=%d" % (base.getTimeStr(), begin, end, step, minData, maxData)
        if minData >= 0 and begin < 0: # 有遇到明明最小值为0但是却从负数开始
            begin = 0
        plt.yticks(np.arange(begin, end, step))

        plt.xlabel(config['index'], fontsize=self.m_ticktitle_labelsize)
        plt.ylabel(config['columns'], fontsize=self.m_ticktitle_labelsize)
        plt.title(config['title'].decode('gbk'), fontsize=self.m_title_labelsize)

        # 显示刻度线
        ax = plt.gca()
        ax.yaxis.grid(True, which='major')  # y坐标轴的网格使用次刻度
        ax.xaxis.grid(True, which='major')  # x坐标轴的网格使用主刻度

        # 图例设置
        legendCount = len(columns)  # 图例数量
        tmpncol = 1 # 标签列数
        if legendCount > 15:
            tmpncol = legendCount / 15
            if legendCount % 15 > 0:
                tmpncol += 1
        plt.legend(loc=self.m_legend_loc, bbox_to_anchor=(0.0, 0.0), fontsize=self.m_legend_labelsize, ncol=tmpncol)

        # save pic
        plt.savefig(picFullName)
        # plt.show() # show on screen

    def drawSimple(self,config):
        print("[%s][DRAW]fname=%s,title=%s,index=%s,data=%s" % (
            base.getTimeStr(), config['fname'], config['title'], config['index'], config['data']))

        # pic file full path
        picFullName = "%s%s" % (self.m_path, config['fname'])

        # open file and get data
        data = DataFrame(pda.read_excel(self.m_path + self.m_excelName))
        data = data[[config['index'], config['data']]]

        # draw
        minData = sys.maxint # 所有数据中最小的值
        maxData = -sys.maxint # 所有数据中最大的值
        day = []
        datas = []
        lastContinue = False # 这个day数据是否跳过
        for a, b in data.iterrows():
            for aa,bb in b.items():
                if aa == config['index']:
                    # 是否有day限制
                    if config.has_key('daylimit'):
                        limitnum = time.mktime(time.strptime(config['daylimit'], '%Y-%m-%d'))
                        tmpnum = time.mktime(time.strptime(bb, '%Y-%m-%d'))
                        if tmpnum < limitnum:
                            lastContinue = True
                            continue
                        else:
                            lastContinue = False
                    day.append(bb)
                else:
                    if not lastContinue:
                        bb = self.fixNumber(bb)
                        if bb < minData:
                            minData = bb
                        elif bb > maxData:
                            maxData = bb
                        datas.append(bb)
        ret = plt.plot(day, datas, label=config['data'], color='r', linewidth=self.m_tick_linewidth, marker='.', markersize=self.m_tick_makersize)

        # 显示刻度线
        gax = plt.gca()
        gax.yaxis.grid(True, which='major')  # y坐标轴的网格
        gax.xaxis.grid(True, which='major')  # xz坐标轴的网络

        # x轴间隔
        # fig, ax = plt.subplots(0)
        tick_spacing = 0
        if len(day) > 15 and len(day) <= 19:
            tick_spacing = 2
        elif len(day) >= 20:
            tick_spacing = len(day) / 10 + (len(day) % 10 / 10)
        # if tick_spacing > 0:
        #    plt.xticks(np.arange(0, len(day), tick_spacing), day)

        # x轴间隔方案一:刻度线也省略
        if tick_spacing > 0:
            ret[0]._axes.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))

        # x轴间隔方案二:不省略刻度线
        #if tick_spacing > 0:
        #    for label in ret[0]._axes.get_xticklabels():
        #        plt.get_current_fig_manager() # 好像没用
        #        label.set_visible(False)
        #    for label in ret[0]._axes.get_xticklabels()[::tick_spacing]:
        #        label.set_visible(True)

        # 设置y轴刻度间隔基数(自动的基础上*2)
        tmpyticks = gax.get_yticks()
        begin = tmpyticks[0]
        end = tmpyticks[-1]
        step = abs((abs(tmpyticks[1]) - abs(tmpyticks[0]))) / self.m_yticks_step_base
        print "[%s][DRAW]begin=%d,end=%d,step=%d,minData=%d,maxData=%d" % (
        base.getTimeStr(), begin, end, step, minData, maxData)
        if minData >= 0 and begin < 0: # 有遇到明明最小值为0但是却从负数开始
            begin = 0
        plt.yticks(np.arange(begin, end, step))

        plt.xlabel(config['index'], fontsize=self.m_ticktitle_labelsize)
        plt.ylabel(config['data'], fontsize=self.m_ticktitle_labelsize)
        plt.title(config['title'].decode('gbk'), fontsize=self.m_title_labelsize)

        # save pic
        plt.savefig(picFullName)
        # plt.show() # show on screen