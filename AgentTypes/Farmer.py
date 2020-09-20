from AgentTypes.Peasant import Peasant


class Farmer(Peasant):

    id = 1

    def __init__(self):
        super(Farmer, self).__init__()
        self.inventory.setAmountOf('Food', 10)
        self.inventory.setAmountOf('Wood', 10)
        self.inventory.setAmountOf('Ore', 0)
        self.inventory.setAmountOf('Metal', 0)
        self.inventory.setAmountOf('Tools', 1)

        self.inventory.setIdealAmount('Food', 0)
        self.inventory.setIdealAmount('Wood', 8)
        self.inventory.setIdealAmount('Ore', 0)
        self.inventory.setIdealAmount('Metal', 0)
        self.inventory.setIdealAmount('Tools', 2)

        self.money = 100
        self.name = 'Bob the Farmer f' + str(Farmer.id)
        Farmer.id += 1

    def produce(self):

        hasTools = self.queryInventory('Tools') > 0
        hasWood = self.queryInventory('Wood') > 0

        if hasWood:
            if hasTools:
                self._produce('Food', 4, 1)
                self._consume('Wood', 1, 1)
                self._consume('Tools', 1, 0.1)
            else:
                self._produce('Food', 1, 1)
                self._consume('Wood', 1, 1)
        else:
            # Fine the agent if they're not being productive.
            self._consume('Money', 2, 1)
