This test script verifies the main functionality of the Payment model.

The test_get_payment_info test checks that get_payment_info() returns the correct payment details such as ID, order ID, card name, status, amount, and expiration date.

The test_process_payment_success test verifies that processPayment() successfully processes a payment and updates the status to PaymentStatus.ACCEPTED.

The test_request_fulfillment_success test confirms that after a payment is successfully processed, request_fulfillment() returns True.

The test_request_fulfillment_denied test checks that if a payment has not been successfully processed, request_fulfillment() returns False, preventing fulfillment.