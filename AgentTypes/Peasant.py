from econsim.Agent import Agent


class Peasant(Agent):

    def __init__(self):
        super(Peasant, self).__init__()
        self.name = self.name + ' the Peasant'
        self.inventory.max_size = 30
        self.money = 10

        self.inventory.setAmountOf('Food', 5)
        self.inventory.setAmountOf('Wood', 5)

        self.clarse = 'Peasant'

        self.inventory.setIdealAmount('Food', 8)
        self.inventory.setIdealAmount('Wood', 8)
        self.inventory.setPriceBeliefsOfCommodity('Food', 1.0, 20.0)
        self.inventory.setPriceBeliefsOfCommodity('Wood', 1.0, 20.0)

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
