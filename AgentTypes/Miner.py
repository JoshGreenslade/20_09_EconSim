from AgentTypes.Peasant import Peasant


class Miner(Peasant):

    id = 1

    def __init__(self):
        super(Miner, self).__init__()
        self.inventory.setAmountOf('Food', 0)
        self.inventory.setAmountOf('Wood', 0)
        self.inventory.setAmountOf('Ore', 10)
        self.inventory.setAmountOf('Metal', 0)
        self.inventory.setAmountOf('Tools', 1)

        self.inventory.setIdealAmount('Food', 8)
        self.inventory.setIdealAmount('Wood', 0)
        self.inventory.setIdealAmount('Ore', 0)
        self.inventory.setIdealAmount('Metal', 0)
        self.inventory.setIdealAmount('Tools', 2)

        self.money = 100
        self.name = 'Jerry the Miner m' + str(Miner.id)
        Miner.id += 1

    def produce(self):

        hasTools = self.queryInventory('Tools') > 0
        hasFood = self.queryInventory('Food') > 0

        if hasFood and hasTools:
            self._produce('Ore', 2, 1)
            self._consume('Food', 1, 1)
            self._consume('Tools', 1, 0.1)
        else:
            self._consume('Money', 2, 1)
