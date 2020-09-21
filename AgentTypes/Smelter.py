from AgentTypes.Peasant import Peasant


class Smelter(Peasant):

    id = 1

    def __init__(self):
        super(Smelter, self).__init__()
        self.inventory.setAmountOf('Food', 1)
        self.inventory.setAmountOf('Wood', 0)
        self.inventory.setAmountOf('Ore', 0)
        self.inventory.setAmountOf('Metal', 0)
        self.inventory.setAmountOf('Tools', 1)

        self.inventory.setIdealAmount('Food', 3)
        self.inventory.setIdealAmount('Wood', 0)
        self.inventory.setIdealAmount('Ore', 5)
        self.inventory.setIdealAmount('Metal', 0)
        self.inventory.setIdealAmount('Tools', 1)

        self.name = 'Sam the Smelty s' + str(Smelter.id)
        Smelter.id += 1

    def produce(self, market):

        hasTools = self.queryInventory('Tools') > 0
        hasOre = self.queryInventory('Ore') > 0
        oreAmount = self.queryInventory('Ore')
        hasFood = self.queryInventory('Food') > 0

        if hasFood and hasOre:
            if hasTools:
                self._produce('Metal', oreAmount, 1)
                self._consume('Ore', oreAmount, 1)
                self._consume('Tools', 1, 0.1)
                self._consume('Food', 1, 1)

                commodityQuantities = {
                    'Ore': oreAmount, 'Tools': 0.1, 'Food': 0.1}
                self.calcCostToProduce(market,
                                       commodityQuantities,
                                       totalProduced=oreAmount)
            else:
                maxToProduce = self.queryInventory('Ore')
                if maxToProduce > 2:
                    maxToProduce = 2
                self._produce('Metal', maxToProduce, 1)
                self._consume('Ore', maxToProduce, 1)
                self._consume('Food', 1, 1)

                commodityQuantities = {'Ore': maxToProduce, 'Food': 1}
                self.calcCostToProduce(market,
                                       commodityQuantities,
                                       totalProduced=maxToProduce)
        else:
            self._consume('Money', 2, 1)
