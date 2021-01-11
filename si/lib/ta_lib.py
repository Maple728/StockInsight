import numpy as np
import pandas as pd


# ---------------------------- Standard Indicator -----------------------------
def moving_average(data_array, cur_idx, window=14):
    """
    Moving Average (MA) of data_array in observation window (cur_idx - window, cur_idx].
    Args:
        data_array: list or ndarray.
            Full data list.
        cur_idx: int > 0.
            The current index.
        window: int > 0.
            The size of observation window.
    Returns:
        A scalar.
    """
    return np.mean(data_array[cur_idx - window + 1: cur_idx + 1])


def exp_moving_average(data_array, cur_idx, window=14):
    """
    Exponential Moving Average (EMA) of data_array in observation window (cur_idx - window, cur_idx].
    Args:
        data_array: list or ndarray.
            Full data list.
        cur_idx: int > 0.
            The current index.
        window: int > 0.
            The size of observation window.

    Returns:
        A scalar.
    """

    alpha = 2 / (window + 1)
    ema = data_array[cur_idx - window]

    for idx in range(cur_idx - window + 1, cur_idx + 1):
        ema = ema + alpha * (data_array[idx] - ema)

    return ema


def true_range(quotes, cur_idx):
    """
    True Range indicator (TR), is used to indicate the true range of the trading day.
    Args:
        quotes: DataFrame.
            A dataframe contains the <quote_date, open, high, low, close>, and be sorted by quote_date ascending.
        cur_idx: int > 0.
            The current index.

    Returns:
        A scalar.
    """
    pre_close = quotes.iloc[cur_idx - 1].close
    quote = quotes.iloc[cur_idx]
    return max(quote.high - quote.low, abs(quote.high - pre_close), abs(quote.low - pre_close))


def average_true_range(quotes, cur_idx, window=14):
    """
    Average True Range (ATR), is used to simply indicate the degree of price volatility.
    Args:
        quotes: DataFrame.
            A dataframe contains the <quote_date, open, high, low, close>, and be sorted by quote_date ascending.
        cur_idx: int > 0.
            The current index.
        window: int > 0.
            The size of observation window.

    Returns:
        A scalar.
    """
    tr_list = [true_range(quotes, i) for i in range(cur_idx - window + 1, cur_idx + 1)]
    return np.mean(tr_list)


def norm_price(quotes, cur_idx):
    """
    Normalized Price (NP).
    Args:
        quotes: DataFrame.
            A dataframe contains the <quote_date, open, high, low, close>, and be sorted by quote_date ascending.
        cur_idx: int > 0.
            The current index.

    Returns:
        A scalar.
    """
    quote = quotes.iloc[cur_idx]
    return (quote.high + quote.low + quote.close) / 3


def money_flow_index(quotes, cur_idx, window=14):
    """
    Average True Range (ATR), is used to simply indicate the degree of price volatility.
    Args:
        quotes: DataFrame.
            A dataframe contains the <quote_date, open, high, low, close>, and be sorted by quote_date ascending.
        cur_idx: int > 0.
            The current index.
        window: int > 0.
            The size of observation window.

    Returns:
        A scalar.
    """
    pos_mf = 0.0
    neg_mf = 0.0

    prev_np = NP(quotes, cur_idx - window)
    for i in range(index - period + 1, index + 1):
        cur_np = NP(quotes, i)
        if prev_np < cur_np:
            # Positive MF
            pos_mf += quotes.iloc[i].volume * cur_np
        elif prev_np > cur_np:
            # Negetive MF
            neg_mf += quotes.iloc[i].volume * cur_np

        prev_np = cur_np

    if neg_mf == 0:
        return 100
    else:
        return 100 - 100 / (1 + pos_mf / neg_mf)


# ---------------------------------- Customize Indicator ----------------------------
def angular(quotes, cur_idx, side_window=5):
    """
    Check whether the current quote is the angular point, that is, it's high price is the highest price or low price is
    the lowest price in the observation window.
    Args:
        quotes: DataFrame.
            A dataframe contains the <quote_date, open, high, low, close>, and be sorted by quote_date ascending.
        cur_idx: int > 0.
            The current index.
        side_window: int, default 5.
            The past and future window size at the current index.

    Returns:
        True if it's angular point, otherwise False.
    """

    ob_quotes = quotes.iloc[cur_idx - side_window: cur_idx + side_window]

    if quotes.iloc[cur_idx].high >= np.max(ob_quotes.high) or quotes.iloc[cur_idx].low <= np.min(ob_quotes.low):
        return True
    else:
        return False


def MI(quotes, index, period=25):
    ''' Mass Index '''
    EMA_PERIOD = 9

    try:

        high_low_diff = quotes.high - quotes.low
        high_low_diff = high_low_diff[0: index + 1]
        # single_ema list including (period + EMA_PERIOD) elements

        single_ema_list = EMA_LIST(high_low_diff, EMA_PERIOD)[EMA_PERIOD:]
        double_ema_list = EMA_LIST(single_ema_list, EMA_PERIOD)

        return np.sum(single_ema_list[-period:] / double_ema_list[-period:])
    except:
        return None


def is_reverse_bulge(quotes, index):
    if index < 0:
        return False
    try:
        pre_mi = MI(quotes, index - 1)
        if pre_mi < 26.5:
            return False
        cur_mi = MI(quotes, index)
        if cur_mi >= pre_mi:
            return False

        return True
    except:
        return False


def VOLATILITY_AN(quotes, index, period=14):
    """
    Volatility calucated by mean of NP divide ATR
    Args:
        quotes:
        index:
        period:

    Returns:

    """
    try:
        return ATR(quotes, index, period) / np.mean([NP(quotes, j) for j in range(index - period + 1, index + 1)])
    except Exception as e:
        return None


def volatility(quotes, index, period):
    atr = average_true_range(quotes, index, period)
    avg = np.mean(quotes.iloc[index - period + 1: index + 1].close)
    return atr / avg
