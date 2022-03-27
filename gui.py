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

        p1 = Process(target=createCandlePlot, args=(self.bars_queue,))
        p1.start()

        self.bars_queue.put(
            {
                'cmd': "init",
                'data': self.bars
            }
        )


    def nextBar(self):
        self.bars_queue.put(1)
            
    def __init__(self, bars_queue):
        super().__init__()
        self.title("Trading Simulation")
        self.bars_queue = bars_queue

        mainframe = ttk.Labelframe(self, text='Select File')
        mainframe.grid(row=0, column=0, padx=10, pady=10)

        filename_lbl = ttk.Label(mainframe, text='Day File')
        filename_lbl.grid(row=0, column=0)
        self.filename = StringVar(value='20220202.csv')


        select_file_btn = ttk.Button(mainframe, text="Open File", command=self.openFile)
        select_file_entry = ttk.Entry(mainframe, width=20, textvariable=self.filename)
        select_file_btn.grid(row=1, column=1, padx=5, pady=5)
        select_file_entry.grid(row=1, column=0)

        next_bar_btn = ttk.Button(mainframe, text='Next Bar',  command=self.nextBar)
        next_bar_btn.grid(row=1, column=2)

def Gui(bars_queue:Queue):
    gui = GUI(bars_queue)
    gui.mainloop()


def main(bars_queue):
    
    # p1 = Process(target=createCandlePlot, args=(bars_queue,))
    p2 = Process(target=Gui, args=(bars_queue,))

    # p1.start()
    p2.start()
    # p1.join()
    p2.join()

if __name__ == '__main__': 
    bars_queue = Queue()
    main(bars_queue)
    print("DONE DONE DONE")