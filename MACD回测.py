import data
import ic_analysis

import talib as ta
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
    #return df.close.pct_change().fillna(0).tz_localize('UTC')
    return df
df = select('sh600007')
fm = df

print('fm:/n', fm)



# 策略函数
def Strategy(fm):
    fm['DIF'], fm['DEA'], fm['MACD'] = ta.MACD(fm.close, fastperiod=12, slowperiod=26, signalperiod=20)
    # fm['LMA'] = fm.close.rolling(12, min_periods=0).mean()  # 12日均线时间序列
    # fm['SMA'] = fm.close.rolling(6, min_periods=0).mean()  # 6日均线时间序列
    fm['position'] = 0  # 记录持仓
    fm['trade'] = 0  # 记录交易
    for i in range(12, len(fm) - 1):
        # 当前空仓、金叉，买进。
        if (fm.MACD[i - 1] >0)  & (fm.MACD[i-4]<0) & (fm.position[i] == 0):
            fm.iloc[i, -1] = 1
            fm.iloc[i + 1, -2] = 1

        # 当前持仓、死叉，卖出。
        elif (fm.MACD[i - 1] <0)  & (fm.MACD[i-4]>0) & (fm.position[i] == 1):
            fm.iloc[i, -1] = -1
            fm.iloc[i + 1, -2] = 0

            # 其他情况，仓位不变。
        else:
            fm.iloc[i + 1, -2] = fm.iloc[i, -2]

    # 日收益率ret，累计净值nav，基准净值benchmark。
    fm['ret'] = fm.close.pct_change(1).fillna(0)
    fm['nav'] = (1 + fm.ret * fm.position).cumprod()
    fm['benchmark'] = fm.close / fm.close[0]

    return fm


# 评价函数
def Performace(fm):
    # 年化收益率
    rety = fm.nav[fm.shape[0] - 1] ** (250 / fm.shape[0]) - 1
    # 夏普比率
    Sharp = (fm.ret * fm.position).mean() / (fm.ret * fm.position).std() * np.sqrt(250)
    # 最大回撤率
    DrawDown = 1 - fm.nav / fm.nav.cummax()
    MaxDrawDown = max(DrawDown)

    print('夏普比率为:', round(Sharp, 2))
    print('年化收益率为:{}%'.format(round(rety * 100, 2)))
    print('最大回撤为：{}%'.format(round(MaxDrawDown * 100, 2)))

    # 作图
    xtick = np.round(np.linspace(0, fm.shape[0] - 1, 7), 0)
    xtick = xtick.astype(int)
    xticklabel = fm.date[xtick]

    plt.figure(figsize=(9, 4))
    ax = plt.axes()

    plt.plot(np.arange(fm.shape[0]), fm.benchmark, 'black', label='benchmark', linewidth=2)
    plt.plot(np.arange(fm.shape[0]), fm.nav, 'red', label='nav', linewidth=2)
    # RS为相对强弱指数。
    plt.plot(np.arange(fm.shape[0]), fm.nav / fm.benchmark, 'yellow', label='RS', linewidth=2)
    plt.legend()
    ax.set_xticks(xtick)
    ax.set_xticklabels(xticklabel)

    return rety, Sharp, MaxDrawDown


fm = Strategy(fm)
rety, Sharp, MaxDrawDown = Performace(fm)
fm[['ret','benchmark']].plot()
print(fm,rety, Sharp, MaxDrawDown)
