from multiprocessing import Process, Queue
from xmlrpc.client import FastUnmarshaller
import matplotlib.pyplot as plt
from random import uniform, random
import pandas as pd
from tkinter import *
from tkinter import ttk
from multiprocessing import Manager
import sys
from collections import namedtuple

df = pd.read_csv('/Users/ljp2/trade/Data/bars1/20220202.csv')

Bar = namedtuple('Bar', 'time open high low close')

class HA:
    def __init__(self) -> None:
        self.bars = []

    def add(self, bar):
        t = bar.time
        o = bar.open
        h = bar.high
        l = bar.low
        c = bar.close

        if len(self.bars) == 0:
            thisbar = Bar(t,o,h,l,c) 
        else:
            pt,po,ph,pl,pc = self.bars[-1]
            ht = t
            ho = (po + pc) / 2
            hc = (o + h + l + c) / 4
            hh = max(h, ho, hc)
            hl = min(l, ho, hc)
            thisbar = Bar(ht, ho, hh, hl, hc) 
        self.bars.append(thisbar)
        return thisbar


def candles(q, miny, maxy):
    fig, ax = plt.subplots(figsize=(12, 6))
    # fig = plt.Figure()
    # ax = plt.axes()
    ax.set_xlim(-10,391)
    ax.set_ylim([miny, maxy])
    plt.pause(.01)

    i = 0
    while True:
        if q.empty() == False:
            row = q.get()
            if row.open < row.close:
                print('o < c')
                color = 'g'
                h = row.close - row.open
                b = row.open
            else:
                color = 'r'
                h = row.open - row.close 
                b = row.close
            print(h, b, color)
            plt.bar(i, h , width=0.8, bottom=b, color=color)
            ax.plot([i, i], [row.low, row.high], color=color)
            i += 1
        plt.pause(.01)

    plt.show()

class GUI(Tk):
    def __init__(self, q, df):
        super().__init__()
        self.title("Simulate Trading")
        self.index = 0
        self.df = df
        self.q = q
        self.position = 0
        self.ha = HA()

        frm = ttk.Frame(self, padding=10)
        frm.grid()
        ttk.Button(frm, text="Next Bar", command=self.nextBarCallBack).grid(column=0, row=0)
        ttk.Button(frm, text="Buy MKT", command=self.buyMktCallBack).grid(column=0, row=1)
        ttk.Button(frm, text="SELL MKT", command=self.sellMktCallBack).grid(column=0, row=2)

        ttk.Label(frm, text='Profit/Loss for Day  ').grid(column=1, row=2)
        ttk.Label(frm, text='0').grid(column=2, row=2)

    def nextBarCallBack(self):
        if self.index < self.df.shape[0]:
            row = self.df.iloc[self.index]
            row = self.ha.add(row)
            self.price = row.close
            self.q.put(row)
            self.index += 1
       
    def buyMktCallBack(self):
        print('Bought', self.price)

    def sellMktCallBack(self):
        print('Sold', self.price)



if __name__ == '__main__':
    if sys.platform == 'darwin':
        bars_dir = '/Users/ljp2/trade/Data/bars1/'
    else:
        bars_dir = 'c:/trade/Data/bars1/'

    df = pd.read_csv(bars_dir + '20220202.csv', parse_dates=['time'])

    maxy = df.high.max()
    miny = df.low.min(

    )
    manager = Manager()
    q = manager.Queue()
    p = Process(target=candles, args=(q, miny, maxy), daemon=True)
    p.start()

    gui = GUI(q, df)
    gui.mainloop()

