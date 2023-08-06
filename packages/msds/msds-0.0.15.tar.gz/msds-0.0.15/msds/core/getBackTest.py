import os
import click
import pandas as pd
from rich import print
from msds.func.Position import *
from msds.func.Evaluate import *
from msds.base.util import makedirs
from msds.base.data import dataClean, timeConversion, timeFilter
from rich.progress import Progress

pd.set_option('expand_frame_repr', False)  # 当列太多时不换行

def go_back_test(strategy, testData, testSymbol):
    '''历史收益回测'''
    # 读入数据并整理
    df = dataClean(pd.read_hdf(testData.get('data_path'), key='df'))
    # 转换K线数据周期
    df = timeConversion(df, testData.get('strategy_time'))
    # 根据时间段进行过滤
    df = timeFilter(df, testData.get('time_start'), testData.get('time_end'))
    # 获取策略参数
    param = strategy.testParam()

    # 单个参数的策略收益
    if not type(param[0]) == list:
        result = computeEquity(df, strategy.test, param, testSymbol)
        return print('策略最终收益：', result)

    # 策略组合的收益数据
    rtn = pd.DataFrame()
    with Progress() as progress:
        myTask = progress.add_task('[bold green]【回测进度】: ', total=len(param))
        for item in param:
            result = computeEquity(df, strategy.test, item, testSymbol)
            rtn.loc[str(item), 'equity_curve'] = result
            progress.update(myTask, advance=1)
        progress.update(myTask, visible=False)
        print('[bold green]数据整理中...')
        rtn.sort_values(by='equity_curve', ascending=False, inplace=True)
    click.clear()
    print(rtn)
    absolute_path = os.path.join(os.getcwd(), 'result')
    makedirs(absolute_path)
    rtn.to_csv(os.path.join(absolute_path, 'result.csv'))

def computeEquity(df, strategy, param, testSymbol):
    '''资产信息计算'''
    _df = df.copy()
    # 计算信号 signal 信息
    _df = strategy(_df, param)
    # 获取持仓 pos 信息
    _df = position_for_OKEx_future(_df)
    # 获取实际持仓信息
    _df = equity_curve_for_OKEx_USDT_future_next_open(
        _df,
        slippage=testSymbol.getfloat('slippage'),
        c_rate=testSymbol.getfloat('service_charge'),
        leverage_rate=testSymbol.getint('leverage_rate'),
        face_value=testSymbol.getint('symbol_face_value'),
        min_margin_ratio=testSymbol.getfloat('min_margin_ratio')
    )
    return _df.iloc[-1]['equity_curve']