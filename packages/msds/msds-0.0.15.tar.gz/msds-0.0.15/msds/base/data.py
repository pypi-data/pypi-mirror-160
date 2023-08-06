import pandas as pd

def dataClean(df):
    '''常规整理：任何原始数据读入都进行一下去重、排序、索引重置，以防万一'''
    df.drop_duplicates(subset=['candle_begin_time'], keep='last', inplace=True)
    df.sort_values(by=['candle_begin_time'], inplace=True)
    df.reset_index(inplace=True, drop=True)
    return df

def timeConversion(df, rule_type):
    ''' 数据时间间隔转化
    1、进行重新采样
    2、对数值根据规则进行聚合
    3、根据open列去除没有交易的周期
    4、去除成交量为0的交易周期
    '''
    result = df.resample(
        rule=rule_type,
        on='candle_begin_time',
        label='left',
        closed='left'
    ).agg({
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
        'volume': 'sum'
    })
    result.dropna(subset=['open'], inplace=True)
    result = result[result['volume'] > 0]
    result.reset_index(inplace=True)
    return result

def timeFilter(df, time_start, time_end):
    '''数据时间过滤'''
    df = df[df['candle_begin_time'] >= pd.to_datetime(time_start)]
    df = df[df['candle_begin_time'] < pd.to_datetime(time_end)]
    df.reset_index(inplace=True, drop=True)
    return df