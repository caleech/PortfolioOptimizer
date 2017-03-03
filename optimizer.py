import QSTK.qstkutil.DataAccess as da
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import datetime as dt
import numpy as np
import unittest

class Result:
    def __init__(self):
        self.average_daily_return = 0

def get_timestamps_for_market_close(args):
    start = dt.datetime(args.startyear, args.startmonth, args.startday)
    end = dt.datetime(args.endyear, args.endmonth, args.endday)
    market_close = dt.timedelta(hours=16)
    return du.getNYSEdays(start, end, market_close)

def get_close_prices(timestamps, symbols):
    database = da.DataAccess('Yahoo')
    fields = ['close']
    result = dict(zip(fields, database.get_data(timestamps, symbols, fields)))
    for i in fields:
        result[i] = result[i].fillna(method='ffill')
        result[i] = result[i].fillna(method='bfill')
        result[i] = result[i].fillna(1.0)

    return result['close'].values

def normalize(prices):
    return prices / prices[0, :]

def simulate(args):
    prices = normalize(
        get_close_prices(
            get_timestamps_for_market_close(args), args.symbols))

    out = Result()
    prices_out = prices.copy()
    tsu.returnize0(prices_out)
    out.average_daily_return = np.average(prices_out)

    return out


class Args:
    def __init__(self):
        self.startyear = 1
        self.startmonth = 1
        self.startday = 1
        self.endyear = 1
        self.endmonth = 1
        self.endday = 1
        self.symbols = []

class Tests(unittest.TestCase):
    def setUp(self):
        self.args = Args()
        self.args.startyear = 2011
        self.args.startmonth = 1
        self.args.startday = 1
        self.args.endyear = 2011
        self.args.endmonth = 12
        self.args.endday = 31
        self.args.symbols = ["AAPL", "GLD", "GOOG", "XOM"]

    def test_average_daily_return(self):
        self.assertAlmostEqual(0.000657261102001,
                               simulate(self.args).average_daily_return,
                               places=4)

if __name__ == '__main__':
    unittest.main()
