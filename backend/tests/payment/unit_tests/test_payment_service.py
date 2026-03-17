import pytest
import backend.services.payment_service as payment_service_module
from backend.services.payment_service import PaymentService
from backend.models.payment.payment_model import PaymentStatus


class MockOrder:
    def __init__(self, order_id=1):
        self.id = order_id


class MockPayment:
    def __init__(
        self,
        id,
        order,
        card_name,
        card_number,
        security_number,
        expiration,
        status,
        amount,
    ):
        self.id = id
        self.order = order
        self.card_name = card_name
        self.card_number = card_number
        self.security_number = security_number
        self.expiration = expiration
        self.status = status
        self.amount = amount

    def validate(self):
        return True

    def processPayment(self):
        self.status = type("MockStatus", (), {"value": "accepted"})()
        return True

    def get_payment_info(self):
        return {
            "card_name": self.card_name,
            "amount": self.amount,
            "status": self.status.value if hasattr(self.status, "value") else self.status,
        }

    def request_fulfillment(self):
        return True


@pytest.fixture
def payment_service():
    return PaymentService()


@pytest.fixture
def order():
    return MockOrder()


# --- FR1: Retrieving Information ---

def test_create_payment_success(payment_service, order, monkeypatch):
    # Positive Functional Test: Payment object is created successfully
    monkeypatch.setattr(
        payment_service.cost_calculator,
        "calculateTotal",
        lambda order: 42.50
    )
    monkeypatch.setattr(payment_service_module, "Payment", MockPayment)

    data = {
        "card_name": "John Doe",
        "card_number": 1234567812345678,
        "security_number": 123,
        "expiration": "12/28",
    }

    result = payment_service.create_payment(order, data)

    assert result["success"] is True
    assert result["payment"].card_name == "John Doe"
    assert result["payment"].amount == 42.50
    assert result["payment"].status == PaymentStatus.DENIED


def test_create_payment_fails_when_cost_calculation_errors(payment_service, order, monkeypatch):
    # Edge Case: Return error if total calculation fails
    def raise_error(order):
        raise Exception("Calculation failed")

    monkeypatch.setattr(
        payment_service.cost_calculator,
        "calculateTotal",
        raise_error
    )

    result = payment_service.create_payment(order, {})

    assert result["success"] is False
    assert "Calculation failed" in result["error"]


def test_get_payment_info_success(payment_service):
    # Positive Functional Test: Payment info can be retrieved
    payment = MockPayment(
        id=1,
        order=MockOrder(),
        card_name="Jane Doe",
        card_number=1111222233334444,
        security_number=321,
        expiration="10/27",
        status=PaymentStatus.DENIED,
        amount=25.00,
    )

    result = payment_service.get_payment_info(payment)

    assert result["success"] is True
    assert result["payment_info"]["card_name"] == "Jane Doe"
    assert result["payment_info"]["amount"] == 25.00


def test_get_payment_info_failure(payment_service):
    # Edge Case: Return error if payment info retrieval fails
    class BrokenPayment:
        def get_payment_info(self):
            raise Exception("Could not retrieve payment info")

    result = payment_service.get_payment_info(BrokenPayment())

    assert result["success"] is False
    assert "Could not retrieve payment info" in result["error"]


# --- FR2: Complete data types ---

def test_validate_payment_success(payment_service):
    # Positive Functional Test: Valid payment passes validation
    class ValidPayment:
        def validate(self):
            return True

    result = payment_service.validate_payment(ValidPayment())

    assert result["success"] is True


def test_validate_payment_failure(payment_service):
    # Negative Edge Case: Invalid payment fails validation
    class InvalidPayment:
        def validate(self):
            return False

    result = payment_service.validate_payment(InvalidPayment())

    assert result["success"] is False
    assert "Invalid payment information" in result["error"]


# --- FR3: Integrated payment gateway ---

def test_process_payment_success(payment_service):
    # Positive Functional Test: Payment is processed successfully
    class ProcessablePayment:
        def __init__(self):
            self.status = type("MockStatus", (), {"value": "denied"})()

        def processPayment(self):
            self.status = type("MockStatus", (), {"value": "accepted"})()
            return True

    payment = ProcessablePayment()
    result = payment_service.process_payment(payment)

    assert result["success"] is True
    assert result["status"] == "accepted"


def test_process_payment_failure(payment_service):
    # Negative Edge Case: Payment is denied
    class DeniedPayment:
        def processPayment(self):
            return False

    result = payment_service.process_payment(DeniedPayment())

    assert result["success"] is False
    assert "Payment was denied" in result["error"]


# --- FR4: Fulfillment request ---

def test_request_fulfillment_success(payment_service):
    # Positive Functional Test: Fulfillment request succeeds for accepted payment
    class FulfillablePayment:
        def request_fulfillment(self):
            return True

    result = payment_service.request_fulfillment(FulfillablePayment())

    assert result["success"] is True


def test_request_fulfillment_failure(payment_service):
    # Negative Edge Case: Fulfillment fails if payment not accepted
    class UnfulfillablePayment:
        def request_fulfillment(self):
            return False

    result = payment_service.request_fulfillment(UnfulfillablePayment())

    assert result["success"] is False
    assert "Payment not accepted" in result["error"]


# --- Cost breakdown ---

def test_get_cost_breakdown_success(payment_service, order, monkeypatch):
    # Positive Functional Test: Cost breakdown is returned correctly
    expected_breakdown = {
        "subtotal": 20.00,
        "tax": 2.40,
        "fees": 1.60,
        "total": 24.00,
    }

    monkeypatch.setattr(
        payment_service.cost_calculator,
        "getBreakdown",
        lambda order: expected_breakdown
    )

    result = payment_service.get_cost_breakdown(order)

    assert result["success"] is True
    assert result["breakdown"] == expected_breakdown


def test_get_cost_breakdown_failure(payment_service, order, monkeypatch):
    # Edge Case: Return error if breakdown calculation fails
    def raise_error(order):
        raise Exception("Breakdown failed")

    monkeypatch.setattr(
        payment_service.cost_calculator,
        "getBreakdown",
        raise_error
    )

    result = payment_service.get_cost_breakdown(order)

    assert result["success"] is False
    assert "Breakdown failed" in result["error"]