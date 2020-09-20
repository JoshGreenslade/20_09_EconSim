import pytest
import econsim

from econsim.Commodity import Commodity


@pytest.fixture
def commodity0Food():
    """ Returns a Food commodity with zero amount """
    food = Commodity('Food')
    return food


@pytest.fixture
def commodity10Food():
    """ Returns a Food commodity with ten amount """
    food = Commodity('Food')
    food.setAmount(10)
    return food


def test_setAmount(commodity0Food):
    commodity0Food.setAmount(10)
    assert commodity0Food.amount == 10


def test_positiveChangeAmount(commodity10Food):
    commodity10Food.changeAmount(3)
    assert commodity10Food.amount == 13


def test_negativeChangeAmount(commodity10Food):
    commodity10Food.changeAmount(-6)
    assert commodity10Food.amount == 4


def test_surplus(commodity10Food):
    commodity10Food.idealAmount = 5
    assert commodity10Food.getSurplus() == 5
    commodity10Food.setAmount(3)
    assert commodity10Food.getSurplus() == 0


def test_shortage(commodity10Food):
    commodity10Food.idealAmount = 15
    assert commodity10Food.getShortage() == 5
    commodity10Food.setAmount(18)
    assert commodity10Food.getShortage() == 0


def test_getPriceBeliefs(commodity0Food):
    priceLow, priceHigh = commodity0Food.getPriceBeliefs()
    assert priceLow == 0
    assert priceHigh == 1


def test_setPriceBeliefs(commodity0Food):
    commodity0Food.setPriceBeliefs(5, 15)
    priceLow, priceHigh = commodity0Food.priceLower, commodity0Food.priceUpper
    assert priceLow == 5
    assert priceHigh == 15
