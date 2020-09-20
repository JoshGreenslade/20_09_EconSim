class Offer():

    def __init__(self, agent, type, commodityType, units, unitPrice):

        self.agent = agent
        self.type = type
        self.commodityType = commodityType
        self.units = units
        self.unitPrice = unitPrice

    def __repr__(self):
        return f'''
Agent ID: {self.agent.name}
Type: {self.type}
Commodity: {self.commodityType}
Units: {self.units}
Unit Price: {self.unitPrice}
'''
