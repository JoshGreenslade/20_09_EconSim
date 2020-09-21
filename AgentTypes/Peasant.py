from econsim.Agent import Agent


class Peasant(Agent):

    def __init__(self):
        super(Peasant, self).__init__()
        self.name = self.name + ' the Peasant'
        self.inventory.max_size = 10
        self.money = 100

        self.inventory.setAmountOf('Food', 0)
        self.inventory.setAmountOf('Wood', 0)
        self.inventory.setAmountOf('Ore', 0)
        self.inventory.setAmountOf('Metal', 0)
        self.inventory.setAmountOf('Tools', 0)

        self.clarse = 'Peasant'

        self.inventory.setIdealAmount('Food', 8)
        self.inventory.setIdealAmount('Wood', 8)
        self.inventory.setIdealAmount('Ore', 8)
        self.inventory.setIdealAmount('Metal', 8)
        self.inventory.setIdealAmount('Tools', 8)

    def produce(self):

        hasFood = self.queryInventory('Food') > 0
        hasWood = self.queryInventory('Wood') > 0

        if hasFood:
            self._consume('Food', 1, 1)
        elif hasWood:
            self._consume('Wood', 1, 1)
        else:
            # Fine the agent if they're not being productive.
            self._consume('Money', 2, 1)
