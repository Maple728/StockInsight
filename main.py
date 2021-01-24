#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: Maple.S
@project: StockInsight
@time: 2021/1/9 19:42
@desc:
"""
import argparse
import yaml

from si.lib.db_operation import DBService
from si.strategy.bigspike_strategy import BigSpikeStrategy
from si.strategy_runner import StrategyRunner


def main(args):
    # read config
    config_filename = args.config_filename
    with open(config_filename) as config_file:
        config = yaml.load(config_file, Loader=yaml.FullLoader)

    # run strategy
    strategy = BigSpikeStrategy(config)
    runner = StrategyRunner(strategy, config)
    runner.back_test(past_ob_window=100, future_window=20)
    # runner.run(past_ob_window=5)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    config_name = 'config/local.yaml'
    parser.add_argument('--config_filename', default=config_name, type=str, required=False,
                        help='Configuration filename')
    args = parser.parse_args()
    main(args)
