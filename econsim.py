import pytest
import econsim
import AgentTypes
import math
from matplotlib import animation
import pylab as plt


from econsim.Commodity import Commodity
from econsim.Inventory import Inventory
from econsim.Market import Market
from econsim.History import Plotter

from AgentTypes.Farmer import Farmer
from AgentTypes.Woodcutter import Woodcutter
from AgentTypes.Miner import Miner
from AgentTypes.Smelter import Smelter
from AgentTypes.Blacksmith import Blacksmith

import logging

logging.basicConfig(filename='./log.log',
                    level=logging.DEBUG,
                    filemode='w',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.debug('Hello!')


def marketWith2Agents():
    market = Market()
    for i in range(10):
        market.addNewAgent(Farmer())
        market.addNewAgent(Woodcutter())
        market.addNewAgent(Miner())
        market.addNewAgent(Smelter())
        market.addNewAgent(Blacksmith())

    return market


x = marketWith2Agents()
NROUNDS = 800
for i in range(NROUNDS):
    x.simulate(1)
    # Farmer.foodOutput = 1 * \
    #     round(math.cos(8*i*2*math.pi/NROUNDS) + 1.4)
    # Woodcutter.woodOutput = 1 * \
    #     round(math.sin(8*i*2*math.pi/NROUNDS) + 1.4)
    if (i > 200) and (i < 300):
        Woodcutter.woodOutput = 0
    else:
        Woodcutter.woodOutput = 2
print('End')


# Animation bits. Needs tidying up. Please Ignore =)
fig, ax = plt.subplots(figsize=(20, 6))
ax.set_xlim([0, NROUNDS])
ax.set_ylim([0, 60])
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tick_params(labelsize=14)
ax.set_xlabel('Time', fontsize=14)
ax.set_ylabel('Cost', fontsize=14)
ax.grid(axis='y')
commodityTypes = ['Food', 'Wood', 'Ore', 'Metal', 'Tools']
lines = []
for index in range(5):
    lobj = ax.plot([], [], lw=2, label=commodityTypes[index])[0]
    lines.append(lobj)


def init():
    for line in lines:
        line.set_data([], [])
    return lines


FRAMES = 400
interval = NROUNDS/FRAMES


def animate(i):
    IDX = int(interval*i)
    xdata = range(IDX)
    yfood = x.book.meanPrices['Food'][:IDX]
    ywood = x.book.meanPrices['Wood'][:IDX]
    yore = x.book.meanPrices['Ore'][:IDX]
    ymetal = x.book.meanPrices['Metal'][:IDX]
    ytools = x.book.meanPrices['Tools'][:IDX]
    ydata = [yfood, ywood, yore, ymetal, ytools]
    for lnum, line in enumerate(lines):
        line.set_data([xdata, ydata[lnum]])
    legend = plt.legend(fontsize=14)
    return lines + [legend]


anim = animation.FuncAnimation(fig,
                               animate,
                               init_func=init,
                               frames=FRAMES,
                               interval=20,
                               blit=True)
anim.save('./animation.gif', writer='imagemagick', fps=60)
