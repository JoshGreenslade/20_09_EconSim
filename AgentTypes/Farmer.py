from AgentTypes.Peasant import Peasant


class Farmer(Peasant):

    def __init__(self):
        super(Farmer, self).__init__()
        self.inventory.setAmountOf('Food', 15)
        self.inventory.setAmountOf('Wood', 5)
        self.money = 30
        self.name = self.name + ' the Farmer'

    def produce(self):

        hasTools = self.queryInventory('Tools') > 0
        hasWood = self.queryInventory('Wood') > 0

        if hasWood:
            if hasTools:
                self._produce('Food', 4, 1)
                self._consume('Wood', 1, 1)
                self._consume('Tools', 1, 0.1)
            else:
                self._produce('Food', 2, 1)
                self._consume('Wood', 1, 1)
        else:
            # Fine the agent if they're not being productive.
            self._consume('Money', 2, 1)
