from AgentTypes.Peasant import Peasant


class Smelter(Peasant):

    id = 1

    def __init__(self):
        super(Smelter, self).__init__()
        self.inventory.setAmountOf('Food', 0)
        self.inventory.setAmountOf('Wood', 0)
        self.inventory.setAmountOf('Ore', 5)
        self.inventory.setAmountOf('Metal', 2)
        self.inventory.setAmountOf('Tools', 1)

        self.inventory.setIdealAmount('Food', 8)
        self.inventory.setIdealAmount('Wood', 0)
        self.inventory.setIdealAmount('Ore', 20)
        self.inventory.setIdealAmount('Metal', 0)
        self.inventory.setIdealAmount('Tools', 2)

        self.money = 100
        self.name = 'Sam the Smelty s' + str(Smelter.id)
        Smelter.id += 1

    def produce(self):

        hasTools = self.queryInventory('Tools') > 0
        hasOre = self.queryInventory('Ore') > 0
        oreAmount = self.queryInventory('Ore')
        hasFood = self.queryInventory('Food') > 0

        if hasFood and hasTools and hasOre:
            self._produce('Metal', self.queryInventory('Ore'), 1)
            self._consume('Ore', self.queryInventory('Ore'), 1)
            self._consume('Tools', 1, 0.1)

        else:
            self._consume('Money', 2, 1)
