import pytest
import econsim
import AgentTypes


from econsim.Commodity import Commodity
from econsim.Inventory import Inventory
from econsim.Market import Market
from AgentTypes import Farmer, Woodcutter

import logging

logging.basicConfig(filename='./log.log',
                    level=logging.DEBUG,
                    filemode='w',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.debug('Hello!')


def genFarmer():
    farmer = Farmer.Farmer()
    return farmer


def genWoodcutter():
    woodcutter = Woodcutter.Woodcutter()
    return woodcutter


def marketWith2Agents():
    market = Market()
    for i in range(1):
        market.agents.append(genFarmer())
        market.agents.append(genWoodcutter())
    return market


x = marketWith2Agents()
x.simulate(5)
