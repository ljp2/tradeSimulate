import os
import numpy as np
import pandas as pd


class Bars:
    def __init__(self, filename):
        if os.name == 'nt':
            bars_dir = 'c:/trade/Data/bars1/'
        else:
            bars_dir = '/Users/ljp2/trade/Data/bars1/'
        self.bars = list(pd.read_csv(bars_dir + '20220202.csv', parse_dates=['time']).itertuples(index=False))
        self.index = 0

    def next_bar(self):
        bar = self.bars[self.index]
        self.index += 1
        return bar


class HABars:
    def __init__(self):
        self.bars = []

    def add(self, bar):
        t = bar.time
        o = bar.open
        h = bar.high
        l = bar.low
        c = bar.close

        if len(self.bars) == 0:
            thisbar = (t,o,h,l,c)
        else:
            pt,po,ph,pl,pc = self.bars[-1]
            ht = t
            ho = (po + pc) / 2
            hc = (o + h + l + c) / 4
            hh = max(h, ho, hc)
            hl = min(l, ho, hc)
            thisbar = (ht, ho, hh, hl, hc)
        self.bars.append(thisbar)
        return thisbar


# compute heiken aski bars


# computer indicators

# make decision

# adjust statistics based upon decisions


if __name__ == '__main__':
    bars = Bars('20220202.csv')
    bar = bars.next_bar()
    print(bar.open, bar.high, bar.low, bar.close)
