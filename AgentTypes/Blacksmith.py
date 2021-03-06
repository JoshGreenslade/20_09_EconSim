from AgentTypes.Peasant import Peasant
import math


class Blacksmith(Peasant):

    id = 1

    def __init__(self):
        super(Blacksmith, self).__init__()
        self.inventory.setAmountOf('Food', 0)
        self.inventory.setAmountOf('Wood', 0)
        self.inventory.setAmountOf('Ore', 0)
        self.inventory.setAmountOf('Metal', 0)
        self.inventory.setAmountOf('Tools', 3)

        self.inventory.setIdealAmount('Food', 3)
        self.inventory.setIdealAmount('Wood', 3)
        self.inventory.setIdealAmount('Ore', 0)
        self.inventory.setIdealAmount('Metal', 3)
        self.inventory.setIdealAmount('Tools', 0)

        self.name = 'Bart the Blacksmith B' + str(Blacksmith.id)
        self.clarse = 'Blacksmith'
        Blacksmith.id += 1

    def produce(self):

        hasMetal = self.queryInventory('Metal') > 0
        hasFood = self.queryInventory('Food') > 0
        hasWood = self.queryInventory('Wood') > 0
        amountMetal = self.queryInventory('Metal')

        if hasFood and hasMetal and hasWood:

            self._produce('Tools', amountMetal, 1)
            self._consume('Metal', amountMetal, 1)
            self._consume('Wood', amountMetal, 1)
            self._consume('Food', 1, 1)

            commodityQuantities = {'Metal': amountMetal, 'Food': 1, 'Wood': 1}
            self.calcCostToProduce(commodityQuantities,
                                   totalProduced=amountMetal)

        else:
            self._consume('Money', 2, 1)
