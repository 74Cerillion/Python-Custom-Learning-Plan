import unittest
import parser

fix1 = {
    "symbol": "AAPL",
    "price": 234.56,
    "timestamp": "2026-09-16T09:31:00"
}

fix2 = {
    "symbol": "AAPL",
    "price": 23456,
    "timestamp": "2026-09-16T09:31:00"
}

fix3 = {
    "symbol": "AAPL1",
    "price": 234.56,
    "timestamp": "2026-09-16 09:31:00"
}

fix4 = {
    "symbol": "APL",
    "price": 234.56,
    "timestamp": "2026-09-16T09:31:00"
}

class TestParser(unittest.TestCase):

    def test_hp(self):
        result = parser._validate(fix1)
        self.assertEqual(result, fix1)

    def test_hp2(self):
        result = parser._validate(fix2)
        self.assertEqual(result, fix2)

    def test_uhp(self):
        result = parser._validate(fix3)
        self.assertEqual(result, fix3)

    def test_boundary(self):
        result = parser._validate(fix4)
        self.assertEqual(result, fix4)