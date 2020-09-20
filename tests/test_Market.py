from AgentTypes import Farmer, Woodcutter
from econsim.Market import Market
from econsim.Inventory import Inventory
from econsim.Commodity import Commodity
import pytest
import econsim
import AgentTypes
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


@pytest.fixture
def emptyMarket():
    market = Market()
    return market


@pytest.fixture
def marketWith100Agents():
    market = Market()
    for i in range(50):
        market.agents.append(genFarmer())
        market.agents.append(genWoodcutter())
    return market


@pytest.fixture
def marketWith2Agents():
    market = Market()
    for i in range(1):
        market.agents.append(genFarmer())
        market.agents.append(genWoodcutter())
    return market


@pytest.fixture
def marketWith3Agents():
    market = Market()
    for i in range(1):
        market.agents.append(genFarmer())
        market.agents.append(genFarmer())
        market.agents.append(genWoodcutter())
    return market


def test_createEmptyMarket(emptyMarket):
    assert emptyMarket


def test_createFullMarket(marketWith100Agents):
    assert marketWith100Agents


def test_makingBids(emptyMarket):
    newFarmer = genFarmer()
    newFarmer.inventory.setAmountOf('Food', 0)
    newFarmer.inventory.setAmountOf('Wood', 8)
    newFarmer.inventory.setIdealAmount('Food', 8)
    newFarmer.inventory.setIdealAmount('Wood', 8)
    newFarmer.inventory.max_space = 100

    emptyMarket.agents.append(newFarmer)
    emptyMarket.agents[0].generateOffers(emptyMarket, 'Food')
    assert len(emptyMarket.book.bids['Food']) > 0


def test_singleSimRound(marketWith3Agents):
    x = marketWith3Agents
    x.simulate(100)
    assert True
