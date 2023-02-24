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
import statsmodels.api as sm
from sklearn.model_selection import train_test_split
import  warnings
warnings.filterwarnings('ignore')
import tqdm
def mad(factor):
    """3倍中位数去极值
    """
    # 求出因子值的中位数
    med = np.median(factor)
    # 求出因子值与中位数的差值，进行绝对值
    mad = np.median(np.abs(factor - med))
    # 定义几倍的中位数上下限
    high = med + (3 * 1.4826 * mad)
    low = med - (3 * 1.4826 * mad)
    # 替换上下限以外的值
    factor = np.where(factor > high, high, factor)
    factor = np.where(factor < low, low, factor)
    #print('mad',factor)
    return factor

def stand(factor):
    """
    自实现标准化
    """
    mean = factor.mean()
    std = factor.std()
    #print(mean)
    return (factor - mean) / std


def select(code):
    df = data.select_daily_stock(code)
    df['code'] = code
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
    return df

engine = create_engine('mysql+pymysql://root:888@106.15.1.22:3306/akshare-price-hfq')
conn = engine.connect()
sql_query = "show tables "
code_list = pd.read_sql(sql_query, engine)

def fac(df):
    #df['fac1'] = -df.close.shift(1).pct_change().cumsum()
    df['fac1'] = (0.5*np.sqrt(1+df.close.pct_change())).shift(1)
    #df['fac2'] = (-df.low.rolling(20).min().shift(1))


    #df['fac1'] = df['fac7']
    df['fac1'].fillna(0,inplace=True)
    #df['fac1'] =df['fac1'].shift(1)
    #df['fac1'] = (1/df['fac1']).shift(1)
    #df['fac1'].fillna(0, inplace=True)
    return stand(mad(df['fac1']))
    #return df['fac1']
df = pd.DataFrame()
for i in tqdm.tqdm(code_list['Tables_in_akshare-price-hfq'][6:]):
    print(i)
    df2 = select(i)
    df2 = df2.dropna()
    df2 = df2.replace([np.inf, -np.inf], 0)
    df2['fac'] = fac(df2)
    df =df.append(df2)
df = df.sort_values(by='date')
df.index = pd.to_datetime(df['date'])
df.index.name = None
df.sort_index(inplace=True)
# MultiIndex，level0为日期，level1为股票代码，assets为get_clean_factor_and_forward_returns所需的因子数据格式
assets = df.set_index([df.index, df['code']], drop=True)
#assets['turnover'] = assets['turnover'].shift(1)
# column为股票代码，index为日期，值为股票收盘价
close = df.pivot_table(index='date', columns='code', values='close')
close.index = pd.to_datetime(close.index)

ic_analysis.ic_analysis(assets[['fac']], close)