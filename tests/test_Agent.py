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
    farmer.produce()
    assert farmer.queryInventory('Food') == 12
    assert farmer.queryInventory('Wood') == 9


def test_checkFarmerProductionWithTools(farmer):
    farmer.inventory.setAmountOf('Tools', 10)
    farmer.inventory.setAmountOf('Food', 10)
    farmer.inventory.setAmountOf('Wood', 10)
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
    assert n_attempts > 1


def test_checkGetFined(farmer):
    farmer.inventory.setAmountOf('Wood', 0)
    farmer.produce()
    assert farmer.money == 28


def test_settingPrice(tradingFarmer):
    tradingFarmer.setPriceBeliefsOf('Wood', 5, 10)
    assert tradingFarmer.getPriceBeliefsOf('Wood') == [5, 10]


def test_determinePurchaseQuantity(tradingFarmer):
    tradingFarmer.inventory.setAmountOf('Wood', 5)
    tradingFarmer.inventory.setIdealAmount('Wood', 10)

    assert tradingFarmer.determinePurchaseQuantity('Wood', 2) == 5
    assert tradingFarmer.determinePurchaseQuantity('Wood', 10) == 0
    assert tradingFarmer.determinePurchaseQuantity('Wood', 5) == 2


def test_determineSaleQuantity(tradingFarmer):
    tradingFarmer.inventory.setAmountOf('Wood', 15)
    tradingFarmer.inventory.setIdealAmount('Wood', 10)

    assert tradingFarmer.determineSaleQuantity('Wood', 2) == 1
    assert tradingFarmer.determineSaleQuantity('Wood', 10) == 5
    assert tradingFarmer.determineSaleQuantity('Wood', 5) == 2


def test_createBid(tradingFarmer):
    tradingFarmer.inventory.setAmountOf('Wood', 5)
    tradingFarmer.inventory.setIdealAmount('Wood', 10)
    offer = tradingFarmer.createBid(2, 'Wood', 10)
    minPrice, maxPrice = tradingFarmer.getPriceBeliefsOf('Wood')
    assert offer.units == 5
    assert offer.commodityType == 'Wood'
    assert (offer.unitPrice >= minPrice) & (offer.unitPrice <= maxPrice)
    tradingFarmer.inventory.setAmountOf('Wood', 5)
    tradingFarmer.inventory.setIdealAmount('Wood', 10)
    offer = tradingFarmer.createBid(5, 'Wood', 10)
    minPrice, maxPrice = tradingFarmer.getPriceBeliefsOf('Wood')
    assert offer.units == 2
    assert offer.commodityType == 'Wood'
    assert (offer.unitPrice >= minPrice) & (offer.unitPrice <= maxPrice)


def test_createAsk(tradingFarmer):
    tradingFarmer.inventory.setAmountOf('Wood', 15)
    tradingFarmer.inventory.setIdealAmount('Wood', 10)
    offer = tradingFarmer.createAsk(1, 'Wood', 1)
    minPrice, maxPrice = tradingFarmer.getPriceBeliefsOf('Wood')
    assert offer.units == 1
    assert offer.commodityType == 'Wood'
    assert (offer.unitPrice >= minPrice) & (offer.unitPrice <= maxPrice)
    tradingFarmer.inventory.setAmountOf('Wood', 15)
    tradingFarmer.inventory.setIdealAmount('Wood', 10)
    offer = tradingFarmer.createAsk(5, 'Wood', 1)
    minPrice, maxPrice = tradingFarmer.getPriceBeliefsOf('Wood')
    assert offer.units == 2
    assert offer.commodityType == 'Wood'
    assert (offer.unitPrice >= minPrice) & (offer.unitPrice <= maxPrice)


def test_generateOffersSurplus(tradingFarmer):
    tradingFarmer.inventory.setAmountOf('Wood', 15)
    tradingFarmer.inventory.setIdealAmount('Wood', 10)
    offer = tradingFarmer.generateOffers(10, 'Wood')
    assert offer.units == 5
    offer = tradingFarmer.generateOffers(1, 'Wood')
    assert offer.units == 1
    offer = tradingFarmer.generateOffers(5, 'Wood')
    assert offer.units == 2


def test_generateOffersShortageWithSpace(tradingFarmer):
    tradingFarmer.inventory.setAmountOf('Wood', 5)
    tradingFarmer.inventory.setIdealAmount('Wood', 10)
    offer = tradingFarmer.generateOffers(10, 'Wood')
    assert offer is None
    offer = tradingFarmer.generateOffers(1, 'Wood')
    assert offer.units == 5
    offer = tradingFarmer.generateOffers(5, 'Wood')
    assert offer.units == 2


def test_generateOffersShortageWithoutSpace(tradingFarmer):
    tradingFarmer.inventory.max_size = 20
    tradingFarmer.inventory.setAmountOf('Wood', 6)
    tradingFarmer.inventory.setIdealAmount('Wood', 8)
    offer = tradingFarmer.generateOffers(1, 'Wood')
    assert offer.units == 2
