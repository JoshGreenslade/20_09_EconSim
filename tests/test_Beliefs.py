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
    wood = tradingFarmer.inventory.getCommodity('Wood')
    wood.setPriceBeliefs(2, 8)
    tradingFarmer.updatePriceBeliefs(marketPrice=5.0,
                                     act='SELL',
                                     commodityType='Wood',
                                     wasSuccess=True,
                                     unitPrice=6.0)
    priceMin, priceMax = tradingFarmer.getPriceBeliefsOf('Wood')
    priceMean = (priceMin + priceMax)/2

    assert priceMin > 2.0
    assert priceMax < 8.0
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
    wood = tradingFarmer.inventory.getCommodity('Wood')
    wood.setPriceBeliefs(3, 7)
    tradingFarmer.updatePriceBeliefs(marketPrice=8,
                                     act='BUY',
                                     commodityType='Wood',
                                     wasSuccess=False,
                                     unitPrice=5)
    priceMin, priceMax = tradingFarmer.getPriceBeliefsOf('Wood')
    priceMean = (priceMin + priceMax)/2

    assert priceMin > 3
    assert priceMax > 7
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


def test_makingSensibleBidCase1(farmer):
    ''' Farmer has no food. Ideal is 10. Observed price is cheap.
        Farmer should try to buy 10.
    '''
    farmer.inventory.setAmountOf('Food', 0)
    farmer.inventory.setIdealAmount('Food', 10)
    farmer.inventory.max_space = 250
    farmer.money = 250

    food = farmer.inventory.getCommodity('Food')
    food.setPriceBeliefs(10, 20)
    food.observedTrades = [10, 10, 10, 10, 10]

    marketPrice = 1
    bidPrice = farmer.getPriceOf('Food')
    maxToBuy = 10
    purchaseQuantity = farmer.determinePurchaseQuantity('Food', marketPrice)
    offer = farmer.createBid('Food', marketPrice, maxToBuy)

    assert farmer.inventory.getShortage('Food') == 10
    assert purchaseQuantity == 10
    assert offer.units == 10
    assert (offer.unitPrice >= 10) & (offer.unitPrice <= 20)
    assert offer.commodityType == 'Food'


def test_makingSensibleBidCase2(farmer):
    ''' Farmer has no food. Ideal is 10. Observed price is average.
        Farmer should try to buy 5.
    '''
    farmer.inventory.setAmountOf('Food', 0)
    farmer.inventory.setIdealAmount('Food', 10)
    farmer.inventory.max_space = 100

    food = farmer.inventory.getCommodity('Food')
    food.setPriceBeliefs(10, 20)
    food.observedTrades = [10, 10, 10, 10, 10]

    marketPrice = 10
    bidPrice = farmer.getPriceOf('Food')

    purchaseQuantity = farmer.determinePurchaseQuantity('Food', marketPrice)
    spareSpace = farmer.inventory.getSpareSpace()
    shortage = farmer.inventory.getShortage('Food')
    if shortage > 0 and spareSpace > 0:
        if shortage <= spareSpace:
            maxToBuy = shortage
        else:
            # I don't understand this line
            maxToBuy = spareSpace
    offer = farmer.createBid('Food', marketPrice, maxToBuy)

    assert spareSpace > 0
    assert shortage > 0
    assert purchaseQuantity == 5
    assert offer.units == 5
    assert (offer.unitPrice >= 10) & (offer.unitPrice <= 20)
    assert offer.commodityType == 'Food'


def test_makingSensibleBidCase3(farmer):
    ''' Farmer has no food. Ideal is 10. Observed price is high.
        Farmer should try to buy at least one.
    '''
    farmer.inventory.setAmountOf('Food', 0)
    farmer.inventory.setIdealAmount('Food', 10)
    farmer.inventory.max_space = 100

    food = farmer.inventory.getCommodity('Food')
    food.setPriceBeliefs(10, 20)
    food.observedTrades = [10, 10, 10, 10, 10]

    marketPrice = 20
    bidPrice = farmer.getPriceOf('Food')

    purchaseQuantity = farmer.determinePurchaseQuantity('Food', marketPrice)
    spareSpace = farmer.inventory.getSpareSpace()
    shortage = farmer.inventory.getShortage('Food')
    if shortage > 0 and spareSpace > 0:
        if shortage <= spareSpace:
            maxToBuy = shortage
        else:
            # I don't understand this line
            maxToBuy = spareSpace
    offer = farmer.createBid('Food', marketPrice, maxToBuy)

    assert spareSpace > 0
    assert shortage > 0
    assert purchaseQuantity == 1
    assert (offer.units > 0) and (offer.units < 5)
    assert (offer.unitPrice >= 10) & (offer.unitPrice <= 20)
    assert offer.commodityType == 'Food'


def test_makingEdgeBidCase1(farmer):
    ''' Farmer has 5 food. Ideal is 10. Observed price is low.
        Farmer has only 3 space.
        Farmer should try to buy 3
    '''
    farmer.inventory.setAmountOf('Food', 7)
    farmer.inventory.setAmountOf('Wood', 0)
    farmer.inventory.setIdealAmount('Food', 10)
    farmer.inventory.max_space = 10

    food = farmer.inventory.getCommodity('Food')
    food.setPriceBeliefs(10, 20)
    food.observedTrades = [10, 10, 10, 10, 10]

    marketPrice = 5
    bidPrice = farmer.getPriceOf('Food')

    purchaseQuantity = farmer.determinePurchaseQuantity('Food', marketPrice)
    spareSpace = farmer.inventory.getSpareSpace()
    shortage = farmer.inventory.getShortage('Food')
    if shortage > 0 and spareSpace > 0:
        if shortage <= spareSpace:
            maxToBuy = shortage
        else:
            # I don't understand this line
            maxToBuy = spareSpace
    offer = farmer.createBid('Food', marketPrice, maxToBuy)

    assert spareSpace > 0
    assert shortage > 0
    assert purchaseQuantity == 3
    assert (offer.units == 3)
    assert (offer.unitPrice >= 10) & (offer.unitPrice <= 20)
    assert offer.commodityType == 'Food'


def test_makingSensibleAskCase1(farmer):
    ''' Farmer has 15 food. Ideal is 10. Observed price is high.
        Farmer should try to sell 5.
    '''
    farmer.inventory.setAmountOf('Food', 15)
    farmer.inventory.setIdealAmount('Food', 10)
    farmer.inventory.max_space = 100

    food = farmer.inventory.getCommodity('Food')
    food.setPriceBeliefs(10, 20)
    food.observedTrades = [10, 10, 10, 10, 10]

    marketPrice = 15
    bidPrice = farmer.getPriceOf('Food')
    minToSell = 1
    saleQuantity = farmer.determineSaleQuantity('Food', marketPrice)
    offer = farmer.createAsk('Food', marketPrice, minToSell)

    assert farmer.inventory.getSurplus('Food') == 5
    assert saleQuantity == 5
    assert offer.units == 5
    assert (offer.unitPrice >= 10) & (offer.unitPrice <= 20)
    assert offer.commodityType == 'Food'


def test_makingSensibleBidCase2(farmer):
    ''' Farmer has 15 food. Ideal is 10. Observed price is average.
        Farmer should try to sell 2.
    '''
    farmer.inventory.setAmountOf('Food', 15)
    farmer.inventory.setIdealAmount('Food', 10)
    farmer.inventory.max_space = 100

    food = farmer.inventory.getCommodity('Food')
    food.setPriceBeliefs(10, 20)
    food.observedTrades = [10, 10, 10, 10, 10]

    marketPrice = 10
    bidPrice = farmer.getPriceOf('Food')
    minToSell = 1
    saleQuantity = farmer.determineSaleQuantity('Food', marketPrice)
    offer = farmer.createAsk('Food', marketPrice, minToSell)

    assert farmer.inventory.getSurplus('Food') == 5
    assert saleQuantity == 2
    assert offer.units == 2
    assert (offer.unitPrice >= 10) & (offer.unitPrice <= 20)
    assert offer.commodityType == 'Food'


def test_makingSensibleBidCase3(farmer):
    ''' Farmer has no food. Ideal is 10. Observed price is low.
        Farmer should try to sell at least one.
    '''
    farmer.inventory.setAmountOf('Food', 15)
    farmer.inventory.setIdealAmount('Food', 10)
    farmer.inventory.max_space = 100

    food = farmer.inventory.getCommodity('Food')
    food.setPriceBeliefs(10, 20)
    food.observedTrades = [10, 10, 10, 10, 10]

    marketPrice = 5
    bidPrice = farmer.getPriceOf('Food')
    minToSell = 1
    saleQuantity = farmer.determineSaleQuantity('Food', marketPrice)
    offer = farmer.createAsk('Food', marketPrice, minToSell)

    assert farmer.inventory.getSurplus('Food') == 5
    assert saleQuantity == 1
    assert offer.units == 1
    assert (offer.unitPrice >= 10) & (offer.unitPrice <= 20)
    assert offer.commodityType == 'Food'
