import pytest

from backend.models.payment.payment_service import PaymentService


class DummyItem:
    def __init__(self, price, quantity):
        self.price = price
        self.quantity = quantity


class DummyOrder:
    def __init__(self, items):
        self.items = items


def test_calculate_subtotal_valid():
    service = PaymentService()

    items = [
        DummyItem(price=10.0, quantity=2),
        DummyItem(price=5.0, quantity=3),
    ]
    order = DummyOrder(items)

    subtotal = service.calculate_subtotal(order)

    assert subtotal == 35.0


def test_calculate_subtotal_rounds_to_two_decimals():
    service = PaymentService()

    items = [
        DummyItem(price=10.555, quantity=1),
        DummyItem(price=2.333, quantity=1),
    ]
    order = DummyOrder(items)

    subtotal = service.calculate_subtotal(order)

    assert subtotal == 12.89


def test_calculate_subtotal_invalid_quantity():
    service = PaymentService()

    items = [
        DummyItem(price=10.0, quantity=0),
    ]
    order = DummyOrder(items)

    with pytest.raises(ValueError, match="item quantity must be positive"):
        service.calculate_subtotal(order)


def test_calculate_subtotal_negative_price():
    service = PaymentService()

    items = [
        DummyItem(price=-5.0, quantity=2),
    ]
    order = DummyOrder(items)

    with pytest.raises(ValueError, match="item price cannot be negative"):
        service.calculate_subtotal(order)


def test_calculate_subtotal_order_none():
    service = PaymentService()

    with pytest.raises(ValueError, match="order cannot be None"):
        service.calculate_subtotal(None)


def test_calculate_subtotal_order_missing_items():
    service = PaymentService()

    class BadOrder:
        pass

    order = BadOrder()

    with pytest.raises(ValueError, match="order must have items"):
        service.calculate_subtotal(order)


def test_calculate_subtotal_item_missing_price():
    service = PaymentService()

    class BadItem:
        def __init__(self):
            self.quantity = 2

    order = DummyOrder([BadItem()])

    with pytest.raises(ValueError, match="item must have price and quantity"):
        service.calculate_subtotal(order)


def test_calculate_subtotal_item_missing_quantity():
    service = PaymentService()

    class BadItem:
        def __init__(self):
            self.price = 10.0

    order = DummyOrder([BadItem()])

    with pytest.raises(ValueError, match="item must have price and quantity"):
        service.calculate_subtotal(order)


def test_calculate_subtotal_price_not_number():
    service = PaymentService()

    items = [
        DummyItem(price="10.0", quantity=2),
    ]
    order = DummyOrder(items)

    with pytest.raises(ValueError, match="item price must be a number"):
        service.calculate_subtotal(order)


def test_calculate_subtotal_quantity_not_integer():
    service = PaymentService()

    items = [
        DummyItem(price=10.0, quantity=2.5),
    ]
    order = DummyOrder(items)

    with pytest.raises(ValueError, match="item quantity must be an integer"):
        service.calculate_subtotal(order)


def test_calculate_subtotal_quantity_negative():
    service = PaymentService()

    items = [
        DummyItem(price=10.0, quantity=-1),
    ]
    order = DummyOrder(items)

    with pytest.raises(ValueError, match="item quantity must be positive"):
        service.calculate_subtotal(order)


def test_calculate_subtotal_empty_items():
    service = PaymentService()

    order = DummyOrder([])

    subtotal = service.calculate_subtotal(order)

    assert subtotal == 0.0