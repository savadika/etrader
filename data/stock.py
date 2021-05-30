from jqdatasdk import *
import pandas as pd
import datetime

auth('18806537016', '82593768')

# 设置行列不忽略
pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', 1000)

# 设置导出路径
export_root = 'E:/etrader/data/csv/'



def get_stock_list():
    """
    获取所有A股股票的代码列表
    @return: 股票代码列表
    上海证券交易所	.XSHG
    深圳证券交易所	.XSHE
    @rtype: list
    """
    stock_lists = get_all_securities(['stock']).index
    return stock_lists


def get_single_stock(code, startdate, enddate, per_fre='daily'):
    """
    获取单个股票的行情数据
    :param code: 股票代码
    :param startdate: 开始时间
    :param enddate: 结束时间
    :param per_fre: 默认是天
    :return: 单个股票的行情数据
    :rtype: dataframe
    """
    single_data = get_price(
        code,
        start_date=startdate,
        end_date=enddate,
        frequency=per_fre)
    # 为首条数据添加表头
    single_data.index.names = ['date',]
    return single_data


def export_data(data, type, save_name):
    """
    导出行情数据
    @param data: 股票的dataframe 数据
    @type data: dataframe
    @param type: 导出的数据的类型
    @type type:  price 价格数据,securities 行情数据,fundamentals 财务数据
    @param save_name: 保存名称
    @type save_name: str
    @return: csv
    @rtype: csv
    """
    save_root = export_root + type + '/' + save_name + '.csv'
    data.to_csv(save_root)
    print('已成功导出', save_root)


def transfer_price_freq(data, time_freq='W'):
    """
    将日K转换为周K数据
    @param data: 传入的dataframe数据
    @type data: dataframe
    @param time_freq: 需要转换成的周期
    @type time_freq: w（星期）
    @return: 转换后的周期
    @rtype: dataframe
    """
    df_trans = pd.DataFrame()
    df_trans['open'] = data['open'].resample(time_freq).first()
    df_trans['close'] = data['close'].resample(time_freq).last()
    df_trans['high'] = data['high'].resample(time_freq).max()
    df_trans['low'] = data['low'].resample(time_freq).min()
    return df_trans


def get_single_finance(code, date, statDate):
    """
    获取单个股票的财务指标
    @param code: 股票代码
    @type code: str
    @param code: 查询日期
    @type code: str
    @param statDate:  季度或者年度时间
    @type statDate:
    @return: 股票的财务指标
    @rtype: dataframe
    """
    df = get_fundamentals(query(indicator).filter(indicator.code == code), date=date, statDate=statDate)
    return df


def get_single_valuation(code, date, statDate):
    """
    获取单个股票的估值数据
    @param code: 股票代码
    @type code: str
    @param date:查询时间
    @type date: str
    @param statDate:季度或者季度时间
    @type statDate: str
    @return: 估值数据
    @rtype: dataframe
    """
    df = get_fundamentals(query(valuation).filter(valuation.code == code), date=date, statDate=statDate)
    return df




"""
财务指标
code	股票代码	带后缀.XSHE/.XSHG
pubDate	日期	公司发布财报日期
statDate	日期	财报统计的季度的最后一天, 比如2015-03-31, 2015-06-30
*eps	每股收益EPS(元)	每股收益(摊薄)＝净利润/期末股本；分子从单季利润表取值，分母取季度末报告期股本值。
adjusted_profit	扣除非经常损益后的净利润(元)	非经常性损益这一概念是证监会在1999年首次提出的，当时将其定义为：公司正常经营损益之外的一次性或偶发性损益。《问答第1号》则指出：非经常性损益是公司发生的与经营业务无直接关系的收支；以及虽与经营业务相关，但由于其性质、金额或发生频率等方面的原因，影响了真实公允地反映公司正常盈利能力的各项收入。
*operating_profit	经营活动净收益(元)	营业总收入-营业总成本
value_change_profit	价值变动净收益(元)	公允价值变动净收益+投资净收益+汇兑净收益
**roe	净资产收益率ROE(%)	归属于母公司股东的净利润*2/（期初归属于母公司股东的净资产+期末归属于母公司股东的净资产）
inc_return	净资产收益率(扣除非经常损益)(%)	扣除非经常损益后的净利润（不含少数股东损益）*2/（期初归属于母公司股东的净资产+期末归属于母公司股东的净资产）
roa	总资产净利率ROA(%)	净利润*2/（期初总资产+期末总资产）
net_profit_margin	销售净利率(%)	净利润/营业收入
gross_profit_margin	销售毛利率(%)	毛利/营业收入
expense_to_total_revenue	营业总成本/营业总收入(%)	营业总成本/营业总收入(%)
operation_profit_to_total_revenue	营业利润/营业总收入(%)	营业利润/营业总收入(%)
net_profit_to_total_revenue	净利润/营业总收入(%)	净利润/营业总收入(%)
operating_expense_to_total_revenue	营业费用/营业总收入(%)	营业费用/营业总收入(%)
ga_expense_to_total_revenue	管理费用/营业总收入(%)	管理费用/营业总收入(%)
financing_expense_to_total_revenue	财务费用/营业总收入(%)	财务费用/营业总收入(%)
operating_profit_to_profit	经营活动净收益/利润总额(%)	经营活动净收益/利润总额(%)
invesment_profit_to_profit	价值变动净收益/利润总额(%)	价值变动净收益/利润总额(%)
adjusted_profit_to_profit	扣除非经常损益后的净利润/归属于母公司所有者的净利润(%)	扣除非经常损益后的净利润/归属于母公司所有者的净利润(%)
goods_sale_and_service_to_revenue	销售商品提供劳务收到的现金/营业收入(%)	销售商品提供劳务收到的现金/营业收入(%)
ocf_to_revenue	经营活动产生的现金流量净额/营业收入(%)	经营活动产生的现金流量净额/营业收入(%)
ocf_to_operating_profit	经营活动产生的现金流量净额/经营活动净收益(%)	经营活动产生的现金流量净额/经营活动净收益(%)
inc_total_revenue_year_on_year	营业总收入同比增长率(%)	营业总收入同比增长率是企业在一定期间内取得的营业总收入与其上年同期营业总收入的增长的百分比，以反映企业在此期间内营业总收入的增长或下降等情况。
inc_total_revenue_annual	营业总收入环比增长率(%)	营业收入是指企业在从事销售商品，提供劳务和让渡资产使用权等日常经营业务过程中所形成的经济利益的总流入。环比增长率=（本期的某个指标的值-上一期这个指标的值）/上一期这个指标的值*100%。
inc_revenue_year_on_year	营业收入同比增长率(%)	营业收入,是指公司在从事销售商品、提供劳务和让渡资产使用权等日常经营业务过程中所形成的经济利益的总流入，而营业收入同比增长率，则是检验上市公司去年一年挣钱能力是否提高的标准，营业收入同比增长,说明公司在上一年度挣钱的能力加强了，营业收入同比下降，则说明公司的挣钱能力稍逊于往年。
inc_revenue_annual	营业收入环比增长率(%)	环比增长率=（本期的某个指标的值-上一期这个指标的值）/上一期这个指标的值*100%。
*inc_operation_profit_year_on_year	营业利润同比增长率(%)	同比增长率就是指公司当年期的净利润和上月同期、上年同期的净利润比较。（当期的利润-上月（上年）当期的利润）/上月（上年）当期的利润=利润同比增长率。
inc_operation_profit_annual	营业利润环比增长率(%)	环比增长率=（本期的某个指标的值-上一期这个指标的值）/上一期这个指标的值*100%。
inc_net_profit_year_on_year	净利润同比增长率(%)	（当期的净利润-上月（上年）当期的净利润）/上月（上年）当期的净利润绝对值=净利润同比增长率。
inc_net_profit_annual	净利润环比增长率(%)	环比增长率=（本期的某个指标的值-上一期这个指标的值）/上一期这个指标的值*100%。
inc_net_profit_to_shareholders_year_on_year	归属母公司股东的净利润同比增长率(%)	归属于母公司股东净利润是指全部归属于母公司股东的净利润，包括母公司实现的净利润和下属子公司实现的净利润；同比增长率，一般是指和去年同期相比较的增长率。同比增长 和上一时期、上一年度或历史相比的增长（幅度）。
inc_net_profit_to_shareholders_annual	归属母公司股东的净利润环比增长率(%)	环比增长率=（本期的某个指标的值-上一期这个指标的值）/上一期这个指标的值*100%。
"""




# 作业1 计算茅台当天市值
# current_close = get_price(
#     '600519.XSHG',
#     start_date=datetime.datetime.today(),
#     end_date=datetime.datetime.today())
# maotai_close = current_close['close'][0]
#
# # 查询茅台总股本
# q = query(valuation.capitalization).filter(valuation.code == '600519.XSHG')
# cp_total = get_fundamentals(q, date=datetime.datetime.now())
# maotai_total = cp_total['capitalization'][0]
#
# print(maotai_total * maotai_total)
#
# # 问题1： serials对象  和 dataframe 对象如何取值
# #  serials   current_close['close'][0]
# #  dataframe   cp_total['capitalization'][0]
#
# #  计算贵州茅台的市盈率
#
# q1 = query(valuation.pe_ratio).filter(valuation.code == '600519.XSHG')
# current_pe = get_fundamentals(q1, date=datetime.datetime.today())
# print(current_pe['pe_ratio'][0])
