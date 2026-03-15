from dataclasses import dataclass
from backend.models.order.order_model import Order


@dataclass
class CostBreakdown:
    subtotal: float
    tax: float
    deliveryFee: float
    serviceFee: float
    total: float


class CostCalculator:

    def calculateSubtotal(self, order: Order) -> float:
        """
        Calculates subtotal of items in the order.
        """
        subtotal = 0.0
        for item in order.items:
            subtotal += item.price * item.quantity
        return subtotal

    def calculateTax(self, order: Order) -> float:
        """
        Example tax calculation (12%).
        """
        subtotal = self.calculateSubtotal(order)
        return subtotal * 0.12

    def calculateDeliveryFee(self, order: Order) -> float:
        """
        Flat delivery fee example.
        """
        return 5.00

    def calculateServiceFee(self, order: Order) -> float:
        """
        Example service fee (5% of subtotal).
        """
        subtotal = self.calculateSubtotal(order)
        return subtotal * 0.05

    def calculateTotal(self, order: Order) -> float:
        """
        Calculates the final total.
        """
        subtotal = self.calculateSubtotal(order)
        tax = self.calculateTax(order)
        delivery = self.calculateDeliveryFee(order)
        service = self.calculateServiceFee(order)

        return subtotal + tax + delivery + service

    def getBreakdown(self, order: Order) -> CostBreakdown:
        """
        Returns the full cost breakdown.
        """
        subtotal = self.calculateSubtotal(order)
        tax = self.calculateTax(order)
        delivery = self.calculateDeliveryFee(order)
        service = self.calculateServiceFee(order)
        total = subtotal + tax + delivery + service

        return CostBreakdown(
            subtotal=subtotal,
            tax=tax,
            deliveryFee=delivery,
            serviceFee=service,
            total=total
        )
        