import data
import ic_analysis

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']        # 字体设置
import matplotlib
matplotlib.rcParams['axes.unicode_minus']=False    # 负号显示问题
code = 'bj430047'
df = data.select_min_stock(code)
df['instrument'] = code
code2 = 'bj430090'
df2 = data.select_min_stock(code2)
df2['instrument'] = code2
df = df2.append(df)
print(df.head())
df['day'] = df['day'].apply(lambda x:str(x)[:10])
def cal_single_df(df):
    #df["date_index"] = df["day"]
    def handle_factor(df):
        minute_df = df
        # def convert_period(bars, period='60s'):
        #     bars = bars.set_index('date')
        #     nbars = pd.DataFrame()
        #     nbars['open'] = bars['price'].resample(rule=period).first()
        #     nbars['high'] = bars['price'].resample(rule=period).max()
        #     nbars['low'] = bars['price'].resample(rule=period).min()
        #     nbars['close'] = bars['price'].resample(rule=period).last()
        #     nbars['1m_amount'] = bars['amount'].resample(rule=period).sum()
        #     nbars['1m_num_trades'] = bars['num_trades'].resample(rule=period).sum()
        #     return nbars[nbars['1m_amount'] > 0]
        #
        # minute_df = convert_period(df, period='60s')
        minute_df['ret'] = minute_df['close'].pct_change()
        Var = minute_df.ret.dropna().var()  # 收益率方差
        Skew = minute_df.ret.dropna().skew()  # 收益率峰度
        Kurt = minute_df.ret.dropna().kurt()  # 收益率偏度

        # # 平均单笔成交金额
        # AmtPerTrd = minute_df['1m_amount'].sum() / minute_df['1m_num_trades'].sum()
        # # 平均单笔流入金额
        # AmtPerTrd_InFlow = minute_df[minute_df['ret'] > 0]['1m_amount'].sum() / minute_df[minute_df['ret'] > 0][
        #     '1m_num_trades'].sum()
        # # 平均单笔流出金额
        # AmtPerTrd_OutFlow = minute_df[minute_df['ret'] < 0]['1m_amount'].sum() / minute_df[minute_df['ret'] < 0][
        #     '1m_num_trades'].sum()
        #
        # AmtPerTrd_InFlow_ratio = AmtPerTrd_InFlow / AmtPerTrd  # 平均单笔流入金额占比
        # AmtPerTrd_OutFlow_ratio = AmtPerTrd_OutFlow / AmtPerTrd  # 平均单笔流出金额占比
        # minute_df['1m_AmtPerTrd'] = minute_df['1m_amount'] / minute_df['1m_num_trades']
        # bigorder_df = minute_df.sort_values('1m_AmtPerTrd', ascending=False).head(int(336 * 0.1))
        #
        # # 大单资金净流入金额
        # Amt_netInFlow_bigOrder = bigorder_df[bigorder_df['ret'] > 0]['1m_amount'].sum() - \
        #                          bigorder_df[bigorder_df['ret'] < 0]['1m_amount'].sum()
        # # 大单资金净流入率
        # Amt_netInFlow_bigOrder_ratio = Amt_netInFlow_bigOrder / minute_df['1m_amount'].sum()
        # # 大单驱动涨幅
        # Mom_bigOrder = (bigorder_df['ret'].dropna() + 1).prod()

        return pd.DataFrame(
            { 'Var': [Var], 'Skew': [Skew], 'Kurt': [Kurt]})

    factor_df = df.groupby(['day', 'instrument']).apply(handle_factor).reset_index()
    return factor_df

print(cal_single_df(df))
