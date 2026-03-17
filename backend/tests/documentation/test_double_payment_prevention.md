This test script verifies that the payment system prevents a payment from being processed more than once.

It first creates a mock order object so the payment can reference an order without requiring the real order model. It then creates a valid Payment object with sample card information, an amount, and an initial status.

The test calls processPayment() twice on the same payment. It checks that the first call succeeds and returns True, meaning the payment was processed successfully. It then checks that the second call returns False, confirming that the system blocks a second attempt to process the same payment.

Finally, it verifies that after the successful first attempt, the payment status has been updated to PaymentStatus.ACCEPTED.