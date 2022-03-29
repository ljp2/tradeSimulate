from tkinter import *
from tkinter import ttk
from multiprocessing import Process, Queue

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


    def nextBar(self):
        bar = self.bars.get_next_bar()
        self.bars_queue.put(bar)

    def init_vars(self):
        self.filename = StringVar(value='20220202.csv')
        self.position = StringVar(value=0)
        self.avgprice = StringVar(value = 0)
        self.unreal_profit_loss = StringVar(value = 0)
        self.day_profit_loss = StringVar(value = 0)

            
    def __init__(self, bars_queue):
        super().__init__()
        self.init_vars()

        self.title("Trading Simulation")
        self.bars_queue = bars_queue

        mainframe = ttk.Frame(self)
        mainframe.grid(row=0, column=0, padx=10, pady=10)

        filenameframe = ttk.Frame(mainframe)
        filenameframe.grid(row=0,column=0)
        select_file_entry = ttk.Entry(filenameframe, width=20, textvariable=self.filename)
        select_file_entry.grid(row=0, column=0, padx=5, pady=5)
        self.select_file_btn = ttk.Button(filenameframe, text='Open File', command=self.openFile)
        self.select_file_btn.grid(row=0, column=1, padx=5, pady=5)
        next_bar_btn = ttk.Button(filenameframe, text='Next Bar',  command=self.nextBar)
        next_bar_btn.grid(row=0, column=2)


        positionframe = ttk.Frame(mainframe)
        positionframe.grid(row=1, column=0, padx=10, pady=10)
        position_lbl = ttk.Label(positionframe, text="Position")
        position_lbl.grid(row=0, column=0, padx=5, pady=5)
        self.position_entry = ttk.Entry(positionframe, width=8, textvariable=self.position)
        self.position_entry.grid(row=0, column=1, padx=10, pady=10)

        avgprice_lbl = ttk.Label(positionframe, text="AvgPrice")
        avgprice_lbl.grid(row=0, column=2, padx=10, pady=10)
        avgprice_entry = ttk.Entry(positionframe, width=8, textvariable=self.avgprice)
        avgprice_entry.grid(row=0, column=3, padx=5, pady=5)

        unreal_pl_lbl = ttk.Label(positionframe, text="UnReal P/L")
        unreal_pl_lbl.grid(row=0, column=4, padx=10, pady=10)
        unreal_pl_entry = ttk.Entry(positionframe, width=8, textvariable=self.unreal_profit_loss)
        unreal_pl_entry.grid(row=0, column=5, padx=5, pady=5)

        day_pl_lbl = ttk.Label(positionframe, text="Day P/L")
        day_pl_lbl.grid(row=0, column=6, padx=10, pady=10)
        day_pl_entry = ttk.Entry(positionframe, width=8, textvariable=self.day_profit_loss)
        day_pl_entry.grid(row=0, column=7, padx=5, pady=5)

        buy_btn = ttk.Button(positionframe, text="Buy", command=self.buy)
        buy_btn.grid(row=1, column=0)        
        sell_btn = ttk.Button(positionframe, text="Sell", command=self.sell)
        sell_btn.grid(row=1, column=1)


    def buy(self):
        pos = int(self.position.get())
        avgprice = float(self.avgprice.get())
        close_price = self.bars.current_bar().close
        newpos = pos + 100
        self.position_value += close_price * 100
        if newpos == 0:
            newavgprice = 0
        else:
            newavgprice = self.position_value / abs(newpos)
        self.position.set(newpos)
        self.avgprice.set(newavgprice)

    def sell(self):
        pos = int(self.position.get())
        avgprice = float(self.avgprice.get())
        close_price = self.bars.current_bar().close
        newpos = pos - 100
        self.position_value -= close_price * 100
        if newpos == 0:
            newavgprice = 0
        else:
            newavgprice = self.position_value / abs(newpos)
        self.position.set(newpos)
        self.avgprice.set(newavgprice)

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