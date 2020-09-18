from econsim.Agent import Agent


class Woodcutter(Agent):

    def produce(self):

        hasTools = self.queryInventory('Tools') > 0
        hasFood = self.queryInventory('Food') > 0

        if hasFood:
            if hasTools:
                self._produce('Wood', 2, 1)
                self._consume('Food', 1, 1)
                self._consume('Tools', 1, 0.1)
            else:
                self._produce('Wood', 1, 1)
                self._consume('Food', 1, 1)
        else:
            self._consume('Money', 2, 1)
