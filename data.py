#引入技术指标数据
from __future__ import (absolute_import ,division,print_function,unicode_literals)
import datetime #用于datetime对象操作
import os.path  #用于管理路径
import sys      #用于在argvTo[0]中找到脚本名称
import backtrader as bt #引入backtrader框架
import sys  # 用于在argvTo[0]中找到脚本名称
import backtrader as bt  # 引入backtrader框架
from backtrader.feeds import GenericCSVData  # 用于扩展DataFeed
import backtrader.indicators as btind
import pymssql
from sqlalchemy import create_engine
import pandas as pd
import akshare as ak
def select_min_stock(code):
    #写入数据
    engine = create_engine('mysql+pymysql://root:888@106.15.1.22:3306/1min')

    sql_query = "select * from {} ".format(code)
    data = pd.read_sql(sql_query, engine)
    return data

def select_5min_stock(code):
    #写入数据
    engine = create_engine('mysql+pymysql://root:888@106.15.1.22:3306/5min')
    sql_query = "select * from {} ".format(code)
    data = pd.read_sql(sql_query, engine)
    return data

def select_10min_stock(code):
    #写入数据
    engine = create_engine('mysql+pymysql://root:888@106.15.1.22:3306/10min')
    sql_query = "select * from {} ".format(code)
    data = pd.read_sql(sql_query, engine)
    return data
def select_daily_stock(code):
    #写入数据
    engine = create_engine('mysql+pymysql://root:888@106.15.1.22:3306/akshare-price-hfq')
    sql_query = "select * from {} ".format(code)
    data = pd.read_sql(sql_query, engine)
    return data

def benchmark():
    df = ak.stock_zh_index_daily_em(symbol="sh000300")
    base = df['close'].pct_change()
    base.index = df['date']
    return base