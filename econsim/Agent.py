import logging
import random
import math

from econsim.Commodity import Commodity
from econsim.Inventory import Inventory
from econsim.Offer import Offer
import econsim.Utils as Utils

logger = logging.getLogger(__name__)


class BasicAgent():

    agentID = 1

    def __init__(self):

        self.agentID = BasicAgent.agentID
        BasicAgent.agentID += 1

        self.name = 'Bob'
        self.clarse = 'None'
        self.money = 0
        self.prevMoney = 0
        self.inventory = Inventory()
        self.profit = []
        self.unitCost = 0

    def queryInventory(self, commodityType):
        return self.inventory.getAmountOfCommodity(commodityType)

    def getPriceOf(self, commodityType):
        return self.inventory.getPriceOfCommodity(commodityType)

    def getPriceBeliefsOf(self, commodityType):
        return self.inventory.getPriceBeliefsOfCommodity(commodityType)

    def getFavouribilityOf(self, commodityType, marketPrice):
        tradingRange = self.inventory.getTradingRangeOfCommodity(commodityType)
        minObsTrade = tradingRange[0]
        maxObsTrade = tradingRange[1]
        favouribility = Utils.positionInRange(
            marketPrice,
            minObsTrade,
            maxObsTrade)
        return favouribility

    def setPriceBeliefsOf(self, commodityType, priceLow, priceHigh):
        return self.inventory.setPriceBeliefsOfCommodity(commodityType, priceLow, priceHigh)

    def determinePurchaseQuantity(self, commodityType, marketPrice):
        favouribility = self.getFavouribilityOf(commodityType, marketPrice)
        favouribility = 1 - favouribility
        shortage = self.inventory.getShortage(commodityType)

        number_to_buy = round(favouribility * shortage * 1.0)
        return max(1, number_to_buy)

    def determineSaleQuantity(self, commodityType, marketPrice):
        favouribility = self.getFavouribilityOf(
            commodityType, marketPrice)
        surplus = self.inventory.getSurplus(commodityType)

        number_to_sell = round(favouribility * surplus * 1.0)
        return max(1, number_to_sell)

    def _checkWillEventHappen(self, chance):
        return chance >= 1.0 or random.random() < chance

    def _produce(self, commodityType, amount, chance):
        if self._checkWillEventHappen(chance):
            self.inventory.changeAmountOfCommodity(commodityType, amount)

    def calcCostToProduce(self, market, commodityQuantities, totalProduced):
        totalCost = sum([commodityQuantities[commodityType] * market.getMeanPrice(
            commodityType) for commodityType in commodityQuantities.keys()])
        self.unitCost = totalCost/totalProduced

    def _consume(self, commodityType, amount, chance):
        if self._checkWillEventHappen(chance):
            if commodityType == "Money":
                self.money -= amount
            else:
                self.inventory.changeAmountOfCommodity(commodityType, -amount)

    def produce(self):
        # Only implemented in subclasses (Farmer, blacksmith ect.)
        pass


class Agent(BasicAgent):

    def __init__(self):
        super(Agent, self).__init__()
        self.SIGNIFICANT = 0.25  # 25% more or less is is significant
        self.SIG_IMBALACE = 0.33
        self.LOW_INVENTORY = 0.1
        self.HIGH_INVENTORY = 2.0
        self.MIN_PRICE = 1.0
        self.MAX_SPEND_FRAC = 0.6

    def createBid(self, commodityType, marketPrice, maxToBuy):
        bidPrice = self.getPriceOf(commodityType)
        idealBidAmount = self.determinePurchaseQuantity(
            commodityType, marketPrice)
        affordableAmount = idealBidAmount

        # # Only buy if they can afford it
        # while affordableAmount*bidPrice > self.MAX_SPEND_FRAC * self.money:
        #     affordableAmount -= 1

        # if affordableAmount < idealBidAmount:
        #     logger.info(
        #         f'{self.name} can only afford {affordableAmount} rather than {idealBidAmount} at {bidPrice} unit price.')

        quantityToBuy = min(affordableAmount, maxToBuy)
        if quantityToBuy > 0:
            return Offer(self, 'BID', commodityType, quantityToBuy, bidPrice)
        return None

    def createAsk(self, commodityType, marketPrice, minToSell):
        askPrice = self.getPriceOf(commodityType)
        if askPrice < self.unitCost:  # If no profit, don't sell
            askPrice = self.unitCost*1.1

        idealAskAmount = self.determineSaleQuantity(commodityType, marketPrice)
        quantityToSell = max(idealAskAmount, minToSell)
        if quantityToSell > 0:
            return Offer(self,
                         'ASK',
                         commodityType,
                         quantityToSell,
                         askPrice)
        return None

    def makeRoomFor(self, commodityType, amount):
        amountReached = 0
        while amountReached < amount:
            for commodity in self.inventory.getCommodityNames():
                if commodity == commodityType:
                    continue
                if self.inventory.getSurplus((commodity)) > 0:
                    self.inventory.changeAmountOfCommodity(commodity, -1)
                    amountReached += 1
                    if amountReached >= amount:
                        break
        logger.info(
            f'{self.name} removed {amountReached} items')

    def generateOffers(self, commodityType, market):
        surplus = self.inventory.getSurplus(commodityType)
        shortage = self.inventory.getShortage(commodityType)
        marketPrice = market.getMeanPrice(commodityType)

        if surplus >= 1:
            offer = self.createAsk(commodityType, marketPrice, 1)
            if offer:
                market.ask(offer)
        else:
            spareSpace = self.inventory.getSpareSpace()

            if shortage > 0:
                # if spareSpace == 0:
                # logger.info(
                #     f'{self.name} has no space! Has a shortage of {shortage} {commodityType}')
                # self.makeRoomFor(commodityType, shortage)
                # spareSpace = self.inventory.getSpareSpace()

                if spareSpace >= 0:
                    if shortage <= spareSpace:
                        maxToBuy = shortage
                    else:
                        # I don't understand this line
                        maxToBuy = math.floor(spareSpace / shortage)

                    if maxToBuy > 0:

                        offer = self.createBid(
                            commodityType, marketPrice, maxToBuy)
                        if offer:
                            market.bid(offer)

    def updatePriceBeliefs(self,
                           commodityType,
                           marketPrice,
                           act,
                           wasSuccess,
                           unitPrice):

        if wasSuccess:
            self.inventory.addTradeOfCommodity(commodityType, unitPrice)

        publicPriceMean = marketPrice
        priceMin, priceMax = self.getPriceBeliefsOf(commodityType)
        priceMean = (priceMin + priceMax)/2
        deltaToMean = priceMean - publicPriceMean
        wobble = 0.05

        if wasSuccess:
            overpaid = act == 'BUY' and deltaToMean > publicPriceMean*self.SIGNIFICANT
            undersold = act == 'SELL' and deltaToMean < -publicPriceMean*self.SIGNIFICANT
            if overpaid or undersold:
                # Overpaid, shift towards mean
                priceMin -= deltaToMean / 2.
                priceMax -= deltaToMean / 2.
            # Increase certainty
            priceMin += wobble * priceMean
            priceMax -= wobble * priceMean
            self.MAX_SPEND_FRAC = 0.6

        else:
            currentStock = self.queryInventory(commodityType)
            idealStock = self.inventory.getIdealAmount(commodityType)

            # Shift towards mean
            priceMin -= deltaToMean / 2.
            priceMax -= deltaToMean / 2.

            lowInventory = act == 'BUY' and currentStock < self.LOW_INVENTORY * idealStock
            highInventory = act == 'SELL' and currentStock > self.HIGH_INVENTORY * idealStock

            if lowInventory or highInventory:
                wobble *= 2

            # Decrease certainty
            priceMin -= wobble * priceMean
            priceMax += wobble * priceMean

            self.MAX_SPEND_FRAC += 0.05
            if self.MAX_SPEND_FRAC > 1.0:
                self.MAX_SPEND_FRAC = 1.0

        if priceMin < self.MIN_PRICE:
            priceMin = self.MIN_PRICE
        if priceMax < priceMin:
            temp = priceMax * 1.0
            priceMax = priceMin
            priceMin = temp

        self.inventory.setPriceBeliefsOfCommodity(
            commodityType, priceMin, priceMax)
