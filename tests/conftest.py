import pytest
from unittest.mock import Mock
from praktikum.bun import Bun
from praktikum.ingredient import Ingredient
from praktikum.ingredient_types import INGREDIENT_TYPE_SAUCE

@pytest.fixture
def mock_bun():
    bun = Mock(spec=Bun)
    bun.get_name.return_value = "Black Bun"
    bun.get_price.return_value = 100.0
    return bun


@pytest.fixture
def mock_ingredient():
    ing = Mock(spec=Ingredient)
    ing.get_type.return_value = INGREDIENT_TYPE_SAUCE
    ing.get_name.return_value = "Hot Sauce"
    ing.get_price.return_value = 50.0
    return ing

