import os
import pandas as pd

class Bars:
    def __init__(self, filename):
        if os.name == 'nt':
            bars_dir = 'c:/trade/Data/bars1/'
        else:
            bars_dir = '/Users/ljp2/trade/Data/bars1/'
        # self.bars = list(pd.read_csv(bars_dir + '20220202.csv', parse_dates=['time']).itertuples(index=False))
        self.bars = pd.read_csv(bars_dir + '20220202.csv', parse_dates=['time'])
        self.current_bar_index = None

    def __getitem__(self, index):
        return self.bars.iloc[index]

    def len(self):
        return len(self.bars)

    def min(self):
        return self.bars.low.min()

    def max(self):
        return self.bars.high.max()

    def get_next_bar(self):
        if self.current_bar_index is None:
            self.current_bar_index = 0
        else:
            self.current_bar_index += 1
        return self[self.current_bar_index]

    def previous_bar(self):
        return self.bars[ self.current_bar_index - 1]

    def current_bar(self):
        return self[ self.current_bar_index]

    def get_all_bars(self):
        return self.bars


class HACandles:
    def __init__(self):
        self.candles = []
        self.current_candle_index = None

    def add(self, bar):
        t = bar.time
        o = bar.open
        h = bar.high
        l = bar.low
        c = bar.close

        if len(self.candles) == 0:
            thiscandle = (t,o,h,l,c)
            self.current_candle_index = 0
        else:
            pt,po,ph,pl,pc = self.candles[-1]
            ht = t
            ho = (po + pc) / 2
            hc = (o + h + l + c) / 4
            hh = max(h, ho, hc)
            hl = min(l, ho, hc)
            thiscandle = (ht, ho, hh, hl, hc)
        self.candles.append(thiscandle)
        self.current_candle_index = len(self.candles) - 1
        return thiscandle

    def all_candles(self):
        return self.candles

    def previous_candle(self):
        return self.candles[ self.current_candle_index - 1]

    def current_candle(self):
        return self.candles[ self.current_candle_index]


