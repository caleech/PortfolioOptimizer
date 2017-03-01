import unittest

class Result:
    def __init__(self):
        self.volatility = 0

def simulate(args):
    return Result()

class Args:
    def __init__(self):
        self.startyear = str()
        self.startmonth = str()
        self.startday = str()
        self.endyear = str()
        self.endmonth = str()
        self.endday = str()
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

    def test_volatility(self):
        self.assertEquals(0.0101467067654, simulate(self.args).volatility)

if __name__ == '__main__':
    unittest.main()
