#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from rich import print
'''
路径: ROOT_PATH: 当前文件main.py所处的位置上一层
作用: 将该路径加入到系统路径中, 保证其它的python文件能够互相通过模块的方式引入
注意: 当全局安装了msds这个包, 但是通过开发的方式运行当前文件时, 其它文件使用模块引入时, 会优先选择引入的是全局的模块
'''
ROOT_PATH = os.path.join(sys.path[0], '../')
sys.path.append(ROOT_PATH)

import click
import shutil
import importlib
import configparser
from msds.interact import interact
from msds.core.getBackTest import go_back_test
from msds.core.getCandleData import save_spot_candle_data_from_exchange

'''
作用: 读取代码实际运行时（使用工具的人执行时）路径下的配置文件
'''
config = configparser.ConfigParser()
config.read([os.path.join(os.getcwd(), 'msds.ini')])

# ------------------------------ 命令定义 ------------------------------
@click.group()
def msds():
    pass

@msds.command()
def init():
    TEMPLATE_FILE = [{
        'origin': 'msds/template/strategy.py',
        'target': 'strategy.py'
    }, {
        'origin': 'msds/template/__init__.py',
        'target': '__init__.py'
    }, {
        'origin': 'msds/template/msds.ini.py',
        'target': 'msds.ini'
    }]
    for i in TEMPLATE_FILE:
        origin_file = os.path.join(sys.path[-2], i['origin'])
        target_file = os.path.join(os.getcwd(), i['target'])
        if not os.path.exists(origin_file):
            print('[bold red]模板文件丢失: ' + origin_file + '[/bold red]')
            continue
        if not os.path.exists(target_file):
            shutil.copyfile(origin_file, target_file)
            print('[bold green]初始化文件成功: ' + target_file + '[/bold green]')

@msds.command()
def data():
    if not bool(config.has_section('CANDLE_DATA')):
        exchange, symbol, time_start, time_end, time_interval = interact.userAnswerData()
        save_spot_candle_data_from_exchange(exchange, symbol, time_start, time_end, time_interval)
    candleConfig = config['CANDLE_DATA']
    return save_spot_candle_data_from_exchange(
        candleConfig['exchange'],
        candleConfig['symbol'],
        candleConfig['time_start'],
        candleConfig['time_end'],
        candleConfig['time_interval']
    )

@msds.command()
def backtest():
    if not bool(config.has_section('BACK_TEST_DATA') and config.has_section('BACK_TEST_SYMBOL')):
        return

    # 策略文件引入
    strategy_name = config['BACK_TEST_DATA'].get('strategy_name') or 'main'
    strategy_path = config['BACK_TEST_DATA'].get('strategy_path') or os.getcwd()
    sys.path.append(strategy_path)
    strategy = importlib.import_module(strategy_name)

    go_back_test(
        strategy,
        config['BACK_TEST_DATA'],
        config['BACK_TEST_SYMBOL']
    )

@msds.command()
def test():
    pass

# ------------------------------ 服务入口 ------------------------------

def main():
    msds()

# 描述: 只有脚本执行的方式时运行main函数
# case1、当该模块被直接执行时: __name__ 等于文件名（包含后缀 .py ）
# case2、当该模块 import 到其他模块中:  __name__ 等于模块名称（不包含后缀.py）
if __name__ == '__main__':
    main()
