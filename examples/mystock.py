# coding=utf-8
# 存储股票数据

import data.stock as st


code = '000001.XSHE'
data = st.get_single_stock(code=code, startdate='2020-01-01', enddate='2021-01-01')
print(data)
st.export_data(data=data, type='price', save_name=code)
