import pytest
import econsim
import AgentTypes


from econsim.Commodity import Commodity
from econsim.Inventory import Inventory
from AgentTypes import Farmer, Woodcutter


@pytest.fixture
def farmer():
    farmer = Farmer.Farmer()
    return farmer


@pytest.fixture
def tradingFarmer():
    farmer = Farmer.Farmer()
    farmer.inventory.max_size = 20
    farmer.inventory.addTradeOfCommodity('Wood', 5)
    farmer.inventory.addTradeOfCommodity('Wood', 4)
    farmer.inventory.addTradeOfCommodity('Wood', 6)
    farmer.inventory.addTradeOfCommodity('Wood', 7)
    farmer.inventory.addTradeOfCommodity('Wood', 3)
    farmer.setPriceBeliefsOf('Wood', 2, 8)
    return farmer


def test_priceUpdateSoldNormal(tradingFarmer):
    tradingFarmer.updatePriceBeliefs(marketPrice=5,
                                     act='SELL',
                                     commodityType='Wood',
                                     wasSuccess=True,
                                     unitPrice=6)
    priceMin, priceMax = tradingFarmer.getPriceBeliefsOf('Wood')
    priceMean = (priceMin + priceMax)/2

    assert priceMin > 2
    assert priceMax < 8
    assert abs(priceMean - 5) < 0.01


def test_priceUpdateBoughtNormal(tradingFarmer):
    tradingFarmer.updatePriceBeliefs(marketPrice=5,
                                     act='BUY',
                                     commodityType='Wood',
                                     wasSuccess=True,
                                     unitPrice=6)
    priceMin, priceMax = tradingFarmer.getPriceBeliefsOf('Wood')
    priceMean = (priceMin + priceMax)/2

    assert priceMin > 2
    assert priceMax < 8
    assert abs(priceMean - 5) < 0.01


def test_priceUpdateSoldUndersold(tradingFarmer):
    tradingFarmer.updatePriceBeliefs(marketPrice=10,
                                     act='SELL',
                                     commodityType='Wood',
                                     wasSuccess=True,
                                     unitPrice=5)
    priceMin, priceMax = tradingFarmer.getPriceBeliefsOf('Wood')
    priceMean = (priceMin + priceMax)/2

    assert priceMin > 2
    assert priceMax > 8
    assert priceMean > 5


def test_priceUpdateBoughtOverpaid(tradingFarmer):
    tradingFarmer.updatePriceBeliefs(marketPrice=1,
                                     act='BUY',
                                     commodityType='Wood',
                                     wasSuccess=True,
                                     unitPrice=15)
    priceMin, priceMax = tradingFarmer.getPriceBeliefsOf('Wood')
    priceMean = (priceMin + priceMax)/2

    assert priceMin < 2
    assert priceMax < 8
    assert priceMean < 5


def test_priceUpdateFailedBuyNormal(tradingFarmer):
    tradingFarmer.updatePriceBeliefs(marketPrice=8,
                                     act='BUY',
                                     commodityType='Wood',
                                     wasSuccess=False,
                                     unitPrice=5)
    priceMin, priceMax = tradingFarmer.getPriceBeliefsOf('Wood')
    priceMean = (priceMin + priceMax)/2

    assert priceMin > 2
    assert priceMax > 8
    assert priceMean > 5


def test_priceUpdateFailedSellNormal(tradingFarmer):
    tradingFarmer.updatePriceBeliefs(marketPrice=2,
                                     act='SELL',
                                     commodityType='Wood',
                                     wasSuccess=False,
                                     unitPrice=5)
    priceMin, priceMax = tradingFarmer.getPriceBeliefsOf('Wood')
    priceMean = (priceMin + priceMax)/2

    assert priceMin < 2
    assert priceMax < 8
    assert priceMean < 5


def test_priceUpdateFailedBuyLowInvent(tradingFarmer):
    tradingFarmer.inventory.setAmountOf('Wood', 1)
    tradingFarmer.inventory.setIdealAmount('Wood', 20)
    tradingFarmer.updatePriceBeliefs(marketPrice=8,
                                     act='BUY',
                                     commodityType='Wood',
                                     wasSuccess=False,
                                     unitPrice=5)
    priceMin, priceMax = tradingFarmer.getPriceBeliefsOf('Wood')
    priceMean = (priceMin + priceMax)/2

    assert priceMin < 3.25
    assert priceMax > 9.75
    assert priceMean > 5


def test_priceUpdateFailedSellHighInvent(tradingFarmer):
    tradingFarmer.inventory.setAmountOf('Wood', 15)
    tradingFarmer.inventory.setAmountOf('Food', 0)
    tradingFarmer.inventory.setIdealAmount('Wood', 5)
    tradingFarmer.updatePriceBeliefs(marketPrice=3,
                                     act='SELL',
                                     commodityType='Wood',
                                     wasSuccess=False,
                                     unitPrice=10)
    priceMin, priceMax = tradingFarmer.getPriceBeliefsOf('Wood')
    priceMean = (priceMin + priceMax)/2

    assert priceMin < 3
    assert priceMax < 8
    assert priceMean < 5
