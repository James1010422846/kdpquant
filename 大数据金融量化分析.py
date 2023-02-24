3.2
运行代码
（1）数据采集.Py
import pandas as pd
import tushare as ts
import csv

ts.set_token('bc6edc25e6c0d0938accb6f0cb65130c1c0c1640a3900df5f042c893')  # 设置token，只需设置一次
pro = ts.pro_api()
# 对齐文本#
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)
pd.set_option('display.width', 180)  # 打印宽度(**重要**)
# 查询当前所有正常上市交易的股票列表  茅台600519.SH、美的000333.SZ、京东方
000725
SZ、恒瑞医药600276.SH和苏宁易购002024.SZ
data = pro.query('stock_basic', exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
data.to_excel('D:\Fun\data\\data.xlsx')
print(data.head())
qdpj = pro.query('daily', ts_code='600600.SH', start_date='20200101', end_date='20210507', fields='trade_date,close')
qdpj.rename(columns={'close': 'qdpj', 'trade_date': 'date'}, inplace=True)
meidi = pro.query('daily', ts_code='000333.SZ', start_date='20200101', end_date='20210507', fields='trade_date,close')
meidi.rename(columns={'close': 'meidi', 'trade_date': 'date'}, inplace=True)
hksw = pro.query('daily', ts_code='002022.SZ', start_date='20200101', end_date='20210507', fields='trade_date,close')
hksw.rename(columns={'close': 'hksw', 'trade_date': 'date'}, inplace=True)
hryy = pro.query('daily', ts_code='600276.SH', start_date='20200101', end_date='20210507', fields='trade_date,close')
hryy.rename(columns={'close': 'hryy', 'trade_date': 'date'}, inplace=True)
xpp = pro.query('daily', ts_code='603711.SH', start_date='20200101', end_date='20210507', fields='trade_date,close')
xpp.rename(columns={'close': 'xpp', 'trade_date': 'date'}, inplace=True)
# 青岛啤酒数据
print(qdpj.head())
alldata = pd.merge(pd.merge(pd.merge(pd.merge(qdpj, meidi, on='date'), xpp, on='date'), hksw, on='date'), hryy,
                   on='date')
# 转成中文   alldata.rename(columns={'qdpj':'青岛啤酒','trade_date':'日期','meidi':'美的','hksw':'华科生物','hryy':'恒瑞药业','xpp':'香飘飘'}, inplace = True)
alldata.to_csv('D:\Fun\data\\all.csv')
print(alldata.head())
alldata.rename(columns={'qdpj': '青岛啤酒', 'meidi': '美的', 'hksw': '华科生物', 'hryy': '恒瑞药业', 'xpp': '香飘飘'}, inplace=True)
alldata.to_csv('D:\Fun\data\\allChinaTitle.csv')



（2）收益数据可视化.py
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
filename = 'D:\Fun\data\\all.csv'
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
plt.savefig('D:\Fun\data\\股票价格走势折线图.png')
plt.show()

（3）收益率可视化
df = pd.read_csv('D:/Fun/data/all.csv')
# shift:下移  上移1位：shift（-1）
# 计算日收益率
df['Rqdpj'] = np.log(df['qdpj']) - np.log(df['qdpj'].shift(-1))
df['Rmeidi'] = np.log(df['meidi']) - np.log(df['meidi'].shift(-1))
df['Rxpp'] = np.log(df['xpp']) - np.log(df['xpp'].shift(-1))
df['Rhksw'] = np.log(df['hksw']) - np.log(df['hksw'].shift(-1))
df['Rhryy'] = np.log(df['hryy']) - np.log(df['hryy'].shift(-1))
# 去空
df.dropna(inplace=True)
df.to_csv('D:\Fun\data\\R.csv')

filename = 'D:\Fun\data\\R.csv'
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
plt.savefig('D:\Fun\data\\日收益率折线图.png')
plt.show()

# 日收益率可视化.py
df = pd.read_csv("D:/Fun/data/R.csv", index_col='date', parse_dates=['date'])[
    ['Rxpp', 'Rqdpj', 'Rmeidi', 'Rhksw', 'Rhryy']]
df[['Rxpp', 'Rqdpj', 'Rmeidi', 'Rhksw', 'Rhryy']].plot(figsize=(17, 9))
plt.legend(["香飘飘", "青岛啤酒", '美的', '华科生物', '恒瑞药业'])
plt.title("股票日收益率波动情况", fontproperties="Kaiti", fontsize=32)
plt.xlabel("日期", fontsize=24)
plt.ylabel("日收益率波动范围", fontsize=24)
plt.savefig('D:\Fun\data\\日收益率折线图2.png')
plt.show()
plt_dis = df[['香飘飘', '青岛啤酒', '美的', '华科生物', '恒瑞药业']].plot(figsize=(17, 9), kind="density")
plt_dis.set_title("股票日收益率分布状况", fontproperties="Kaiti", fontsize=32)
plt_dis.set_xlabel("日期", fontsize=24)
plt_dis.set_ylabel("日收益率密度", fontsize=24)
plt.savefig('D:\Fun\data\\日收益率分布图.png')
plt.show()

# 投资优化组合可视化.py
df = pd.read_csv("D:/Fun/data/R.csv", index_col='date', parse_dates=['date'])[
    ['Rxpp', 'Rqdpj', 'Rmeidi', 'Rhksw', 'Rhryy']]
df.rename(columns={'Rqdpj': '青岛啤酒', 'Rmeidi': '美的', 'Rhksw': '华科生物', 'Rhryy': '恒瑞药业', 'Rxpp': '香飘飘'}, inplace=True)

df_m = df.mean() * 252
df_v = df.var() * 252
df_c = df.cov() * 252
df_corr = df.corr()
df_vol = df.std() * np.sqrt(252)
x = np.random.random(5)
weight = x / np.sum(x)
dfxxport = np.sum(weight * df_m)
v_p = np.sqrt(np.dot(weight, np.dot(df_c, weight.T)))

W = np.array([0.2] * 5)
df_mean = df.mean() * len(df.index)
df_cov = df.cov() * len(df.index)
r_df = np.dot(df_mean, W)
print('组合得到的期望收益率', r_df)
var_df = np.dot(W, df_cov)
var_df = np.dot(var_df, W.T)
sharp_ratio = r_df / var_df
print('夏普比率', sharp_ratio)

# 构建有限前沿
import scipy.optimize as sco


def f(w):  # 构建最优化函数
    w = np.array(w)
    Rp_opt = np.sum(w * df_m)
    Vp_opt = np.sqrt(np.dot(w, np.dot(df_c, w.T)))
    return np.array([Rp_opt, Vp_opt])


def Vmin_f(w):
    return f(w)[1]


cons = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
bnds = tuple((0, 1) for x in range(len(df_m)))
result = sco.minimize(Vmin_f, len(df_m) * [1.0 / len(df_m), ], method='SLSQP', bounds=bnds, constraints=cons)
print("投资组合预期收益率 10% 时香飘飘的权重", round(result['x'][0], 4))
print("投资组合预期收益率 10% 时青岛啤酒的权重", round(result['x'][1], 4))
print("投资组合预期收益率 10% 时美的的权重", round(result['x'][2], 4))
print("投资组合预期收益率 10% 时华科生物的权重", round(result['x'][3], 4))
print("投资组合预期收益率 10% 时恒瑞药业的权重", round(result['x'][4], 4))
plt.pie([round(result['x'][0], 4), round(result['x'][1], 4), round(result['x'][2], 4), round(result['x'][3], 4),
         round(result['x'][4], 4)], labels=["香飘飘", "青岛啤酒", "美的", "华科生物", "恒瑞药业"], explode=[0, 0, 0, 0, 0.2])
Rp_vmin = np.sum(df_m * result['x'])
Vp_vmin = result['fun']
print('波动率在可行集是全局最小值的投资组合预期收益率', round(Rp_vmin, 4))
print('在可行集是全局最小值的波动率', round(Vp_vmin, 4))

# 有效前沿的可视化（星号以上部分才是资本市场线）
Rp_target = np.linspace(-0.1, 0.6, 100)
Vp_target = []
for r in Rp_target:
    conss = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1}, {'type': 'eq', 'fun': lambda x: f(x)[0] - r})
    bndss = tuple((0, 1) for x in range(len(df_m)))
    result = sco.minimize(Vmin_f, len(df_m) * [1.0 / len(df_m), ], method='SLSQP', bounds=bndss, constraints=conss)
Vp_target.append(result['fun'])


def F(w):
    Rf = 0.02
    w = np.array(w)
    Rp_opt = np.sum(w * df_m)
    Vp_opt = np.sqrt(np.dot(w, np.dot(df_c, w.T)))
    SR = (Rp_opt - Rf) / Vp_opt
    return np.array([Rp_opt, Vp_opt, SR])


def SRmin_F(w):
    return -F(w)[2]


cons_SR = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
result_SR = sco.minimize(SRmin_F, len(df_m) * [1.0 / len(df_m), ], method='SLSQP', bounds=bnds, constraints=cons_SR)

Rf = 0.02
slope = -result_SR['fun']
Rm = np.sum(df_m * result_SR['x'])
Vm = (Rm - Rf) / slope
print('市场组合的预期收益率', round(Rm, 4))
print('市场组合的波动率', round(Vm, 4))

Rp_cml = np.linspace(0.02, 0.6)
Vp_cml = (Rp_cml - Rf) / slope
#plt.scatter(Vp, Rp, s=10)
plt.plot(Vp_target, Rp_target, 'r-', label=u'有效前沿', lw=2.5)
plt.plot(Vp_cml, Rp_cml, 'b--', label=u'资本市场线', lw=2.5)
plt.plot(Vp_vmin, Rp_vmin, 'b*', label=u'全局最小波动率', markersize=18)
plt.plot(Vm, Rm, 'g*', label=u'市场组合', markersize=14)
plt.xlabel(u'波动率', fontsize=24)
plt.ylabel(u'收益率', fontsize=24)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.xlim(0.15, 0.48)
plt.ylim(-0.1, 0.45)
plt.title(u'投资组合理论的可视化', fontsize=24)
plt.legend(fontsize=13)
plt.show()

