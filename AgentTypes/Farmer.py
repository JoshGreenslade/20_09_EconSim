from AgentTypes.Peasant import Peasant


class Farmer(Peasant):

    id = 1
    foodOutput = 2

    def __init__(self):
        super(Farmer, self).__init__()
        self.inventory.setAmountOf('Food', 3)
        self.inventory.setAmountOf('Wood', 0)
        self.inventory.setAmountOf('Ore', 0)
        self.inventory.setAmountOf('Metal', 0)
        self.inventory.setAmountOf('Tools', 0)

        self.inventory.setIdealAmount('Food', 0)
        self.inventory.setIdealAmount('Wood', 3)
        self.inventory.setIdealAmount('Ore', 0)
        self.inventory.setIdealAmount('Metal', 0)
        self.inventory.setIdealAmount('Tools', 1)

        self.name = 'Bob the Farmer f' + str(Farmer.id)
        self.clarse = 'Farmer'
        Farmer.id += 1

    def produce(self):

        hasTools = self.queryInventory('Tools') > 0
        hasWood = self.queryInventory('Wood') > 0

        if Farmer.foodOutput > 0:
            if hasWood:
                if hasTools:
                    self._produce('Food', Farmer.foodOutput, 1)
                    self._consume('Wood', 1, 1)
                    self._consume('Tools', 1, 0.1)

                    commodityQuantities = {'Wood': 1, 'Tools': 0.1}
                    self.calcCostToProduce(commodityQuantities,
                                           totalProduced=Farmer.foodOutput)
                else:
                    self._produce('Food', 1, 1)
                    self._consume('Wood', 1, 1)

                    commodityQuantities = {'Wood': 1}
                    self.calcCostToProduce(commodityQuantities,
                                           totalProduced=1)
            else:
                # Fine the agent if they're not being productive.
                self._consume('Money', 2, 1)
        else:
            # Fine the agent if they're not being productive.
            self._consume('Money', 2, 1)
