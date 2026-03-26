# backend/services/notification_service.py
# this file contains simple notification helper functions
# for order and payment related events.

from __future__ import annotations


def notify_order_status_change(order_id: str, status: str) -> str:
    """
    return a notification message when an order status changes.
    """
    return f"Order {order_id} status updated to {status}."


def notify_payment_result(order_id: str, success: bool) -> str:
    """
    return a notification message for payment result.
    """
    if success:
        return f"Payment for order {order_id} was successful."
    return f"Payment for order {order_id} failed."


def notify_owner_new_paid_order(order_id: str) -> str:
    """
    return a notification message for restaurant owner
    when a new paid order is received.
    """
    return f"New paid order received: {order_id}."


def get_recent_notifications(notifications: list[str], limit: int = 5) -> list[str]:
    """
    return the most recent notifications from a list.
    """
    return notifications[-limit:]

