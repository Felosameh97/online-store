import hashlib
import hmac
import json
import requests
from django.conf import settings

PAYMOB_BASE_URL = "https://accept.paymobsolutions.com/api"


def get_paymob_auth_token():
    payload = {
        "api_key": settings.PAYMOB_API_KEY,
    }
    response = requests.post(f"{PAYMOB_BASE_URL}/auth/tokens", json=payload, timeout=15)
    response.raise_for_status()
    return response.json().get("token")


def create_payment_request(order, billing_data, integration_id=None):
    if integration_id is None:
        integration_id = settings.PAYMOB_INTEGRATION_ID

    auth_token = get_paymob_auth_token()
    payload = {
        "auth_token": auth_token,
        "amount_cents": int(order.total_amount * 100),
        "currency": "EGP",
        "delivery_needed": False,
        "merchant_order_id": order.id,
        "billing_data": billing_data,
        "items": [
            {
                "name": item.product.title,
                "amount_cents": int(item.total_price * 100),
                "description": item.product.description[:100],
                "quantity": item.quantity,
            }
            for item in order.items.all()
        ],
        "integration_id": integration_id,
    }
    response = requests.post(f"{PAYMOB_BASE_URL}/ecommerce/orders", json=payload, timeout=15)
    response.raise_for_status()
    return response.json()


def verify_webhook_signature(body, signature):
    secret = settings.PAYMOB_HMAC_SECRET.encode()
    expected = hmac.new(secret, body.encode("utf-8"), hashlib.sha512).hexdigest()
    return hmac.compare_digest(expected, signature)


def create_payment_key(order, billing_data, integration_id=None):
    auth_token = get_paymob_auth_token()
    payload = {
        "auth_token": auth_token,
        "amount_cents": int(order.total_amount * 100),
        "expiration": 3600,
        "order_id": order.id,
        "billing_data": billing_data,
        "integration_id": integration_id or settings.PAYMOB_INTEGRATION_ID,
        "currency": "EGP",
    }
    response = requests.post(f"{PAYMOB_BASE_URL}/acceptance/payment_keys", json=payload, timeout=15)
    response.raise_for_status()
    return response.json()
