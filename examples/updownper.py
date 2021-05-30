# coding=utf-8
# 测试000001.XSHE 在某段 时间内的 涨跌幅

import data.stock as st

# 定义获取某只股票每日涨跌幅的函数
def calculate_change_prc(code, startdate, enddate, per_fre):
    """

    @param code: 股票代码
    @type code: str
    @param startdate:开始时间
    @type startdate: str
    @param enddate:结束时间
    @type enddate: str
    @param per_fre:频率
    @type per_fre: str
    @return:当只股票的行情数据
    @rtype: dataframe
    """
    current_data = st.get_single_stock(code= code, startdate = startdate ,enddate =enddate,per_fre=per_fre)
    current_data['per_change'] = (current_data['close'] - current_data['close'].shift(1)) / current_data['close']
    return current_data



# 主函数调用显示涨跌幅
if __name__ == '__main__':
    mydata = calculate_change_prc('000001.XSHE', '2021-01-01', '2021-03-01', 'daily')
    print(mydata)

