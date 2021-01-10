#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: Maple.S
@project: StockInsight
@time: 2021/1/9 21:52
@desc:
"""
import numpy as np

from si.lib.ta_lib import moving_average, exp_moving_average
from si.strategy.base_strategy import BaseStrategy


class BigSpikeStrategy(BaseStrategy):
    """
    Find the quotes that experience a series big spike.
    """

    def __init__(
            self,
            config
    ):
        super(BigSpikeStrategy, self).__init__(config)
        strategy_config = config['strategy']['bigspike']
        self.ob_window = strategy_config['ob_window']
        self.rule_3_volume = strategy_config['rule_3_volume']
        self.rule_8_horizon = strategy_config['rule_8_horizon']
        self.rule_8_volume_multiple = strategy_config['rule_8_volume_multiple']

    @property
    def context_length(self):
        return self.ob_window

    @property
    def future_length(self):
        return self.rule_8_horizon

    def apply_strategy(self, quotes, cur_idx, **kwargs):
        # price on spike day above {ob_window} day price high.
        rule_2 = quotes.iloc[cur_idx].close > np.max(quotes.iloc[cur_idx - self.ob_window:cur_idx].high)

        # 50 day volume moving average is less than 300000.
        rule_3 = quotes['volume'].iloc[cur_idx - self.ob_window: cur_idx].mean() < self.rule_3_volume

        # closing price on spike day is above the opening price on the same day.
        rule_4 = quotes.iloc[cur_idx]['close'] > quotes.iloc[cur_idx]['open']

        # closing price on spike day is above the closing price on the day before the spike.
        rule_5 = quotes.iloc[cur_idx]['close'] > quotes.iloc[cur_idx - 1]['close']

        # volume after the spike is at least three times the volume traded the day before the spike.
        rule_8 = (moving_average(quotes['volume'], cur_idx + self.rule_8_horizon, self.rule_8_horizon) >
                  moving_average(quotes['volume'], cur_idx - 1, self.rule_8_horizon) * self.rule_8_volume_multiple)

        rule_9 = (exp_moving_average(quotes['volume'], cur_idx, self.ob_window) <
                  moving_average(quotes['volume'], cur_idx, self.ob_window) * 1.5)

        # apply rules
        result = rule_2 & rule_3 & rule_4 & rule_5 & rule_8 & rule_9

        return result
