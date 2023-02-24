
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


# 投资优化组合可视化.py
df = pd.read_csv("R.csv", index_col='date', parse_dates=['date'])[
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
