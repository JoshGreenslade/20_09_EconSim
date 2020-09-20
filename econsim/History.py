import pylab as plt


class Plotter():

    def __init__(self):
        pass

    def plotAllPrices(self, market):
        for commodityType in market.commodityTypes:
            self.plotMeanPrice(commodityType, market)
        plt.legend()
        plt.grid()
        plt.show()

    def plotMeanPrice(self, commodityType, market):
        prices = market.book.meanPrices[commodityType]
        # agentFrac = market.book.agentFracion['Farmer']
        plt.plot(prices, label=commodityType)
        # plt.plot([i * 100 for i in agentFrac], )
