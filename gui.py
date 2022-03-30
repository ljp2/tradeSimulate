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
        p1 = Process(target=createCandlePlot, args=(self.bars_queue,), daemon=True)
        p1.start()
        self.bars_queue.put(self.bars)
        self.select_file_btn['state'] = "disable"

        self.next_bar_btn.focus()

    def nextBar(self):
        bar = self.bars.get_next_bar()
        self.bars_queue.put(bar)
        close_price = "Price {:.2f}".format(bar.close) 
        self.price_lbl['text'] = close_price

    def init_vars(self):
        self.filename = StringVar(value='20220202.csv')
        self.position = 0

    def update_value_vars():
        pass
            
    def __init__(self, bars_queue):
        super().__init__()
        self.init_vars()

        self.title("Trading Simulation")
        self.bars_queue = bars_queue

        mainframe = ttk.Frame(self)
        mainframe.grid(row=0, column=0, padx=10, pady=10)

        filenameframe = ttk.Frame(mainframe)
        filenameframe.grid(row=0,column=0)

        if os.name == 'nt':
            values=os.listdir('c:/trade/Data/bars1/')
        else:
            values=os.listdir('/Users/ljp2/trade/Data/bars1/')

    # File Frame
        select_file_entry = ttk.Combobox(filenameframe, width=20, textvariable=self.filename, values=values)
        select_file_entry.grid(row=0, column=0, padx=5, pady=5)

        self.select_file_btn = ttk.Button(filenameframe, text='Open File', command=self.openFile)
        self.select_file_btn.grid(row=0, column=1, padx=5, pady=5)
        self.next_bar_btn = ttk.Button(filenameframe, text='Next Bar',  command=self.nextBar)
        self.next_bar_btn.grid(row=0, column=2)

    # Position Frame
        positionframe = ttk.Frame(mainframe)
        positionframe.grid(row=1, column=0, padx=10, pady=10)
        
        self.position_lbl = Label(positionframe, text="Position 0")
        self.position_lbl.grid(row=0, column=0, padx=5, pady=5)
        # self.position_entry = ttk.Entry(positionframe, width=8, textvariable=self.position)
        # self.position_entry.grid(row=0, column=1, padx=10, pady=10)

        self.position_value_lbl = Label(positionframe, text="Position Value -----------")
        self.position_value_lbl.grid(row=0, column=2, padx=10, pady=10)
        # posvalue_entry = ttk.Entry(positionframe, width=8, textvariable=self.posvalue)
        # posvalue_entry.grid(row=0, column=3, padx=5, pady=5)

        self.unreal_pl_lbl = ttk.Label(positionframe, text="UnRealized P/L -------")
        self.unreal_pl_lbl.grid(row=0, column=4, padx=10, pady=10)
        # unreal_pl_entry = ttk.Entry(positionframe, width=8, textvariable=self.unreal_profit_loss)
        # unreal_pl_entry.grid(row=0, column=5, padx=5, pady=5)

        self.day_pl_lbl = ttk.Label(positionframe, text="Day P/L ------")
        self.day_pl_lbl.grid(row=0, column=6, padx=10, pady=10)
        # day_pl_entry = ttk.Entry(positionframe, width=8, textvariable=self.day_profit_loss)
        # day_pl_entry.grid(row=0, column=7, padx=5, pady=5)

        self.price_lbl = ttk.Label(positionframe, text="Price -------")
        self.price_lbl.grid(row=1, column=0, padx=5, pady=5)
        buy_btn = ttk.Button(positionframe, text="Buy", command=self.buy)
        buy_btn.grid(row=1, column=1)        
        sell_btn = ttk.Button(positionframe, text="Sell", command=self.sell)
        sell_btn.grid(row=1, column=2)


    def setPositionColor(self):
        pos = self.position
        if pos < 0:
            self.position_lbl['fg'] = 'red'
            self.position_value_lbl['fg'] = 'red'
        elif pos > 0:
            self.position_lbl['fg'] = 'green'
            self.position_value_lbl['fg'] = 'green'
        else:
            self.position_lbl['fg'] = 'black'
            self.position_value_lbl['fg'] = 'black'

    def buy(self):
        newpos = self.position + 100
        self.position_lbl['text'] = "Position {:.2f}".format(newpos)
        self.position = newpos

        close_price = self.bars.current_bar().close
        value = self.position * close_price
        self.position_value_lbl['text'] = "Position Value {:9.2f}".format(value)
        self.setPositionColor()

        self.next_bar_btn.focus()


        # posvalue = float(self.posvalue.get())
        # close_price = self.bars.current_bar().close
        # newpos = pos + 100
        # self.position_value += close_price * 100
        # if newpos == 0:
        #     newposvalue = 0
        # else:
        #     newposvalue = self.position_value / abs(newpos)
        # self.position.set(newpos)
        # self.posvalue.set(newposvalue)

    def sell(self):
        newpos = self.position - 100
        self.position_lbl['text'] = "Position {}".format(newpos)
        self.position = newpos

        close_price = self.bars.current_bar().close
        value = self.position * close_price
        self.position_value_lbl['text'] = "Position Value {:9.2f}".format(value)
        self.setPositionColor()

        self.next_bar_btn.focus()

        # pos = int(self.position.get())
        # posvalue = float(self.posvalue.get())
        # close_price = self.bars.current_bar().close
        # newpos = pos - 100
        # self.position_value -= close_price * 100
        # if newpos == 0:
        #     newposvalue = 0
        # else:
        #     newposvalue = self.position_value / abs(newpos)
        # self.position.set(newpos)
        # self.posvalue.set(newposvalue)

def Gui(bars_queue:Queue):
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