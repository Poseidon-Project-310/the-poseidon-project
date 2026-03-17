This test script verifies the validation logic of the Payment model.

The test_validate_success test checks that validate() returns True when all payment details (card name, card number, security number, expiration, and amount) are valid.

The test_validate_empty_card_name test ensures that validation fails if the card name is empty.

The test_validate_invalid_card_number test verifies that validation fails when the card number is invalid.

The test_validate_invalid_security_number test checks that validation fails when the security number is invalid.

The test_validate_empty_expiration test ensures that validation fails if the expiration date is empty.

The test_validate_negative_amount test verifies that validation fails when the payment amount is negative.