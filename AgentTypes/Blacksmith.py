from AgentTypes.Peasant import Peasant
import math


class Blacksmith(Peasant):

    id = 1

    def __init__(self):
        super(Blacksmith, self).__init__()
        self.inventory.setAmountOf('Food', 0)
        self.inventory.setAmountOf('Wood', 0)
        self.inventory.setAmountOf('Ore', 0)
        self.inventory.setAmountOf('Metal', 10)
        self.inventory.setAmountOf('Tools', 0)

        self.inventory.setIdealAmount('Food', 8)
        self.inventory.setIdealAmount('Wood', 0)
        self.inventory.setIdealAmount('Ore', 0)
        self.inventory.setIdealAmount('Metal', 15)
        self.inventory.setIdealAmount('Tools', 0)

        self.money = 100
        self.name = 'Bart the Blacksmith B' + str(Blacksmith.id)
        Blacksmith.id += 1

        self.metalPerTool = 5

    def produce(self):

        hasMetal = self.queryInventory('Metal') > self.metalPerTool
        hasFood = self.queryInventory('Food') > 0
        amountTools = math.floor(
            self.queryInventory('Metal')/self.metalPerTool)

        if hasFood and hasMetal:

            self._produce('Tools', amountTools, 1)
            self._consume('Metal', amountTools*self.metalPerTool, 1)
            self._consume('Food', 1, 1)

        else:
            self._consume('Money', 2, 1)
