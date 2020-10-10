import pylab as plt
import numpy
import math


def running_mean(x, N):
    cumsum = numpy.cumsum(numpy.insert(x, 0, 0))
    return (cumsum[N:] - cumsum[:-N]) / float(N)


class Plotter():

    def __init__(self):
        pass

    def plotAllPrices(self, market):
        for commodityType in market.commodityTypes:
            self.plotMeanPrice(commodityType, market)
            # self.plotMeanPriceOffered(commodityType, market)
        plt.legend()
        plt.grid()
        plt.show()

    def plotMeanPrice(self, commodityType, market):
        prices = market.book.meanPrices[commodityType]
        # prices = running_mean(prices, 10)
        plt.plot(prices, label=commodityType, lw=3)

    def plotMeanPriceOffered(self, commodityType, market):
        prices = market.book.meanPricesOffered[commodityType]
        prices = running_mean(prices, 20)
        plt.plot(prices, label='Off: ' + commodityType, lw=3)
