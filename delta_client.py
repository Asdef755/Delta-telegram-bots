import requests
import os

BASE_URL = os.getenv("DELTA_BASE_URL")
API_KEY = os.getenv("DELTA_KEY")
API_SECRET = os.getenv("DELTA_SECRET")
PRODUCT_ID = os.getenv("DELTA_PRODUCT_ID", "27")


def place_order(side, size, price=None, stop_loss=None):
    """
    Dummy order function (you’ll expand with full Delta API later).
    Right now just prints to logs.
    """
    print(f"[Delta] {side} order placed: size={size}, stop={stop_loss}, price={price}")
    return True


def cancel_all():
    """Cancel all orders (dummy)."""
    print("[Delta] All orders canceled.")
    return True
