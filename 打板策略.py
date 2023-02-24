import akshare as ak
import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import mplfinance as mpf
from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文字体为微软雅
plt.rcParams['font.sans-serif'] = ['SimHei']        # 字体设置
import matplotlib
matplotlib.rcParams['axes.unicode_minus']=False    # 负号显示问题

#获取最大涨幅板块
ind = ak.stock_board_industry_name_em()
bk = ind.sort_values('涨跌幅',ascending=False)['板块名称'][0]

#获得板块股票池
stock_pool= ak.stock_board_industry_cons_em(symbol=bk)

end =datetime.now().strftime('%Y%m%d')
#end = '20230217'
stock_zt_pool_em_df = ak.stock_zt_pool_em(date=end)
stock_pool= stock_zt_pool_em_df[(stock_zt_pool_em_df['所属行业']==bk)]
stock_hot_rank_wc_df = ak.stock_hot_rank_wc(date=end)
stock_hot_rank_wc_df.rename(columns= {'股票代码':'代码'},inplace=True)


stock_hot_rank_wc_df = stock_hot_rank_wc_df[(stock_hot_rank_wc_df['代码']==stock_pool.iloc[0,1])]
stock_pool = pd.merge(stock_pool,stock_hot_rank_wc_df,on='代码')
print(stock_pool)