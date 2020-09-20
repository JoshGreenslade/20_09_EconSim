import random
import logging
from AgentTypes.Farmer import Farmer
from AgentTypes.Woodcutter import Woodcutter
from AgentTypes.Miner import Miner
from AgentTypes.Smelter import Smelter
from AgentTypes.Blacksmith import Blacksmith


logger = logging.getLogger(__name__)


class TradeBook():

    def __init__(self):
        self.bids = {}
        self.asks = {}
        self.meanPrices = {}
        self.totalUnitsBid = {}
        self.totalUnitsAsk = {}
        self.totalUnitsTraded = {}
        self.totalMoneyTraded = {}
        self.totalSuccessfullTrades = {}
        self.agentFracion = {}

    def setCommodityTypes(self, commodityTypes, agentTypes):
        for commodityType in commodityTypes:
            # We must initalise these with something or things will fail
            self.bids[commodityType] = []
            self.asks[commodityType] = []
            self.meanPrices[commodityType] = [10]
            self.totalUnitsBid[commodityType] = [0]
            self.totalUnitsAsk[commodityType] = [0]
            self.totalUnitsTraded[commodityType] = [0]
            self.totalMoneyTraded[commodityType] = [0]
            self.totalSuccessfullTrades[commodityType] = [0]
        for type in agentTypes:
            self.agentFracion[type] = [0]

    def bid(self, offer):
        commodityType = offer.commodityType
        self.bids[commodityType].append(offer)

    def ask(self, offer):
        commodityType = offer.commodityType
        self.asks[commodityType].append(offer)


class Market():

    def __init__(self):

        self.agents = []
        self.book = TradeBook()
        self.commodityTypes = ['Food', 'Wood', 'Ore', 'Metal', 'Tools']
        self.agentTypes = {'Farmer': Farmer,
                           'Woodcutter': Woodcutter,
                           'Miner': Miner,
                           'Smelter': Smelter,
                           'Blacksmith': Blacksmith}
        self.book.setCommodityTypes(
            self.commodityTypes, self.agentTypes.keys())

    def getMostProfitableClass(self, lastNDays):
        profits = {worker: 0 for worker in self.agentTypes.keys()}
        for agent in self.agents:
            worker = agent.__class__.__name__
            profits[worker] += sum(agent.profit[-lastNDays:])
        mostProfit = max(profits, key=lambda key: profits[key])
        return self.agentTypes[mostProfit]

    def updateFractionOfClasses(self):
        agentTypeNumbers = {type: 0 for type in self.agentTypes.keys()}
        for agent in self.agents:
            type = agent.__class__.__name__
            agentTypeNumbers[type] += 1
        nAgents = len(self.agents)*1.0
        for agentType in self.book.agentFracion.keys():
            self.book.agentFracion[agentType].append(
                agentTypeNumbers[agentType]/nAgents)

    def returnLastBookValues(self, book):
        return [{key: book[key][-1]} for key in book.keys()]

    def simulate(self, n_rounds):
        for agent in self.agents:
            worker = agent.__class__.__name__

        for round in range(n_rounds):
            logger.info(f' ')
            logger.info(f'====== ROUND {round} =======')
            logger.info(f' ')
            self.updateFractionOfClasses()
            self.produceAndGenerateAllOffers()
            self.resolveAllOffers()
            logger.info(
                f'Bids: {self.returnLastBookValues(self.book.totalUnitsBid)} ')
            logger.info(
                f'Asks: {self.returnLastBookValues(self.book.totalUnitsAsk)} ')
            # logger.info(f'Asks: {[key:self.book.unitsAsk[key][-1] for key in self.book.unitsAsk.keys()]} ')

            # Remove old agents and add new ones
            toBeRemoved = []
            toBeAdded = []
            for agent in self.agents:
                agent.profit.append(agent.money - agent.prevMoney)
                if agent.money <= 0:
                    newClass = self.getMostProfitableClass(lastNDays=30)
                    toBeRemoved.append(agent)
                    toBeAdded.append(newClass())
                    logger.info(
                        f'{agent.name} was replaced with {toBeAdded[-1].name}')
            [self.agents.remove(agent) for agent in toBeRemoved]
            [self.agents.append(agent) for agent in toBeAdded]

    def produceAndGenerateAllOffers(self):
        for agent in self.agents:
            agent.prevMoney = agent.money
            agent.produce()
            for commodityType in self.commodityTypes:
                agent.generateOffers(commodityType, self)

    def resolveAllOffers(self):
        for commodityType in self.commodityTypes:
            self.resolveOffers(commodityType)

    def resolveOffers(self, commodityType):

        nTrades = 0
        unitsBid = 0
        unitsAsk = 0
        unitsTraded = 0
        moneyTraded = 0
        successfulTrades = 0

        bids = self.book.bids[commodityType]
        asks = self.book.asks[commodityType]

        random.shuffle(bids)
        random.shuffle(asks)

        unitsBid = sum([i.units for i in bids])
        unitsAsk = sum([i.units for i in asks])

        if len(bids) > 0 and len(asks) > 0:
            bids = sorted(bids, key=lambda x: x.unitPrice, reverse=True)
            asks = sorted(asks, key=lambda x: x.unitPrice, reverse=False)

        while len(bids) > 0 and len(asks) > 0:

            buyerOffer = bids[0]
            sellerOffer = asks[0]

            seller = sellerOffer.agent
            buyer = buyerOffer.agent

            quantityTraded = min(buyerOffer.units, sellerOffer.units)
            clearingPrice = (buyerOffer.unitPrice + sellerOffer.unitPrice)/2.0

            if quantityTraded > 0:

                # Transfer Goods and Money
                sellerOffer.units -= quantityTraded
                buyerOffer.units -= quantityTraded

                self.transferGoods(commodityType=commodityType,
                                   agentFrom=seller,
                                   agentTo=buyer,
                                   amount=quantityTraded)
                self.transferMoney(agentFrom=buyer,
                                   agentTo=seller,
                                   amount=quantityTraded * clearingPrice)

            # Update beliefs
            seller.updatePriceBeliefs(marketPrice=self.book.meanPrices[commodityType][-1],
                                      act='SELL',
                                      commodityType=commodityType,
                                      wasSuccess=True,
                                      unitPrice=clearingPrice)
            buyer.updatePriceBeliefs(marketPrice=self.book.meanPrices[commodityType][-1],
                                     act='BUY',
                                     commodityType=commodityType,
                                     wasSuccess=True,
                                     unitPrice=clearingPrice)

            # Log stats
            moneyTraded += quantityTraded * clearingPrice
            unitsTraded += quantityTraded
            successfulTrades += 1

            logger.info(
                f'{seller.name} sold {quantityTraded} units of {commodityType} for {buyer.name} for {clearingPrice} gold a peice!')

            # Drop offers with no remaining units
            if buyerOffer.units == 0:
                bids = bids[1:]
            if sellerOffer.units == 0:
                asks = asks[1:]

        # Reject all other bids
        while len(bids) > 0:
            buyerOffer = bids[0]
            buyer = buyerOffer.agent
            buyer.updatePriceBeliefs(marketPrice=self.book.meanPrices[commodityType][-1],
                                     act='BUY',
                                     commodityType=commodityType,
                                     wasSuccess=False,
                                     unitPrice=0)  # Unitprice is not used if unsucessfull
            bids = bids[1:]

        while len(asks) > 0:
            sellerOffer = asks[0]
            seller = sellerOffer.agent
            seller.updatePriceBeliefs(marketPrice=self.book.meanPrices[commodityType][-1],
                                      act='SELL',
                                      commodityType=commodityType,
                                      wasSuccess=False,
                                      unitPrice=0)  # Unitprice is not used if unsucessfull
            asks = asks[1:]

        # Tidy up the book
        self.book.bids[commodityType] = []
        self.book.asks[commodityType] = []
        self.book.totalUnitsBid[commodityType].append(unitsBid)
        self.book.totalUnitsAsk[commodityType].append(unitsAsk)
        self.book.totalUnitsTraded[commodityType].append(unitsTraded)
        self.book.totalMoneyTraded[commodityType].append(moneyTraded)
        self.book.totalSuccessfullTrades[commodityType].append(
            successfulTrades)

        if unitsTraded > 0:
            meanPrice = moneyTraded/unitsTraded
        else:
            meanPrice = self.book.meanPrices[commodityType][-1]
        self.book.meanPrices[commodityType].append(meanPrice)

    def transferGoods(self, commodityType, agentFrom, agentTo, amount):
        agentFrom.inventory.changeAmountOfCommodity(commodityType, -amount)
        agentTo.inventory.changeAmountOfCommodity(commodityType, amount)

    def transferMoney(self, agentFrom, agentTo, amount):
        agentFrom.money -= amount
        agentTo.money += amount

    def bid(self, offer):
        self.book.bid(offer)

    def ask(self, offer):
        self.book.ask(offer)

    def getMeanPrice(self, commodityType):
        return self.book.meanPrices[commodityType][-1]

    def getMeanPrices(self, commodityType, nPrices):
        return self.book.meanPrices[commodityType][:-n]
