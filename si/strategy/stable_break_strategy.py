#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: Maple.S
@project: StockInsight
@time: 2021/5/22 14:21
@desc:
"""
import numpy as np

from si.strategy.base_strategy import BaseStrategy


def is_stable_window(quotes, cur_idx, window_threshold=10):
    from si.lib.ta_lib import moving_average
    idx = cur_idx

    while True:
        moving_average(quotes, cur_idx)


class StableBreakStrategy(BaseStrategy):
    def __init__(self, config):
        super().__init__(config)

        self.closeness_window = 20
        self.previous_window = 20

    def apply_strategy(self, quotes, cur_idx, **kwargs):
        # previous window recognize
        previous_window_quotes = quotes.iloc[
                                 cur_idx - self.previous_window - self.closeness_window: cur_idx - self.closeness_window]

        prev_low = previous_window_quotes['low'].min()

        # closeness window
        closeness_window_quotes = quotes.iloc[cur_idx - self.closeness_window: cur_idx]
        closeness_window_high = closeness_window_quotes['high'].max()

        closeness_window_avg_vol = closeness_window_quotes['volume'].mean()

        # current
        cur_quote = quotes.iloc[cur_idx]

        rules = [
            prev_low > closeness_window_high * 0.95,
            cur_quote['close'] > closeness_window_high,
            cur_quote['volume'] > closeness_window_avg_vol * 1.5,
            cur_quote['close'] > cur_quote.open
        ]

        if np.mean(rules) == 1.0:
            return True
        else:
            return False

    def get_context_length(self):
        return self.closeness_window + self.previous_window

    def get_future_length(self):
        return 0
