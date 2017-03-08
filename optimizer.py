import QSTK.qstkutil.DataAccess as da
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import datetime as dt
import numpy as np
import unittest

class Result:
    def __init__(self):
        self.average_daily_return = 0
        self.cumulative_daily_value = 0
        self.volatility = 0

    def sharpe_ratio(self):
        trading_days = 250
        return (self.average_daily_return/self.volatility)*np.sqrt(trading_days)

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

def check_args(args):
    if len(args.symbols) != len(args.allocations):
        raise ValueError("Symbols don't match allocations")
    if np.sum(args.allocations) != 1.0:
        raise ValueError("Allocations must sum to 1.0")

def apply_allocations(prices, allocations):
    return prices * allocations

def simulate(args):
    check_args(args)
    prices = apply_allocations(
        normalize(
            get_close_prices(
                get_timestamps_for_market_close(args), args.symbols)),
        args.allocations)

    out = Result()
    row_wise_sum = prices.copy().sum(axis=1).copy()
    out.cumulative_daily_value = np.sum(tsu.returnize0(row_wise_sum)) + 1
    out.average_daily_return = np.average(row_wise_sum)
    out.volatility = np.std(row_wise_sum)

    return out

def get_possible_allocations(args):
    out = []
    if not args.symbols:
        out.append([])
    elif len(args.symbols) == 1:
        out.append([1])

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
        self.allocations = []

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
        self.args.allocations = [0.4, 0.4, 0.0, 0.2]

    def test_average_daily_return(self):
        self.assertAlmostEqual(0.000657261102001,
                               simulate(self.args).average_daily_return,
                               places=10)

    def test_cumulative_daily_value(self):
        self.assertAlmostEqual(1.16487261965,
                               simulate(self.args).cumulative_daily_value,
                               places=2)

    def test_volatility(self):
        self.assertAlmostEqual(0.0101467067654,
                               simulate(self.args).volatility,
                               places=7)

    def test_sharpe(self):
        self.assertAlmostEqual(1.02828403099,
                               simulate(self.args).sharpe_ratio(),
                               places=2)

    def test_allocations_and_symbol_mismatch(self):
        def fn():
            self.args.symbols = []
            simulate(self.args)

        self.assertRaises(ValueError, fn)

    def test_allocations_must_sum_to_one(self):
        def fn():
            self.args.allocations = [1, 1, 1, 1]
            simulate(self.args)

        self.assertRaises(ValueError, fn)

    def test_empty_possible_allocations(self):
        self.args.symbols = []
        self.assertEqual([[]], get_possible_allocations(self.args))

    def test_get_possible_allocations_for_single_symbol(self):
        self.args.symbols = ["GOOG"]
        self.assertEqual([[1]], get_possible_allocations(self.args))

    def test_get_possible_allocations_for_two_symbols(self):
        self.args.symbols = ["GOOG", "AAPL"]
        items = get_possible_allocations(self.args)
        self.assertEqual([1.0, 0.0], items[0])
        self.assertEqual([0.9, 0.1], items[1])

if __name__ == '__main__':
    unittest.main()
