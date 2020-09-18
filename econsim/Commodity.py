import logging
import random
logger = logging.getLogger(__name__)


class Commodity():

    def __init__(self, commodityName, commodityAmount):

        self.name = commodityName
        self.amount = commodityAmount
        self.priceLower = random.randint(0, 15)
        self.priceUpper = round(self.priceLower + random.randint(0, 10) + 1)

    def __repr__(self):
        return f'{self.amount}'

    def estimate_price(self):
        priceRange = self.priceUpper - self.priceLower
        priceEstimate = self.priceLower + round(priceRange*random.random())
        return priceEstimate

    def changeAmount(self, amount):
        self.amount += amount
        if self.amount < 0:
            self.amount = 0
