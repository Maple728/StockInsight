#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: Maple.S
@project: StockInsight
@time: 2021/1/10 18:25
@desc:
"""
import numpy as np

from si.lib.db_operation import DBService


class StrategyRunner(object):

    def __init__(self, strategy, config):
        data_config = config['data']
        self.db = DBService(database=data_config['database'], user=data_config['user'],
                            password=data_config['password'],
                            host=data_config['host'], port=data_config['port'])
        self.strategy = strategy

    def back_test(self, past_ob_window, future_window, **kwargs):

        # connect db
        self.db.connect()

        for company, quotes in self.db.get_all_company_quotes_iterator():
            symbol = company['symbol']
            len_quotes = len(quotes)
            start_idx = max(len_quotes - past_ob_window - future_window, 0)
            end_idx = max(len_quotes - future_window, 0)
            for idx in range(start_idx, end_idx):
                if self.strategy.forward(quotes, idx, **kwargs):
                    cur_quote = quotes.iloc[idx]
                    profit = self.profit(quotes, idx, future_window)
                    print(f"Ticker: {symbol}, Date: {cur_quote['quote_date']:.0f}, Profit: {profit}")

        # close db
        self.db.close_db()

        return

    def run(self, **kwargs):
        # connect db
        self.db.connect()

        for company, quotes in self.db.get_all_company_quotes_iterator():
            past_ob_window = 5
            future_window = self.strategy.future_length

            symbol = company['symbol']
            len_quotes = len(quotes)
            start_idx = max(len_quotes - past_ob_window - future_window, 0)
            end_idx = max(len_quotes - future_window, 0)
            for idx in range(start_idx, end_idx):
                if self.strategy.forward(quotes, idx, **kwargs):
                    cur_quote = quotes.iloc[idx]
                    print(f"Ticker: {symbol}, Date: {cur_quote['quote_date']:.0f}")

        # close db
        self.db.close_db()

        return

    def profit(self, quotes, signal_idx, future_window):
        entry_price = quotes.iloc[signal_idx + 1]['open']
        window_quotes = quotes.iloc[signal_idx: signal_idx + future_window]
        min_price = np.min(window_quotes['low'])
        max_price = np.max(window_quotes['high'])
        last_price = quotes.iloc[signal_idx + future_window]['open']

        low_roi = (min_price / entry_price) - 1
        high_roi = (max_price / entry_price) - 1
        hold_roi = (last_price / entry_price) - 1

        return f'low_roi: {low_roi:.2f}, high_roi: {high_roi:.2f}, hold_roi: {hold_roi:.2f}'
