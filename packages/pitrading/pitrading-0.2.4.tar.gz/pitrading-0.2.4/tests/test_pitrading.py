#!/usr/bin/env python

"""Tests for `pitrading` package."""


from datetime import timedelta
import unittest

import pandas as pd

from pitrading import pitrading
from pitrading.holidays import Holidays
from pitrading.instrument import Instrument

class TestPitrading(unittest.TestCase):
    """Tests for `pitrading` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):
        """Test something."""
        ds = Holidays.to_datetime('20220101')
        while ds <= Holidays.to_datetime('20220722'):
            if Holidays.tradingday(ds):
                Instrument(ds.strftime('%Y%m%d'), morning=True).get_tradable_contracts()
            ds += timedelta(days=10)
            
        