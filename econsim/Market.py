import random
import logging
import statistics
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
        self.agentFraction = {}
        self.meanPricesOffered = {}
        self.meanPricesRequested = {}

    def setCommodityTypes(self, commodityTypes, agentTypes):
        for commodityType in commodityTypes:
            # We must initalise these with something or things will fail
            self.bids[commodityType] = []
            self.asks[commodityType] = []
            self.meanPrices[commodityType] = [1]
            self.totalUnitsBid[commodityType] = [0]
            self.totalUnitsAsk[commodityType] = [0]
            self.totalUnitsTraded[commodityType] = [0]
            self.totalMoneyTraded[commodityType] = [0]
            self.totalSuccessfullTrades[commodityType] = [0]
            self.meanPricesOffered[commodityType] = [1]
            self.meanPricesRequested[commodityType] = [1]

        for type in agentTypes:
            self.agentFraction[type] = [0]

    def bid(self, offer):
        commodityType = offer.commodityType
        self.bids[commodityType].append(offer)

    def ask(self, offer):
        commodityType = offer.commodityType
        self.asks[commodityType].append(offer)


class Market():

    marketRound = 1

    def __init__(self):

        self.agents = []
        self.book = TradeBook()
        self.commodityTypes = ['Food', 'Wood', 'Ore', 'Metal', 'Tools']
        self.whoMakesThisGood = {'Food': Farmer,
                                 'Wood': Woodcutter,
                                 'Ore': Miner,
                                 'Metal': Smelter,
                                 'Tools': Blacksmith}
        self.agentTypes = {'Farmer': Farmer,
                           'Woodcutter': Woodcutter,
                           'Miner': Miner,
                           'Smelter': Smelter,
                           'Blacksmith': Blacksmith}
        self.book.setCommodityTypes(
            self.commodityTypes, self.agentTypes.keys())
        self.hottestGood = None
        self.mostProfitableClass = None

    def bid(self, offer):
        self.book.bid(offer)

    def ask(self, offer):
        self.book.ask(offer)

    def getMeanPrice(self, commodityType):
        return self.getMeanPrices(commodityType, 1)

    def getLastNMeanPrices(self, commodityType, nPrices):
        return self.book.meanPrices[commodityType][-nPrices:]

    def getMeanPrices(self, commodityType, nPrices):
        return statistics.mean(self.getLastNMeanPrices(commodityType, nPrices))

    def getMeanOfferedPrices(self, commodityType, nPrices):
        return statistics.mean(self.getLastNMeanPricesOffered(commodityType, nPrices))

    def getLastNMeanPricesOffered(self, commodityType, nPrices):
        return self.book.meanPricesOffered[commodityType][-nPrices:]

    def getLastNMeanPricesRequested(self, commodityType, nPrices):
        return self.book.meanPricesRequested[commodityType][-nPrices:]

    def getMeanPricesOffered(self, commodityType, nPrices):
        return statistics.mean(self.getLastNMeanPricesOffered(commodityType, nPrices))

    def getDemand(self, commodityType, nLookback=1):
        return statistics.mean(self.book.totalUnitsBid[commodityType][-nLookback:])

    def getSupply(self, commodityType, nLookback=1):
        return statistics.mean(self.book.totalUnitsAsk[commodityType][-nLookback:])

    def getHottestGood(self, minimumRatio=1.5, nLookback=10):

        currentBestGood = None
        currentBestRatio = minimumRatio

        for commodityType in self.commodityTypes:
            supply = self.getSupply(commodityType, nLookback)
            demand = self.getDemand(commodityType, nLookback)
            if (supply == 0):
                supply = 0.5

            ratio = demand / supply

            if ratio > currentBestRatio:
                currentBestGood = commodityType
                currentBestRatio = ratio

        return currentBestGood

    def getMostProfitableClass(self, lastNDays=10):
        profits = {worker: 0 for worker in self.agentTypes.keys()}
        nWorkers = {worker: 0 for worker in self.agentTypes.keys()}

        for agent in self.agents:
            worker = agent.__class__.__name__
            profits[worker] += statistics.mean(agent.profit[-lastNDays:])
            nWorkers[worker] += 1

        for worker in profits.keys():
            if nWorkers[worker] > 0:
                profits[worker] = round(profits[worker]/nWorkers[worker], 2)

        mostProfit = max(profits, key=lambda key: profits[key])
        logger.info(f'Profits: {profits}')
        return mostProfit

    def returnLastBookValues(self, book):
        return [{key: round(book[key][-1], 2)} for key in book.keys()]

    def addNewAgent(self, agent):
        for commodityType in agent.inventory.getCommodityNames():
            agent.inventory.getCommodity(
                commodityType).initaliseObservedTrades(self)
        self.agents.append(agent)

    def decideReplacementClass(self):
        if self.hottestGood is not None:
            logger.info(f'Theres lots of demand for {self.hottestGood}!')
            return self.whoMakesThisGood[self.hottestGood]
        else:
            return self.agentTypes[self.mostProfitableClass]

    def simulate(self, n_rounds):
        for agent in self.agents:
            worker = agent.__class__.__name__

        for round in range(n_rounds):
            logger.info(f' ')
            logger.info(f'====== ROUND {Market.marketRound} =======')
            logger.info(f' ')
            self.produceAndGenerateAllOffers()
            self.resolveAllOffers()
            self.updateAgentFraction()
            logger.info(' ')
            logger.info(f'Fractions {self.book.agentFraction}')
            logger.info(
                f'Bids: {self.returnLastBookValues(self.book.totalUnitsBid)} ')
            logger.info(
                f'Asks: {self.returnLastBookValues(self.book.totalUnitsAsk)} ')
            logger.info(
                f'Mean Prices: {self.returnLastBookValues(self.book.meanPrices)} ')
            logger.info(
                f'Mean Prices Offered: {self.returnLastBookValues(self.book.meanPricesOffered)} ')
            logger.info(
                f'Mean Prices Requested: {self.returnLastBookValues(self.book.meanPricesRequested)} ')
            # Remove old agents and add new ones
            self.mostProfitableClass = self.getMostProfitableClass()
            self.hottestGood = self.getHottestGood()
            toBeRemoved = []
            toBeAdded = []
            for agent in self.agents:
                agent.profit.append(agent.money - agent.prevMoney)
                if agent.money <= 0:
                    newClass = self.decideReplacementClass()
                    toBeRemoved.append(agent)
                    toBeAdded.append(newClass())
                    logger.info(
                        f'{agent.name} was replaced with {toBeAdded[-1].name}')
            [self.agents.remove(agent) for agent in toBeRemoved]
            [self.addNewAgent(agent) for agent in toBeAdded]
            Market.marketRound += 1

    def produceAndGenerateAllOffers(self):
        for agent in self.agents:
            agent.prevMoney = agent.money
            agent.produce()
            for commodityType in self.commodityTypes:
                agent.generateOffers(commodityType, self)

    def resolveAllOffers(self):
        for commodityType in self.commodityTypes:
            self.resolveOffers(commodityType)

    def updateAgentFraction(self):
        nTotalAgents = 0
        nAgents = {type: 0 for type in self.agentTypes.keys()}
        for agent in self.agents:
            nTotalAgents += 1
            nAgents[agent.clarse] += 1
        self.book.agentFraction = {
            agentType: fraction / nTotalAgents for agentType, fraction in nAgents.items()}

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
        if len(asks) > 0:
            meanPricesOffered = sum([i.unitPrice for i in asks])/len(asks)
        else:
            meanPricesOffered = self.getLastNMeanPricesOffered(
                commodityType, 1)[0]
        if len(bids) > 0:
            meanPricesRequested = sum([i.unitPrice for i in bids])/len(bids)
        else:
            meanPricesRequested = self.getLastNMeanPricesRequested(
                commodityType, 1)[0]

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
        self.book.meanPricesOffered[commodityType].append(meanPricesOffered)
        self.book.meanPricesRequested[commodityType].append(
            meanPricesRequested)

        if unitsTraded > 0:
            meanPrice = moneyTraded/unitsTraded
        else:
            meanPrice = self.book.meanPrices[commodityType][-1]
            # meanPrice = meanPriceOffered

        # Get the mean price for the last several days
        lookbackTimeForMeanPrice = 2
        prevMeanPrices = self.getLastNMeanPrices(
            commodityType, lookbackTimeForMeanPrice)
        prevMeanPrices.append(meanPrice)
        meanPrice = statistics.mean(prevMeanPrices)

        self.book.meanPrices[commodityType].append(meanPrice)

    def transferGoods(self, commodityType, agentFrom, agentTo, amount):
        agentFrom.inventory.changeAmountOfCommodity(commodityType, -amount)
        agentTo.inventory.changeAmountOfCommodity(commodityType, amount)

    def transferMoney(self, agentFrom, agentTo, amount):
        agentFrom.money -= amount
        agentTo.money += amount
