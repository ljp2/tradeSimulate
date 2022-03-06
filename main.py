from multiprocessing import Process, Queue
from xmlrpc.client import FastUnmarshaller
import matplotlib.pyplot as plt
from random import uniform, random
import threading
from time import sleep
import pandas as pd
from tkinter import *
from tkinter import ttk
from multiprocessing import Manager

df = pd.read_csv('/Users/ljp2/trade/Data/bars1/20220202.csv')


def candles(q):
    global  df
    maxy = df.high.max()
    miny = df.low.min()

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.set_xlim([0, 391])
    ax.set_ylim([miny, maxy])
    plt.pause(.01)

    i = 0
    while i < 390:
        if q.empty() == False:
            row = q.get()
            if row.open < row.close:
                color = 'g'
                h = row.close - row.open
                b = row.open
            else:
                color = 'r'
                h = row.open - row.close 
                b = row.close
            plt.bar(i, h , width=0.8, bottom=b, color=color)
            ax.plot([i, i], [row.low, row.high], color=color)
            i += 1
        plt.pause(.01)

    plt.show()

class GUI(Tk):
    def __init__(self, q):
        super().__init__()
        self.title("Simulate Trading")
        self.index = 0
        self.q = q
        self.position = 0

        frm = ttk.Frame(self, padding=10)
        frm.grid()
        ttk.Button(frm, text="Next Bar", command=self.nextBarCallBack).grid(column=0, row=0)
        ttk.Button(frm, text="Buy MKT", command=self.buyMktCallBack).grid(column=0, row=1)
        ttk.Button(frm, text="SELL MKT", command=self.sellMktCallBack).grid(column=0, row=2)

        ttk.Label(frm, text='Profit/Loss for Day  ').grid(column=1, row=2)
        ttk.Label(frm, text='0').grid(column=2, row=2)




    def nextBarCallBack(self):
        row = df.iloc[self.index]
        self.price = row.close
        self.q.put(row)
        self.index += 1
       
    def buyMktCallBack(self):
        print('Bought', self.price)

    def sellMktCallBack(self):
        print('Sold', self.price)



if __name__ == '__main__':
    manager = Manager()
    q = manager.Queue()
    p = Process(target=candles, args=(q,), daemon=True)
    p.start()

    gui = GUI(q)
    gui.mainloop()

    # p.join()
