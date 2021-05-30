# coding=utf-8
# author:ylf
# contact: ylf8708@126.com
# datetime:2021/5/30 20:53

"""
文件说明：
每周买卖策略（根据周一买，周四卖的策略进行选股，并剔除掉不正常的交易信号，同时进行交易信号的整合）
"""
import data.stock as  st
import numpy as np

def week_period_strategy(code, starttime, end_time, freq):
    # 获取股票数据
    data = st.get_single_stock(code=code, startdate=starttime, enddate=end_time, per_fre=freq)
    # index的设置有点问题，无法读取到
    data['week_day'] = data.index.weekday
    # 只取部分的data
    data = data[['open', 'close', 'week_day']]
    # 根据时间生成交易信号
    data['buy_signal'] = np.where((data['week_day'] == 0) | (data['week_day'] == 1), 1, 0)
    data['sell_signal'] = np.where((data['week_day'] == 3) | (data['week_day'] == 4), -1, 0)
    # 排除交易信号的异常情况(目前的情况比较单一，还没有完全解决)
    # 2  剔除掉第二次出现的交易信号
    data['buy_signal'] = np.where((data['buy_signal'] == 1) & (data['buy_signal'].shift(1) == 1), 0, data['buy_signal'])
    data['sell_signal'] = np.where((data['sell_signal'] == -1) & (data['sell_signal'].shift(1) == -1), 0, data['sell_signal'])
    data['singal'] = data['buy_signal']+data['sell_signal']
    # 生成合并后正常的交易信号
    return data


if __name__ == '__main__':
    current_data = week_period_strategy('000001.XSHE', '2021-01-01', '2021-03-01', 'daily')
    print(current_data)












