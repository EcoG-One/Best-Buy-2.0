import pytest
from products import Product


def test_normal_product_creation():
    '''
    Tests that creating a normal product works.
    '''
    product = Product("Test Product", price=10, quantity=100)
    assert product.name == "Test Product"
    assert product.price == 10
    assert product.quantity == 100
    assert product.active == True


def test_invalid_product_creation():
    '''
    Tests that creating a product with invalid details (empty name,
    negative price) invokes an exception.
    '''
    with pytest.raises(ValueError):
        Product("", price=10, quantity=100)  # Empty name

    with pytest.raises(ValueError):
        Product("Test Product", price=-10, quantity=100) # negative price


def test_product_becomes_inactive():
    '''
    Tests that when a product reaches 0 quantity, it becomes inactive.
    '''
    product = Product("Test Product", price=10, quantity=1)
    product.buy(1)
    assert product.active == False


def test_product_purchase():
    '''
    Tests that product purchase modifies the quantity and returns
    the right output.
    '''
    product = Product("Test Product", price=10, quantity=10)
    total_price = product.buy(3)
    assert product.quantity == 7
    assert total_price == 30


def test_buy_larger_quantity_than_exists():
    '''
    Tests that buying a larger quantity than exists invokes exception.
    '''
    product = Product("Test Product", price=10, quantity=5)
    with pytest.raises(ValueError):
        product.buy(10)
