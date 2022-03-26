from base64 import b16decode
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd

from barscandles import Bars, HACandles

bars = Bars('20220202.csv')
xf = bars.get_all_bars()

width = (bars[1].time - bars[0].time) * 0.8
width2 = width * 0.2
col1 = 'green'
col2 = 'red'

# up = xf[xf.close>=xf.open]
# down = xf[xf.close < xf.open]


fig, ax = plt.subplots(figsize=(16,8))
ax.set_xlim(left = bars[0].time, right=bars.len())
ax.set_ylim(bottom=bars.min()-5, top=bars.max()+5)





# b1 = ax.bar(up.index,up.close-up.open,width,bottom=up.open,color=col1)
# b2 = ax.bar(up.index,up.high-up.close,width2,bottom=up.close,color=col1)
# b3 = ax.bar(up.index,up.low-up.open,width2,bottom=up.open,color=col1)
#
# b4 = ax.bar(down.index,down.close-down.open,width,bottom=down.open,color=col2)
# b5 = ax.bar(down.index,down.high-down.open,width2,bottom=down.open,color=col2)
# b6 = ax.bar(down.index,down.low-down.close,width2,bottom=down.close,color=col2)

# arts = []
# for b in (b1,b2,b3,b4,b5,b6):
#     arts.extend(b.get_children())
# return arts

# ani = animation.FuncAnimation(fig, candles, frames=50, blit=True,  interval=20,  repeat=False )



# for i,bar in xf.iterrows():
#     t,o,h,l,c,v,w = bar
#     ax.bar(i,c-o,.8,bottom=o,color=col1)
#     break

plt.show()

