from econsim.Commodity import Commodity


class Inventory():

    max_size = 0

    def __init__(self):

        self.inventory = {}

    def __repr__(self):
        return self.inventory

    def addCommodity(self, commodityType):
        self.inventory[commodityType] = Commodity(commodityType)

    def getCommodityNames(self):
        return [i for i in self.inventory.keys()]

    def getCommodity(self, commodityType):
        return self.inventory[commodityType]

    def getAmountOfCommodity(self, commodityType):
        self.ensureCommodityExists(commodityType)
        return self.getCommodity(commodityType).amount

    def getPriceOfCommodity(self, commodityType):
        return self.getCommodity(commodityType).estimatePrice()

    def getPriceBeliefsOfCommodity(self, commodityType):
        return self.getCommodity(commodityType).getPriceBeliefs()

    def setPriceBeliefsOfCommodity(self, commodityType, priceLow, priceHigh):
        return self.getCommodity(commodityType).setPriceBeliefs(priceLow, priceHigh)

    def getTradingRangeOfCommodity(self, commodityType):
        return self.getCommodity(commodityType).getTradingRange()

    def addTradeOfCommodity(self, commodityType, unitPrice):
        return self.getCommodity(commodityType).addTrade(unitPrice)

    def setAmountOf(self, commodityType, amount):
        self.ensureCommodityExists(commodityType)
        self.getCommodity(commodityType).amount = amount

    def changeAmountOfCommodity(self, commodityType, changeByThisAmount):
        self.ensureCommodityExists(commodityType)
        self.getCommodity(commodityType).changeAmount(changeByThisAmount)
        self.ensureAmountOfCommodityIsSane(commodityType)

    def ensureAmountOfCommodityIsSane(self, commodityType):
        if self.getAmountOfCommodity(commodityType) < 0:
            self.setAmountOf(commodityType, 0)
        if self.getAmountOfCommodity(commodityType) > self.max_size:
            self.setAmountOf(commodityType, self.max_size)

    def checkCommodityExists(self, commodityType):
        return commodityType in self.getCommodityNames()

    def ensureCommodityExists(self, commodityType):
        if not self.checkCommodityExists(commodityType):
            self.addCommodity(commodityType)

    def getUsedSpace(self):
        return sum([self.getAmountOfCommodity(i) for i in self.getCommodityNames()])

    def getSpareSpace(self):
        return self.max_size - self.getUsedSpace()

    def getSurplus(self, commodityType):
        return self.getCommodity(commodityType).getSurplus()

    def getShortage(self, commodityType):
        return self.getCommodity(commodityType).getShortage()

    def getIdealAmount(self, commodityType):
        return self.getCommodity(commodityType).idealAmount

    def ensureAmountSensible(self, amount):
        if amount < 0:
            amount = 0
        if amount > self.max_size:
            amount = self.max_size
        return amount

    def setIdealAmount(self, commodityType, amount):
        amount = self.ensureAmountSensible(amount)
        self.getCommodity(commodityType).idealAmount = amount
