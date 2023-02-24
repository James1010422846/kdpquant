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

# 获取历史交易数据
def select(code):
    df = data.select_daily_stock(code)
    df['code'] = code
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
    return df
code = 'sh600519'

df = select(code)
df = df.dropna()
df = df.replace([np.inf, -np.inf], 0)
df300 = df
df300 = df300.set_index('date')

# 筛选出指数价格的极大值点
def find_max(stock_data, start_date, end_date):
    """
    :param stock_data: 需要筛选出极大值点的指数数据
    :param start_date: 筛选范围的开始日期
    :param end_date: 筛选范围的结束日期
    :return:返回极大值点对应当天数据
    """
    max_price = stock_data[start_date:end_date]['close'].max()    # 极大值点的收盘价
    return stock_data[stock_data['close'] == max_price]    # 极大值点对应当天数据


# 按月定投函数
def auto_invest_monthly(stock_data, start_date, end_date):
    """
    :param stock_data: 需要定投的指数数据
    :param start_date: 开始定投的日期
    :param end_date: 结束定投的日期
    :return: 返回从开始定投到结束每天的资金数据
    """
    # 截取股票数据
    stock_data = stock_data[start_date:end_date]

    # 修改stock_data的index的数据类型，这样才能和temp进行合并
    stock_data.index = stock_data.index.astype('period[D]')

    # 每月第一个交易日定投
    buy_month = stock_data.resample('M', kind='period').first()

    # 定投购买指数基金
    trade_log = pd.DataFrame(index=buy_month.index)
    trade_log['一手资金'] = buy_month['close'] %100*100  # 将收盘价除以1000作为基金净值
    trade_log['定投资金'] = 100000  # 每月投入1000元申购该指数基金
    trade_log['每次购买份额'] = trade_log['定投资金'] / trade_log['一手资金']  # 买入份额等于买入金额除以基金净值
    trade_log['持有份额'] = trade_log['每次购买份额'].cumsum()  # 累计申购份额
    trade_log['累计投入'] = trade_log['定投资金'].cumsum()  # 累计投入金额

    temp = trade_log.resample('D').ffill()  # 将交易记录填充为日级数据

    # 计算每个交易日的资产（等于当天的基金份额乘以单位基金净值）
    daily_data = pd.merge(stock_data, temp, left_index=True, right_index=True, how='left')
    daily_data = daily_data[['close', '定投资金', '每次购买份额', '持有份额', '累计投入']]
    daily_data['基金净值'] = daily_data['close']*100
    daily_data['持有基金价值'] = daily_data['close'] * daily_data['持有份额']

    # 将daily_data的index修改为datetime类型，否则无法使用matplotlib绘图
    daily_data.index = daily_data.index.astype('datetime64')

    return daily_data
# 每月定投沪深300指数
df300m = auto_invest_monthly(df300, '2007/10/16','2023/01/20' )


# 按周定投函数
def auto_invest_weekly(stock_data, start_date, end_date):
    """
    :param stock_data: 需要定投的指数数据
    :param start_date: 开始定投的日期
    :param end_date: 结束定投的日期
    :return: 返回从开始定投到结束每天的资金数据
    """
    # 截取股票数据
    stock_data = stock_data[start_date:end_date]

    # 修改stock_data的index的数据类型，这样才能和temp进行合并
    stock_data.index = stock_data.index.astype('period[D]')

    # 每周第一个交易日定投，如果整周都是休息日，则跳过本周
    buy_week = stock_data.resample('w', kind='period').first().dropna()

    # 定投购买指数基金
    trade_log = pd.DataFrame(index=buy_week.index)
    trade_log['一手资金'] = buy_week['close'] %100*100  # 将收盘价除以1000作为基金净值
    trade_log['定投资金'] = 200000  # 每月投入1000元申购该指数基金
    trade_log['每次购买份额'] = trade_log['定投资金'] / trade_log['一手资金']  # 买入份额等于买入金额除以基金净值
    trade_log['持有份额'] = trade_log['每次购买份额'].cumsum()  # 累计申购份额
    trade_log['累计投入'] = trade_log['定投资金'].cumsum()  # 累计投入金额

    temp = trade_log.resample('D').ffill()  # 将交易记录填充为日级数据

    # 计算每个交易日的资产（等于当天的基金份额乘以单位基金净值）
    daily_data = pd.merge(stock_data, temp, left_index=True, right_index=True, how='left')
    daily_data = daily_data[['close', '定投资金', '每次购买份额', '持有份额', '累计投入']]
    daily_data['基金净值'] = daily_data['close']*100
    daily_data['持有基金价值'] = daily_data['close'] * daily_data['持有份额']

    # 将daily_data的index修改为datetime类型，否则无法使用matplotlib绘图
    daily_data.index = daily_data.index.astype('datetime64')

    return daily_data
# 每周定投沪深300指数
df300w = auto_invest_weekly(df300, '2007/10/16', '2023/7/31')

df_300 = ak.stock_zh_index_daily_em(symbol="sh000300")
df_300['date'] = pd.to_datetime(df_300['date'], format='%Y-%m-%d')

# 合并两个数据表
df_merge = df300w.merge(df_300, how='inner', on='date')
print(df_merge)
# 将合并数据表的日期列改为时间格式
df_merge['date'] = pd.to_datetime(df_merge['date'], format='%Y-%m-%d')
target = (df_merge['持有基金价值']).pct_change()
# 将索引设置为日期列
target.index = df_merge['date']
# 基准策略收益率Series，计算方法相同
base = df_merge['close_x'].pct_change()
base.index = df_merge['date']
ic_analysis.qs_analysis(target,base)