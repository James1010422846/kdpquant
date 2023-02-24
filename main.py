# 这是一个示例 Python 脚本。

# 按 Shift+F10 执行或将其替换为您的代码。
# 按 双击 Shift 在所有地方搜索类、文件、工具窗口、操作和设置。


import akshare as ak
import requests
import json
import pandas as pd
import threading
import akshare as ak
from datetime import datetime
from tqdm import tqdm
from sqlalchemy import create_engine
import warnings

warnings.filterwarnings("ignore")
# 写入数据
engine = create_engine('mysql+pymysql://root:888@106.15.1.22:3306/1min')

now_date_str = str(datetime.now())[:10]
now_date = ''.join(str(datetime.now())[:10].split('-'))


def get_all_stock_code():
    '''
    获取全部股票代码
    '''
    df = ak.stock_zh_a_spot()
    # df=ak.stock_individual_fund_flow_rank(indicator='今日')
    df1 = df['代码']
    return df1


def get_stock_min_em(stock='sh600031'):
    '''
    获取股票分钟数据
    '''
    data = ak.stock_zh_a_minute(symbol=stock, period='1', adjust="qfq")
    print(stock)
    data.to_sql(name=stock, con=engine, index=False, if_exists='replace')
    return data


def down_all_data():
    # 线程池
    threading_list = []
    all_code = get_all_stock_code()
    # print(all_code.head())
    code_list = all_code
    # code_list=all_code['代码'].to_list()
    i=1
    for stock in code_list[4594:]:
        print(i/len(code_list[4594:]))
        print(i)
        get_stock_min_em(stock)
        i+=1
    # for stock in code_list:
    #     threading_list.append(threading.Thread(target=get_stock_min_em, args=(stock,)))
    # # 线程启动
    # for down in threading_list:
    #     down.start()
    # # join就是阻塞，主进程有join，主进程下面的代码一律不执行，直到进程执行完毕之后，再执行。
    # for down in threading_list:
    #     down.join()




# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    down_all_data()
    # df = ak.stock_zh_a_spot()
    # df1 = df['代码']
    # print(df1[4594:])
# 访问 https://www.jetbrains.com/help/pycharm/ 获取 PyCharm 帮助
