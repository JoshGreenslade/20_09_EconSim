import logging
from econsim.Commodity import Commodity
logger = logging.getLogger(__name__)


class Agent():

    agentID = 1

    def __init__(self):

        self.name = 'Bob'
        self.money = 0
        self.inventory = {'Food': Commodity('Food', 10),
                          'Wood': Commodity('Wood', 10)}
        self.starving = False
        self.bankrupt = False

    def ensureInventoryItemExists(self, commodityType):
        if commodityType not in self.inventory.keys():
            self.inventory[commodityType] = Commodity(commodityType, 0)

    def queryInventory(self, commodityType):
        self.ensureInventoryItemExists(commodityType)
        return self.inventory[commodityType].amount

    def _produce(self, commodityType, amount, chance):
        if chance >= 1.0 or random.random() < chance:
            self.inventory[commodityType].changeAmount(amount)

    def _consume(self, commodityType, amount, chance):
        if chance >= 1.0 or random.random() < chance:
            if commodityType == "money":
                self.money -= amount
            else:
                self.inventory[commodityType].changeAmount(-amount)
