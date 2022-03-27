from queue import Queue
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.animation import FuncAnimation

from barscandles import Bars, HACandles

def createCandlePlot(q):
    bars = q.get()['data']
    habars = HACandles()

    width = (bars[1].time - bars[0].time) * 0.8
    width2 = width * 0.2
    col1 = 'green'
    col2 = 'red'

    fig, axs = plt.subplots(2, 1, sharex=True, sharey=True, figsize=(10,5))
    ax,bx = axs
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    left =  bars[0].time - width
    right = bars[-1].time + width
    ax.set_xlim(left=left, right=right)
    ax.set_ylim(bottom=bars.min()-5, top=bars.max()+5)

    i = 0
    while i < 390:
        if not q.empty():
            q.get()
            bar = bars[i]
            i += 1
            t, o, h, l, c, v, w = bar
            if c >= o:
                b1 = ax.bar(t, c-o, width, bottom=o, color=col1)
                b2 = ax.bar(t, h-c, width2, bottom=c, color=col1)
                b3 = ax.bar(t, l-o, width2, bottom=o, color=col1)
            else:
                b4 = ax.bar(t, c-o, width, bottom=o, color=col2)
                b5 = ax.bar(t, h-o, width2, bottom=o, color=col2)
                b6 = ax.bar(t, l-c, width2, bottom=c, color=col2)

            ha = habars.add(bar)
            t,o,h,l,c = ha
            if c >= o:
                b1 = bx.bar(t, c-o, width, bottom=o, color=col1)
                b2 = bx.bar(t, h-c, width2, bottom=c, color=col1)
                b3 = bx.bar(t, l-o, width2, bottom=o, color=col1)
            else:
                b4 = bx.bar(t, c-o, width, bottom=o, color=col2)
                b5 = bx.bar(t, h-o, width2, bottom=o, color=col2)
                b6 = bx.bar(t, l-c, width2, bottom=c, color=col2)
                
        plt.pause(0.05)
        


    plt.show()