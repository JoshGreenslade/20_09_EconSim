import logging
import random

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

    def queryInventory(self, commodityType):
        return self.inventory.getAmountOfCommodity(commodityType)

    def getPriceOf(self, commodityType):
        return self.inventory.getPriceOfCommodity(commodityType)

    def getPriceBeliefsOf(self, commodityType):
        return self.inventory.getPriceBeliefsOfCommodity(commodityType)

    def setPriceBeliefsOf(self, commodityType, priceLow, priceHigh):
        return self.inventory.setPriceBeliefsOfCommodity(commodityType, priceLow, priceHigh)

    def determinePurchaseQuantity(self, commodityType, marketPrice):
        minObsTrade, maxObsTrade = self.inventory.getTradingRangeOfCommodity(
            commodityType)
        favouribility = Utils.positionInRange(
            marketPrice,
            minObsTrade,
            maxObsTrade)
        favouribility = 1 - favouribility
        shortage = self.inventory.getShortage(commodityType)

        number_to_buy = round(favouribility * shortage * 1.0)
        return number_to_buy

    def determineSaleQuantity(self, commodityType, marketPrice):
        minObsTrade, maxObsTrade = self.inventory.getTradingRangeOfCommodity(
            commodityType)
        favouribility = Utils.positionInRange(
            marketPrice,
            minObsTrade,
            maxObsTrade)

        surplus = self.inventory.getSurplus(commodityType)
        number_to_sell = round(favouribility * surplus * 1.0)
        return max(1, number_to_sell)

    def _checkWillEventHappen(self, chance):
        return chance >= 1.0 or random.random() < chance

    def _produce(self, commodityType, amount, chance):
        if self._checkWillEventHappen(chance):
            self.inventory.changeAmountOfCommodity(commodityType, amount)

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

    def createBid(self, marketPrice, commodityType, maxToBuy):
        bidPrice = self.getPriceOf(commodityType)
        idealBidAmount = self.determinePurchaseQuantity(
            commodityType, marketPrice)
        quantityToBuy = min(idealBidAmount, maxToBuy)
        if quantityToBuy > 0:
            return Offer(self, commodityType, quantityToBuy, bidPrice)
        return None

    def createAsk(self, marketPrice, commodityType, minToSell):
        askPrice = self.getPriceOf(commodityType)
        idealAskAmount = self.determineSaleQuantity(commodityType, marketPrice)
        quantityToSell = max(idealAskAmount, minToSell)
        if quantityToSell > 0:
            return Offer(agent=self,
                         commodityType=commodityType,
                         units=quantityToSell,
                         unitPrice=askPrice)
        return None

    def generateOffers(self, market, commodityType):
        surplus = self.inventory.getSurplus(commodityType)
        shortage = self.inventory.getShortage(commodityType)
        marketPrice = market.getMeanPrice(commodityType)

        if surplus > 1:
            offer = self.createAsk(marketPrice, commodityType, 1)
            if offer:
                market.ask(offer)
        else:
            spareSpace = self.inventory.getSpareSpace()

            if shortage > 0 and spareSpace > 0:
                if shortage <= spareSpace:
                    maxToBuy = shortage
                else:
                    # I don't understand this line
                    maxToBuy = spareSpace

                if maxToBuy > 0:

                    offer = self.createBid(
                        marketPrice, commodityType, maxToBuy)
                    if offer:
                        market.bid(offer)

    def updatePriceBeliefs(self,
                           marketPrice,
                           act,
                           commodityType,
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

        if priceMin < self.MIN_PRICE:
            priceMin = self.MIN_PRICE
        if priceMax < self.MIN_PRICE:
            priceMax = self.MIN_PRICE

        self.inventory.setPriceBeliefsOfCommodity(
            commodityType, priceMin, priceMax)
