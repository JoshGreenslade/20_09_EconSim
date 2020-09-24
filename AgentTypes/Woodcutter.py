from AgentTypes.Peasant import Peasant


class Woodcutter(Peasant):

    id = 1

    def __init__(self):
        super(Woodcutter, self).__init__()
        self.inventory.setAmountOf('Food', 3)
        self.inventory.setAmountOf('Wood', 0)
        self.inventory.setAmountOf('Ore', 0)
        self.inventory.setAmountOf('Metal', 0)
        self.inventory.setAmountOf('Tools', 1)

        self.inventory.setIdealAmount('Food', 3)
        self.inventory.setIdealAmount('Wood', 0)
        self.inventory.setIdealAmount('Ore', 0)
        self.inventory.setIdealAmount('Metal', 0)
        self.inventory.setIdealAmount('Tools', 1)

        self.name = 'Alice the Woodcutter w' + str(Woodcutter.id)
        Woodcutter.id += 1

    def produce(self):

        hasTools = self.queryInventory('Tools') > 0
        hasFood = self.queryInventory('Food') > 0

        if hasFood:
            if hasTools:
                self._produce('Wood', 2, 1)
                self._consume('Food', 1, 1)
                self._consume('Tools', 1, 0.1)

                commodityQuantities = {'Food': 1, 'Tools': 0.1}
                self.calcCostToProduce(commodityQuantities,
                                       totalProduced=2)
            else:
                self._produce('Wood', 1, 1)
                self._consume('Food', 1, 1)

                commodityQuantities = {'Food': 1}
                self.calcCostToProduce(commodityQuantities,
                                       totalProduced=1)
        else:
            self._consume('Money', 2, 1)
