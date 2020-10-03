import pytest
import econsim
import AgentTypes
import math


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
for i in range(800):
    x.simulate(1)
    Farmer.foodOutput = 1 * \
        round(math.cos(i*2*math.pi/200) + 1.4)
    Woodcutter.woodOutput = 1 * \
        round(math.sin(i*2*math.pi/100) + 1.4)
    print(i, Farmer.foodOutput)
# for agent in x.agents:
#     agent.inventory.setAmountOf('Wood', 0)
#     agent.inventory.setAmountOf('Food', 0)
# x.simulate(800)
y = Plotter()
y.plotAllPrices(x)
