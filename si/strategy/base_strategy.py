#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: Maple.S
@project: StockInsight
@time: 2021/1/10 17:51
@desc:
"""
from abc import abstractmethod, ABC
import numpy as np


class BaseStrategy(ABC):

    def __init__(self, config):
        self.base_filter_config = config['base_filter']

    def forward(self, quotes, cur_idx, **kwargs):
        """

        Args:
            quotes:
            cur_idx:
            **kwargs:

        Returns:

        """
        if self.filter_quotes(quotes, cur_idx, **kwargs) and self.apply_strategy(quotes, cur_idx, **kwargs):
            return True
        else:
            return False

    def filter_quotes(self, quotes, cur_idx, **kwargs):
        ob_window = self.base_filter_config['ob_window']
        min_price = self.base_filter_config['min_price']
        min_volume = self.base_filter_config['min_volume']

        start_idx = cur_idx - ob_window

        if start_idx < 0:
            return False

        # filter price
        period_quotes = quotes.iloc[start_idx: cur_idx]

        if np.min(period_quotes.low) < min_price:
            return False

        # filter volume
        if np.mean(period_quotes.volume) < min_volume:
            return False

        return True

    @abstractmethod
    def apply_strategy(self, quotes, cur_idx, **kwargs):
        pass

    @abstractmethod
    def context_length(self):
        pass

    @abstractmethod
    def future_length(self):
        pass
