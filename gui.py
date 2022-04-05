from tkinter import *
from tkinter import ttk
from multiprocessing import Process, Queue
import os

from barscandles import Bars
from plots import createCandlePlot


class GUI(Tk):

    def openFile(self):
        global filename
        print("Opening File", self.filename.get())
        self.bars = Bars(self.filename.get())
        p1 = Process(target=createCandlePlot, args=(
            self.bars_queue,), daemon=True)
        p1.start()
        self.bars_queue.put(self.bars)
        self.select_file_btn['state'] = "disable"

        self.next_bar_btn.focus()

    def init_vars(self):
        self.filename = StringVar(value='20220202.csv')
        self.position = 0
        self.position_cost = 0.0
        self.position_value = 0.0

        self.unreal_pl = 0.0
        self.day_pl = 0.0

    def __init__(self, bars_queue):
        super().__init__()
        self.init_vars()

        self.title("Trading Simulation")
        self.bars_queue = bars_queue

        mainframe = ttk.Frame(self)
        mainframe.grid(row=0, column=0, padx=10, pady=10)

        filenameframe = ttk.Frame(mainframe)
        filenameframe.grid(row=0, column=0)

        if os.name == 'nt':
            values = os.listdir('c:/trade/Data/bars1/')
        else:
            values = os.listdir('/Users/ljp2/trade/Data/bars1/')

    # File Frame
        select_file_entry = ttk.Combobox(
            filenameframe, width=20, textvariable=self.filename, values=values)
        select_file_entry.grid(row=0, column=0, padx=5, pady=5)

        self.select_file_btn = ttk.Button(
            filenameframe, text='Open File', command=self.openFile)
        self.select_file_btn.grid(row=0, column=1, padx=5, pady=5)
        self.next_bar_btn = ttk.Button(
            filenameframe, text='Next Bar',  command=self.nextBar)
        self.next_bar_btn.grid(row=0, column=2)

    # Position Frame
        positionframe = ttk.Frame(mainframe)
        positionframe.grid(row=1, column=0, padx=10, pady=10)

        self.position_lbl = Label(
            positionframe, text="Position {:3d}".format(self.position))
        self.position_lbl.grid(row=0, column=0, padx=5, pady=5)

        self.unreal_pl_lbl = Label(
            positionframe, text="UnRealized P/L{:9.2f}".format(0))
        self.unreal_pl_lbl.grid(row=0, column=1, padx=10, pady=10)

        self.day_pl_lbl = Label(
            positionframe, text="Day P/L {:9.2f}".format(self.day_pl))
        self.day_pl_lbl.grid(row=0, column=2, padx=10, pady=10)

        self.position_cost_lbl = Label(
            positionframe, text="Position Cost {:9.2f}".format(self.position_cost))
        self.position_cost_lbl.grid(row=0, column=3, padx=10, pady=10)

        self.position_value_lbl = Label(
            positionframe, text="Position Value {:9.2f}".format(self.position_value))
        self.position_value_lbl.grid(row=0, column=4, padx=10, pady=10)

        self.price_lbl = Label(positionframe, text="Price -------")
        self.price_lbl.grid(row=1, column=0, padx=5, pady=5)
        buy_btn = ttk.Button(positionframe, text="Buy", command=self.buy)
        buy_btn.grid(row=1, column=1)
        sell_btn = ttk.Button(positionframe, text="Sell", command=self.sell)
        sell_btn.grid(row=1, column=2)

    def setPositionColor(self):
        pos = self.position
        if pos < 0:
            self.position_lbl['fg'] = 'red'
            self.position_cost_lbl['fg'] = 'red'
            self.position_value_lbl['fg'] = 'red'
        elif pos > 0:
            self.position_lbl['fg'] = 'green'
            self.position_cost_lbl['fg'] = 'green'
            self.position_value_lbl['fg'] = 'green'
        else:
            self.position_lbl['fg'] = 'black'
            self.position_cost_lbl['fg'] = 'black'
            self.position_value_lbl['fg'] = 'black'

        if self.unreal_pl < 0:
            self.unreal_pl_lbl['fg'] = 'red'
        elif self.unreal_pl > 0:
            self.unreal_pl_lbl['fg'] = 'green'
        else:
            self.unreal_pl_lbl['fg'] = 'black'

        if self.day_pl < 0:
            self.day_pl_lbl['fg'] = 'red'
        elif self.day_pl > 0:
            self.day_pl_lbl['fg'] = 'green'
        else:
            self.day_pl_lbl['fg'] = 'black'

    def setPositionLabels(self):
        self.position_value = self.position * self.current_price
        self.price_lbl['text'] = self.current_price
        self.position_lbl['text'] = "Position {:3d}".format(self.position)
        self.position_value_lbl['text'] = "Position Value {:9.2f}".format(
            self.position_value)
        self.position_cost_lbl['text'] = "Position Cost {:9.2f}".format(
            self.position_cost)
        self.unreal_pl_lbl['text'] = "UnRealized P/L{:9.2f}".format(
            self.unreal_pl)
        self.day_pl_lbl['text'] = "Day P/L {:9.2f}".format(self.day_pl)
        self.setPositionColor()

    def calculatePositionValues(self):
        self.position_value = self.position * self.current_price
        if self.position < 0:
            self.unreal_pl = abs(self.position_cost) - self.position_value
        if self.position == 0:
            self.unreal_pl = 0
        else:
            self.unreal_pl = self.position_value - self.position_cost

    def nextBar(self):
        bar = self.bars.get_next_bar()
        self.current_price = self.bars.current_bar().close
        self.calculatePositionValues()
        self.setPositionLabels()
        self.bars_queue.put(bar)

    def buy(self):
        quantity = 100
        if self.position < 0:
            value_per_share = self.position_cost / self.position
            pl = (abs(value_per_share) - self.current_price) * quantity
            self.day_pl += pl
            self.position += quantity
            self.position_cost = value_per_share * self.position
        elif self.position == 0:
            self.position += quantity
            self.position_cost = self.current_price * self.position
        else:
            self.position_cost += quantity * self.current_price
            self.position += quantity

        self.calculatePositionValues()
        self.setPositionLabels()
        self.next_bar_btn.focus()

    def sell(self):
        quantity = 100
        if self.position < 0:
            self.position_cost -= quantity * self.current_price
            self.position -= quantity
        elif self.position == 0:
            self.position -= quantity
            self.position_cost = self.current_price * self.position
        else:
            cost_per_share = self.position_cost / self.position
            pl = (self.current_price - cost_per_share) * quantity
            self.day_pl += pl
            self.position -= quantity
            self.position_cost = cost_per_share * self.position

        self.calculatePositionValues()
        self.setPositionLabels()
        self.next_bar_btn.focus()


def Gui(bars_queue: Queue):
    gui = GUI(bars_queue)
    gui.mainloop()


def main(bars_queue):
    p2 = Process(target=Gui, args=(bars_queue,))
    p2.start()
    p2.join()


if __name__ == '__main__':
    bars_queue = Queue()
    main(bars_queue)
    print("DONE DONE DONE")
