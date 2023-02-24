import data
import ic_analysis

from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import akshare as ak
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']        # 字体设置
import matplotlib
matplotlib.rcParams['axes.unicode_minus']=False    # 负号显示问题


def select(code):
    df = data.select_daily_stock(code)
    df['code'] = code
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
    df.index = pd.to_datetime(df.date)
    return df.close.pct_change().fillna(0).tz_localize('UTC')
df = select('sh600007')
df_300 = ak.stock_zh_index_daily_em(symbol="sh000300")
df_300['date'] = pd.to_datetime(df_300['date'], format='%Y-%m-%d')
df_300.index = pd.to_datetime(df_300.date)
df2 = df_300.close.pct_change().fillna(0).tz_localize('UTC')

date='2020-01-03'

ic_analysis.pf_analysis(df,df2,date)