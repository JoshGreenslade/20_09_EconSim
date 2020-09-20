import pytest
import econsim

from econsim.Commodity import Commodity
from econsim.Inventory import Inventory


@pytest.fixture
def emptyInventory():
    inventory = Inventory()
    inventory.max_size = 20
    return inventory


@pytest.fixture
def inventoryWith10Food():
    inventory = Inventory()
    inventory.max_size = 20
    inventory.setAmountOf('Food', 10)
    return inventory


def test_addCommodityToInventory(emptyInventory):
    emptyInventory.addCommodity('Food')
    assert 'Food' in emptyInventory.inventory.keys()
    assert emptyInventory.inventory['Food'].amount == 0


def test_autoAddCommodity(emptyInventory):
    emptyInventory.setAmountOf('Food', 10)
    assert emptyInventory.getAmountOfCommodity('Food') == 10


def test_getAmountOfCommodity(inventoryWith10Food):
    assert inventoryWith10Food.getAmountOfCommodity('Food') == 10


def test_changeAmountOfCommodityNegative(inventoryWith10Food):
    inventoryWith10Food.changeAmountOfCommodity('Food', -3)
    assert inventoryWith10Food.getAmountOfCommodity('Food') == 7


def test_changeAmountOfCommodityPositive(inventoryWith10Food):
    inventoryWith10Food.changeAmountOfCommodity('Food', 4)
    assert inventoryWith10Food.getAmountOfCommodity('Food') == 14


def test_maxSizeObeyed(inventoryWith10Food):
    inventoryWith10Food.setAmountOf('Food', 15)
    inventoryWith10Food.changeAmountOfCommodity('Food', 50)
    assert inventoryWith10Food.getAmountOfCommodity('Food') == 20


def test_checkUsedSpace(inventoryWith10Food):
    inventoryWith10Food.setAmountOf('Wood', 5)
    assert inventoryWith10Food.getUsedSpace() == 15


def test_checkSpareSpace(inventoryWith10Food):
    inventoryWith10Food.setAmountOf('Wood', 5)
    assert inventoryWith10Food.getSpareSpace() == 5


def test_Surplus(inventoryWith10Food):
    inventoryWith10Food.setIdealAmount('Food', 5)
    assert inventoryWith10Food.getSurplus('Food') == 5
    inventoryWith10Food.setIdealAmount('Food', 15)
    assert inventoryWith10Food.getSurplus('Food') == 0


def test_Shortage(inventoryWith10Food):
    inventoryWith10Food.setIdealAmount('Food', 15)
    assert inventoryWith10Food.getShortage('Food') == 5
    inventoryWith10Food.setIdealAmount('Food', 5)
    assert inventoryWith10Food.getShortage('Food') == 0
