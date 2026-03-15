import pytest
from unittest.mock import MagicMock
from backend.models.payment.payment_model import Payment, PaymentStatus


@pytest.fixture
def mock_order():
    order = MagicMock()
    order.id = 1
    return order


# Positive Validation Test: Valid payment passes validation
def test_validate_success(mock_order):
    payment = Payment(
        id=1,
        order=mock_order,
        card_name="John Doe",
        card_number=1234567812345678,
        security_number=123,
        expiration="12/26",
        status=PaymentStatus.DENIED,
        amount=50.0,
    )

    assert payment.validate() is True


# Negative Validation Test: Empty card name fails validation
def test_validate_empty_card_name(mock_order):
    payment = Payment(
        id=1,
        order=mock_order,
        card_name="",
        card_number=1234567812345678,
        security_number=123,
        expiration="12/26",
        status=PaymentStatus.DENIED,
        amount=50.0,
    )

    assert payment.validate() is False


# Negative Validation Test: Invalid card number fails validation
def test_validate_invalid_card_number(mock_order):
    payment = Payment(
        id=1,
        order=mock_order,
        card_name="John Doe",
        card_number=0,
        security_number=123,
        expiration="12/26",
        status=PaymentStatus.DENIED,
        amount=50.0,
    )

    assert payment.validate() is False


# Negative Validation Test: Invalid security number fails validation
def test_validate_invalid_security_number(mock_order):
    payment = Payment(
        id=1,
        order=mock_order,
        card_name="John Doe",
        card_number=1234567812345678,
        security_number=0,
        expiration="12/26",
        status=PaymentStatus.DENIED,
        amount=50.0,
    )

    assert payment.validate() is False


# Negative Validation Test: Empty expiration fails validation
def test_validate_empty_expiration(mock_order):
    payment = Payment(
        id=1,
        order=mock_order,
        card_name="John Doe",
        card_number=1234567812345678,
        security_number=123,
        expiration="",
        status=PaymentStatus.DENIED,
        amount=50.0,
    )

    assert payment.validate() is False


# Negative Validation Test: Non-positive amount fails validation
def test_validate_invalid_amount(mock_order):
    payment = Payment(
        id=1,
        order=mock_order,
        card_name="John Doe",
        card_number=1234567812345678,
        security_number=123,
        expiration="12/26",
        status=PaymentStatus.DENIED,
        amount=0.0,
    )

    assert payment.validate() is False


# Functional Test: Invalid payment processing sets status to denied
def test_process_payment_invalid_payment(mock_order):
    payment = Payment(
        id=1,
        order=mock_order,
        card_name="",
        card_number=1234567812345678,
        security_number=123,
        expiration="12/26",
        status=PaymentStatus.ACCEPTED,
        amount=50.0,
    )

    result = payment.processPayment()

    assert result is False
    assert payment.status == PaymentStatus.DENIED