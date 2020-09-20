class Offer():

    def __init__(self, agent, commodityType, units, unitPrice):

        self.agent = agent
        self.commodityType = commodityType
        self.units = units
        self.unitPrice = unitPrice

    def __repr__(self):
        return f'Agent ID: {self.agentID}, Commodity: {self.commodityType}, Units: {self.units}, Unit Price: {self.unitPrice}'
