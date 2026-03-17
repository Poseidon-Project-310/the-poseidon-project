This test script verifies the cost calculation logic in the CostCalculator model.

It first creates a mock order containing two items with prices and quantities. The test_calculate_subtotal test checks that calculateSubtotal() correctly multiplies each item's price by its quantity and sums them to produce the correct subtotal of 35.0.

The test_calculate_tax test verifies that calculateTax() correctly computes tax as 12% of the subtotal, ensuring the tax calculation is based on the correct subtotal value.