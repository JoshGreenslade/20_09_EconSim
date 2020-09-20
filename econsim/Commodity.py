import logging
import random
logger = logging.getLogger(__name__)


class Commodity():

    def __init__(self, commodityName):

        self.name = commodityName
        self.amount = 0
        self.idealAmount = 0
        self.priceLower = 0.0
        self.priceUpper = 1.0
        self.observedTrades = [random.randint(0, 20) for i in range(5)]
        self.maxObservedTrades = 20

    def __repr__(self):
        return f'{self.amount}'

    def estimatePrice(self):
        priceRange = self.priceUpper - self.priceLower
        priceEstimate = self.priceLower + round(priceRange*random.random())
        return priceEstimate

    def getPriceBeliefs(self):
        return [self.priceLower, self.priceUpper]

    def setPriceBeliefs(self, priceLow, priceHigh):
        self.priceLower = priceLow
        self.priceUpper = priceHigh

    def getTradingRange(self):
        if len(self.observedTrades) >= 2:
            return [min(self.observedTrades), max(self.observedTrades)]
        else:
            return [1.0, 20.0]

    def addTrade(self, trade):
        self.observedTrades.append(trade)
        if len(self.observedTrades) > self.maxObservedTrades:
            self.observedTrades = self.observedTrades[-self.maxObservedTrades:]

    def changeAmount(self, amount):
        self.amount += amount

    def setAmount(self, amount):
        self.amount = amount

    def getSurplus(self):
        surplus = self.amount - self.idealAmount
        return surplus if surplus > 0 else 0

    def getShortage(self):
        shortage = self.idealAmount - self.amount
        return shortage if shortage > 0 else 0
