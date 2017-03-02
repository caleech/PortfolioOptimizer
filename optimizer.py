import datetime as dt
import unittest
import QSTK.qstkutil.DataAccess as da
import QSTK.qstkutil.qsdateutil as du

class Result:
    def __init__(self):
        self.average_daily_return = 0

def get_timestamps_for_market_close(args):
    start = dt.datetime(args.startyear, args.startmonth, args.startday)
    end = dt.datetime(args.endyear, args.endmonth, args.endday)
    market_close = dt.timedelta(hours=16)
    return du.getNYSEdays(start, end, market_close)

def get_market_data(fields, timestamps, symbols):
    database = da.DataAccess('Yahoo')
    return dict(zip(fields, database.get_data(timestamps, symbols, fields)))

def simulate(args):
    fields = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
    print get_market_data(fields,
                          get_timestamps_for_market_close(args),
                          args.symbols)
    return Result()

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
        self.assertEquals(0.000657261102001, simulate(self.args).average_daily_return)

if __name__ == '__main__':
    unittest.main()
