import pylab as plt
import numpy


def running_mean(x, N):
    cumsum = numpy.cumsum(numpy.insert(x, 0, 0))
    return (cumsum[N:] - cumsum[:-N]) / float(N)


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
        prices = running_mean(prices, 20)
        # agentFrac = market.book.agentFracion['Farmer']
        plt.plot(prices, label=commodityType)
        # plt.plot([i * 100 for i in agentFrac], )
