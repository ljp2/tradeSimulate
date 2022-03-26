
from barscandles import Bars, HACandles


if __name__ == '__main__':
    bars = Bars('20220202.csv')
    bar = bars.get_next_bar()
    print(bar.open, bar.high, bar.low, bar.close)
    print
    print(bars.get_all_bars())

