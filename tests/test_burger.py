import pytest
from unittest.mock import Mock
from praktikum.burger import Burger
from praktikum.ingredient import Ingredient
from praktikum.ingredient_types import INGREDIENT_TYPE_SAUCE, INGREDIENT_TYPE_FILLING

def test_set_buns(mock_bun):
    burger = Burger()
    burger.set_buns(mock_bun)
    assert burger.bun == mock_bun


def test_add_ingredient(mock_ingredient):
    burger = Burger()
    burger.add_ingredient(mock_ingredient)
    assert len(burger.ingredients) == 1
    assert burger.ingredients[0] == mock_ingredient

@pytest.mark.parametrize("index", [0, 1, 2])
def test_remove_ingredient_valid(index):
    burger = Burger()
    for _ in range(3):
        burger.add_ingredient(Mock(spec=Ingredient))
    expected_len = len(burger.ingredients) - 1
    burger.remove_ingredient(index)
    assert len(burger.ingredients) == expected_len


def test_remove_ingredient_invalid_index():
    burger = Burger()
    burger.add_ingredient(Mock(spec=Ingredient))
    with pytest.raises(IndexError):
        burger.remove_ingredient(5)


@pytest.mark.parametrize("old, new, expected_order", [
    (0, 1, [1, 0, 2]),
    (2, 0, [2, 0, 1]),
    (1, 1, [0, 1, 2]),
])
def test_move_ingredient_valid(old, new, expected_order):
    burger = Burger()
    ingredients = [Mock(spec=Ingredient) for _ in range(3)]
    for ing in ingredients:
        burger.add_ingredient(ing)
    burger.move_ingredient(old, new)
    for i, idx in enumerate(expected_order):
        assert burger.ingredients[i] == ingredients[idx]


def test_move_ingredient_invalid_old_index():
    burger = Burger()
    burger.add_ingredient(Mock(spec=Ingredient))
    with pytest.raises(IndexError):
        burger.move_ingredient(5, 0)


def test_move_ingredient_invalid_new_index():
    burger = Burger()
    burger.add_ingredient(Mock(spec=Ingredient))
    burger.add_ingredient(Mock(spec=Ingredient))
    original_ingredients = burger.ingredients.copy()
    burger.move_ingredient(0, 5)
    assert len(burger.ingredients) == 2
    assert burger.ingredients[1] == original_ingredients[0]


def test_get_price_with_bun_and_ingredients(mock_bun, mock_ingredient):
    burger = Burger()
    burger.set_buns(mock_bun)
    burger.add_ingredient(mock_ingredient)
    expected = mock_bun.get_price() * 2 + mock_ingredient.get_price()
    assert burger.get_price() == expected


def test_get_price_with_bun_only(mock_bun):
    burger = Burger()
    burger.set_buns(mock_bun)
    expected = mock_bun.get_price() * 2
    assert burger.get_price() == expected


def test_get_price_without_bun(mock_ingredient):
    burger = Burger()
    burger.add_ingredient(mock_ingredient)
    with pytest.raises(AttributeError):
        burger.get_price()


def test_get_receipt_with_bun_and_ingredients(mock_bun, mock_ingredient):
    burger = Burger()
    burger.set_buns(mock_bun)
    burger.add_ingredient(mock_ingredient)

    expected_lines = [
        f'(==== {mock_bun.get_name()} ====)',
        f'= {mock_ingredient.get_type().lower()} {mock_ingredient.get_name()} =',
        f'(==== {mock_bun.get_name()} ====)\n',
        f'Price: {burger.get_price()}'
    ]
    expected = '\n'.join(expected_lines)

    assert burger.get_receipt() == expected


def test_get_receipt_with_bun_only(mock_bun):
    burger = Burger()
    burger.set_buns(mock_bun)

    expected_lines = [
        f'(==== {mock_bun.get_name()} ====)',
        f'(==== {mock_bun.get_name()} ====)\n',
        f'Price: {burger.get_price()}'
    ]
    expected = '\n'.join(expected_lines)

    assert burger.get_receipt() == expected


def test_get_receipt_without_bun(mock_ingredient):
    burger = Burger()
    burger.add_ingredient(mock_ingredient)
    with pytest.raises(AttributeError):
        burger.get_receipt()


def test_get_receipt_multiple_ingredients(mock_bun):
    burger = Burger()
    burger.set_buns(mock_bun)

    ing1 = Mock(spec=Ingredient)
    ing1.get_type.return_value = INGREDIENT_TYPE_SAUCE
    ing1.get_name.return_value = "Sauce A"
    ing1.get_price.return_value = 30

    ing2 = Mock(spec=Ingredient)
    ing2.get_type.return_value = INGREDIENT_TYPE_FILLING
    ing2.get_name.return_value = "Filling B"
    ing2.get_price.return_value = 70

    burger.add_ingredient(ing1)
    burger.add_ingredient(ing2)
    expected_lines = [
        f'(==== {mock_bun.get_name()} ====)',
        f'= {ing1.get_type().lower()} {ing1.get_name()} =',
        f'= {ing2.get_type().lower()} {ing2.get_name()} =',
        f'(==== {mock_bun.get_name()} ====)\n',
        f'Price: {burger.get_price()}'
    ]
    expected = '\n'.join(expected_lines)

    assert burger.get_receipt() == expected