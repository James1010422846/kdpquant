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

data = pro.query('stock_basic', exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
data.to_excel('data.xlsx')
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
alldata.to_csv('all.csv')
print(alldata.head())
alldata.rename(columns={'qdpj': '青岛啤酒', 'meidi': '美的', 'hksw': '华科生物', 'hryy': '恒瑞药业', 'xpp': '香飘飘'}, inplace=True)
alldata.to_csv('allChinaTitle.csv')
