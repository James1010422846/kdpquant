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

df_300 = ak.stock_zh_index_daily_em(symbol="sh000300")
df_300['date'] = pd.to_datetime(df_300['date'], format='%Y-%m-%d')

# 获取工商银行历史交易数据
code = 'sh600888'
df = data.select_daily_stock(code)
df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
# 将列名日期改为date，使其与df_300具备同名日期列

# 合并两个数据表
df_merge = df.merge(df_300, how='inner', on='date')
# 将合并数据表的日期列改为时间格式
df_merge['date'] = pd.to_datetime(df_merge['date'], format='%Y-%m-%d')

# 目标策略收益率Series，pct_change的作用是根据价格计算收益率
target = df_merge['close_x'].pct_change()
# 将索引设置为日期列
target.index = df_merge['date']
# 基准策略收益率Series，计算方法相同
base = df_merge['close_y'].pct_change()
base.index = df_merge['date']
ic_analysis.qs_analysis(target,base)
