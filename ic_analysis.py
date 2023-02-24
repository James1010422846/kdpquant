import pandas as pd
from alphalens.utils import get_clean_factor_and_forward_returns
from alphalens.tears import create_full_tear_sheet
import pyfolio as pf
import quantstats as qs
def ic_analysis(factor,close):
    # df = df.sort_values(by='date')
    # df.index = pd.to_datetime(df['date'])
    # df.index.name = None
    # df.sort_index(inplace=True)
    # # MultiIndex，level0为日期，level1为股票代码，assets为get_clean_factor_and_forward_returns所需的因子数据格式
    # assets = df.set_index([df.index, df['code']], drop=True)
    # # column为股票代码，index为日期，值为股票收盘价
    # close = df.pivot_table(index='date', columns='code', values='close')
    # close.index = pd.to_datetime(close.index)
    # 需要将pct_chg做shift处理，否则将使用未来数据
    #plan 1
    # ret = get_clean_factor_and_forward_returns(factor, close,max_loss=1.0,periods=(5,10,21))
    # create_full_tear_sheet(ret, long_short=True)
    #plan 2
    ret = get_clean_factor_and_forward_returns(factor, close,max_loss=1.0)
    create_full_tear_sheet(ret, long_short=True)
    return '分析结束'
def pf_analysis(strategy,benchmark_rets,date):
    '''
    def get_return(code):
        df = ts.get_k_data(code, start='2010-01-01')
        df.index = pd.to_datetime(df.date)
        return df.close.pct_change().fillna(0).tz_localize('UTC')

    ret = get_return('600519')
    benchmark_ret = get_return('sh')
    # 假设前面是模拟盘，2017年开始实盘买入600519并一直持有
    date = '2017-01-03'
    '''
    pf.create_full_tear_sheet(strategy, benchmark_rets=benchmark_rets,live_start_date=date)
    print('pf分析完成')
def qs_analysis(target,base):
    '''
    # 获取沪深300历史交易数据
    df_300 = ak.stock_zh_index_daily_em(symbol="sh000300")

    # 获取工商银行历史交易数据
    df = ak.stock_zh_a_hist(symbol="601398", adjust="hfq")
    # 将列名日期改为date，使其与df_300具备同名日期列
    df['date'] = df['日期']

    # 合并两个数据表
    df_merge = df.merge(df_300, how='inner', on='date')
    # 将合并数据表的日期列改为时间格式
    df_merge['date'] = pd.to_datetime(df_merge['date'] , format='%Y-%m-%d')

    # 目标策略收益率Series，pct_change的作用是根据价格计算收益率
    target = df_merge['收盘'].pct_change()
    # 将索引设置为日期列
    target.index = df_merge['date']
    # 基准策略收益率Series，计算方法相同
    base = df_merge['close'].pct_change()
    base.index = df_merge['date']
    '''
    # 输出网页格式的分析结果
    qs.reports.html(target, base, output='Output.html')