import ipywidgets as wd

import akshare as ak

import chart_studio
import cufflinks as cf
import pandas as pd
import yfinance as yf
from plotly.offline import iplot,init_notebook_mode
from ipywidgets import interact, interact_manual
init_notebook_mode()
import plotly.io as pio
pio.renderers.default='notebook'

df= ak.stock_zh_a_hist(symbol='600309', period="daily", start_date="19900301", end_date='20211201', adjust="")
df['日期'] = pd.to_datetime(df['日期'], format='%Y-%m-%d')
df.rename(columns= {'开盘':'open','最高':'high','最低':'low','收盘':'close','成交量':'volume'},inplace=True)
df.set_index('日期')
df.index.name = None

qf = cf.QuantFig(df,
                title=f'TA Dashboard ',
                legend = 'right')
qf.iplot()
