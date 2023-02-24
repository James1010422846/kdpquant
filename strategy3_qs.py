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
import talib as ta
df_300 = ak.stock_zh_index_daily_em(symbol="sh000300")
df_300['date'] = pd.to_datetime(df_300['date'], format='%Y-%m-%d')

# 获取历史交易数据
def select(code):
    df = data.select_daily_stock(code)
    df['code'] = code
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
    return df
code = 'sh600007'

df = select(code)
df = df.dropna()
df = df.replace([np.inf, -np.inf], 0)
# 策略函数
def Strategy(fm):
    fm['MAX'] = fm.low.rolling(60).max()
    fm['MAX2'] = fm.low.rolling(40).max()
    fm['MIN'] = fm.low.rolling(60).min()
    fm['position'] = 0  # 记录持仓
    fm['trade'] = 0  # 记录交易
    for i in range(60, len(fm) - 1):
        # 当前空仓、金叉，买进。
        if (fm.close[i-1] < fm.MIN[i - 2]) & (fm.position[i] == 0):
            fm.iloc[i, -1] = 1
            fm.iloc[i + 1, -2] = 1
        # 当前持仓、死叉，卖出。
        elif (fm.close[i - 1] > fm.MAX[i - 2]) & (fm.position[i] == 1):
            fm.iloc[i, -1] = -1
            fm.iloc[i + 1, -2] = 0
            # 其他情况，仓位不变。
        else:
            fm.iloc[i + 1, -2] = fm.iloc[i, -2]

    # 日收益率ret，累计净值nav，基准净值benchmark。
    fm['ret'] = fm.close.pct_change(1).fillna(0)
    fm['nav'] = (1 + fm.ret * fm.position).cumprod()
    fm['benchmark'] = fm.close / fm.close[0]
    fm['ret'].plot()
    return fm
df = Strategy(df)[['date','nav']]
# 合并两个数据表
df_merge = df.merge(df_300, how='inner', on='date')
# 将合并数据表的日期列改为时间格式
df_merge['date'] = pd.to_datetime(df_merge['date'], format='%Y-%m-%d')

# 目标策略收益率Series，pct_change的作用是根据价格计算收益率
target = df_merge['nav']
# 将索引设置为日期列
target.index = df_merge['date']
# 基准策略收益率Series，计算方法相同
#base = df_merge['close_y'].pct_change()
base = df_merge['close'].pct_change()
base.index = df_merge['date']
ic_analysis.qs_analysis(target,base)
