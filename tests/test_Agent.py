import pytest
import econsim
import AgentTypes


from econsim.Commodity import Commodity
from econsim.Inventory import Inventory
from AgentTypes import Farmer, Woodcutter


@pytest.fixture
def farmer():
    farmer = Farmer.Farmer()
    farmer.setPriceBeliefsOf('Food', 2, 8)
    farmer.setPriceBeliefsOf('Wood', 2, 8)
    farmer.setPriceBeliefsOf('Tools', 2, 8)
    farmer.inventory.max_size = 100
    return farmer


@pytest.fixture
def tradingFarmer():
    farmer = Farmer.Farmer()
    farmer.setPriceBeliefsOf('Food', 2, 8)
    farmer.setPriceBeliefsOf('Wood', 2, 8)
    farmer.setPriceBeliefsOf('Tools', 2, 8)
    farmer.inventory.max_size = 100
    farmer.inventory.addTradeOfCommodity('Wood', 2)
    farmer.inventory.addTradeOfCommodity('Wood', 8)
    farmer.inventory.addTradeOfCommodity('Food', 2)
    farmer.inventory.addTradeOfCommodity('Food', 8)
    return farmer


def test_checkFarmerDefaultSetup(farmer):
    farmer.inventory.setAmountOf('Food', 10)
    farmer.inventory.setAmountOf('Wood', 10)
    farmer.money = 30

    assert farmer.queryInventory('Food') == 10
    assert farmer.queryInventory('Wood') == 10
    assert farmer.money == 30


def test_checkFarmerProductionWithoutTools(farmer):
    farmer.inventory.setAmountOf('Food', 10)
    farmer.inventory.setAmountOf('Wood', 10)
    farmer.inventory.setAmountOf('Tools', 0)
    farmer.produce()
    assert farmer.queryInventory('Food') == 12
    assert farmer.queryInventory('Wood') == 9


def test_checkFarmerProductionWithTools(farmer):
    farmer.inventory.setAmountOf('Food', 10)
    farmer.inventory.setAmountOf('Wood', 10)
    farmer.inventory.setAmountOf('Tools', 10)
    farmer.produce()
    assert farmer.queryInventory('Food') == 14
    assert farmer.queryInventory('Wood') == 9


def test_checkToolsGetDestroyed(farmer):
    farmer.inventory.setAmountOf('Tools', 1)
    n_attempts = 0
    while farmer.queryInventory('Tools') > 0:
        farmer.inventory.setAmountOf('Food', 10)
        farmer.inventory.setAmountOf('Wood', 10)
        farmer.produce()
        n_attempts += 1
    assert n_attempts > 0


def test_checkGetFined(farmer):
    initalMoney = farmer.money
    farmer.inventory.setAmountOf('Wood', 0)
    farmer.produce()
    assert farmer.money == initalMoney - 2


def test_settingPrice(tradingFarmer):
    tradingFarmer.setPriceBeliefsOf('Wood', 5, 10)
    assert tradingFarmer.getPriceBeliefsOf('Wood') == [5, 10]


def test_determinePurchaseQuantity(tradingFarmer):
    tradingFarmer.inventory.max_size = 10
    tradingFarmer.inventory.setAmountOf('Wood', 5)
    tradingFarmer.inventory.setIdealAmount('Wood', 10)
    food = tradingFarmer.inventory.getCommodity('Wood')
    food.observedTrades = [4, 5, 6, 5, 5]

    assert tradingFarmer.determinePurchaseQuantity('Wood', 2) == 5
    assert tradingFarmer.determinePurchaseQuantity('Wood', 10) == 1
    assert tradingFarmer.determinePurchaseQuantity('Wood', 5) == 2


def test_determineSaleQuantity(tradingFarmer):
    tradingFarmer.inventory.max_size = 10
    tradingFarmer.inventory.setAmountOf('Wood', 15)
    tradingFarmer.inventory.setIdealAmount('Wood', 10)
    food = tradingFarmer.inventory.getCommodity('Wood')
    food.observedTrades = [4, 5, 6, 5, 5]

    assert tradingFarmer.determineSaleQuantity('Wood', 2) == 1
    assert tradingFarmer.determineSaleQuantity('Wood', 10) == 5
    assert tradingFarmer.determineSaleQuantity('Wood', 5) == 2


def test_createBid(tradingFarmer):
    tradingFarmer.inventory.setAmountOf('Wood', 5)
    tradingFarmer.inventory.setIdealAmount('Wood', 10)
    offer = tradingFarmer.createBid('Wood', 2, 10)
    minPrice, maxPrice = tradingFarmer.getPriceBeliefsOf('Wood')
    assert offer.units == 5
    assert offer.commodityType == 'Wood'
    assert (offer.unitPrice >= minPrice) & (offer.unitPrice <= maxPrice)
    tradingFarmer.inventory.setAmountOf('Wood', 5)
    tradingFarmer.inventory.setIdealAmount('Wood', 10)
    offer = tradingFarmer.createBid('Wood', 5, 10)
    minPrice, maxPrice = tradingFarmer.getPriceBeliefsOf('Wood')
    assert offer.units == 2
    assert offer.commodityType == 'Wood'
    assert (offer.unitPrice >= minPrice) & (offer.unitPrice <= maxPrice)


def test_createAsk(tradingFarmer):
    tradingFarmer.inventory.setAmountOf('Wood', 15)
    tradingFarmer.inventory.setIdealAmount('Wood', 10)
    offer = tradingFarmer.createAsk('Wood', 1, 1)
    minPrice, maxPrice = tradingFarmer.getPriceBeliefsOf('Wood')
    assert offer.units == 1
    assert offer.commodityType == 'Wood'
    assert (offer.unitPrice >= minPrice) & (offer.unitPrice <= maxPrice)
    tradingFarmer.inventory.setAmountOf('Wood', 15)
    tradingFarmer.inventory.setIdealAmount('Wood', 10)
    offer = tradingFarmer.createAsk('Wood', 5, 1)
    minPrice, maxPrice = tradingFarmer.getPriceBeliefsOf('Wood')
    assert offer.units == 2
    assert offer.commodityType == 'Wood'
    assert (offer.unitPrice >= minPrice) & (offer.unitPrice <= maxPrice)
