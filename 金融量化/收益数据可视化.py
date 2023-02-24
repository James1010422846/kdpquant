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

# 读入csv文件数据
filename = 'all.csv'
with open(filename) as f:
    reader = csv.reader(f)
    header_row = next(reader)
    # 创建列表
    dates, meidis, qdpjs, xpps, hksws, hryys = [], [], [], [], [], []
    # 遍历并存到列表中
    for row in reader:
        current_date = datetime.strptime(row[1], "%Y%m%d")
        dates.append(current_date)
        # !!!!!数据存储到csv中读取数据是字符串形式，将其转换为float或者int型
        qdpj = float(row[2])
        meidi = float(row[3])
        xpp = float(row[4])
        hksw = float(row[5])
        hryy = float(row[6])

        meidis.append(meidi)
        qdpjs.append(qdpj)
        xpps.append(xpp)
        hksws.append(hksw)
        hryys.append(hryy)

# 绘图
plt.plot(dates, meidis, label="美的")
plt.plot(dates, qdpjs, label="青岛啤酒")
plt.plot(dates, xpps, label="香飘飘")
plt.plot(dates, hksws, label="华科生物")
plt.plot(dates, hryys, label="恒瑞药业")
plt.legend(loc="best")
plt.title("股票价格历史走势", fontproperties="Kaiti", fontsize=24)  # Kaiti 中文楷体 fontproperties字体
plt.xlabel("日期", fontsize=20)
plt.ylabel("股票价格", fontsize=20)
plt.savefig('股票价格走势折线图.png')
plt.show()


#（3）收益率可视化
df = pd.read_csv('all.csv')
# shift:下移  上移1位：shift（-1）
# 计算日收益率
df['Rqdpj'] = np.log(df['qdpj']) - np.log(df['qdpj'].shift(-1))
df['Rmeidi'] = np.log(df['meidi']) - np.log(df['meidi'].shift(-1))
df['Rxpp'] = np.log(df['xpp']) - np.log(df['xpp'].shift(-1))
df['Rhksw'] = np.log(df['hksw']) - np.log(df['hksw'].shift(-1))
df['Rhryy'] = np.log(df['hryy']) - np.log(df['hryy'].shift(-1))
# 去空
df.dropna(inplace=True)
df.to_csv('R.csv')

filename = 'R.csv'
with open(filename) as f:
    reader = csv.reader(f)
header_row = next(reader)
dates, meidis, qdpjs, xpps, hksws, hryys = [], [], [], [], [], []
for row in reader:
    current_date = datetime.strptime(row[2], "%Y%m%d")
    dates.append(current_date)

    qdpj = float(row[8])
    meidi = float(row[9])
    xpp = float(row[10])
    hksw = float(row[11])
    hryy = float(row[12])

    meidis.append(meidi)
    qdpjs.append(qdpj)
    xpps.append(xpp)
    hksws.append(hksw)
    hryys.append(hryy)

# 绘图
plt.figure(figsize=(17, 9))
plt.plot(dates, meidis, label="美的")
plt.plot(dates, qdpjs, label="青岛啤酒")
plt.plot(dates, xpps, label="香飘飘")
plt.plot(dates, hksws, label="华科生物")
plt.plot(dates, hryys, label="恒瑞药业")
plt.legend(loc="best")
plt.title("股票日收益率波动情况", fontproperties="Kaiti", fontsize=32)
plt.xlabel("日期", fontsize=24)
plt.ylabel("日收益率波动范围", fontsize=24)
plt.savefig('日收益率折线图.png')
plt.show()