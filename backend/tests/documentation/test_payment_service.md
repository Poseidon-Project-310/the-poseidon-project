This test script verifies the main functionality of the PaymentService class using mock versions of the payment model and cost calculator so the tests depend only on the service logic.

It checks that create_payment() correctly creates a payment object, fills in provided card details, calculates the amount, and uses default values when fields are missing. It tests that get_payment_info() returns payment details correctly and also handles failures when payment information cannot be retrieved.

It verifies that validate_payment() returns success for a valid payment and returns an error for invalid payment information. It also checks that process_payment() succeeds when a payment is accepted and fails when a payment is denied.

The script then tests that request_fulfillment() succeeds for an accepted payment and fails when the payment is not accepted. Finally, it verifies that get_cost_breakdown() returns the expected subtotal, tax, fees, and total for an order.