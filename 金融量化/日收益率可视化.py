import pandas as pd
import tushare as ts
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
import datetime
from datetime import datetime
import numpy as np
import scipy.optimize as sco
import csv

# 设置坐标轴的标签与标题
mpl.rcParams["font.family"] = "Kaiti"
mpl.rcParams["axes.unicode_minus"] = False
mpl.rcParams["font.style"] = "normal"
mpl.rcParams["font.size"] = 10


# 日收益率可视化.py
df = pd.read_csv("R.csv", index_col='date', parse_dates=['date'])[
    ['Rxpp', 'Rqdpj', 'Rmeidi', 'Rhksw', 'Rhryy']]
#df.rename(columns={'Rqdpj': '青岛啤酒', 'Rmeidi': '美的', 'Rhksw': '华科生物', 'Rhryy': '恒瑞药业', 'Rxpp': '香飘飘'}, inplace=True)
print(df.head())
df[['Rxpp', 'Rqdpj', 'Rmeidi', 'Rhksw', 'Rhryy']].plot(figsize=(17, 9))
plt.legend(["香飘飘", "青岛啤酒", '美的', '华科生物', '恒瑞药业'])
plt.title("股票日收益率波动情况", fontproperties="Kaiti", fontsize=32)
plt.xlabel("日期", fontsize=24)
plt.ylabel("日收益率波动范围", fontsize=24)
plt.savefig('日收益率折线图2.png')
plt.show()
plt_dis = df[['香飘飘', '青岛啤酒', '美的', '华科生物', '恒瑞药业']].plot(figsize=(17, 9), kind="density")
plt_dis.set_title("股票日收益率分布状况", fontproperties="Kaiti", fontsize=32)
plt_dis.set_xlabel("日期", fontsize=24)
plt_dis.set_ylabel("日收益率密度", fontsize=24)
plt.savefig('日收益率分布图.png')
plt.show()