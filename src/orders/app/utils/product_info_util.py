import requests
import os
from flask import request

def get_product_info(id):
    token = request.headers.get("Authorization")
    response = requests.get(f"{os.getenv('PATH_API_PRODUCTS')}/products/{id}", headers={"Authorization": token})
    if response.status_code == 200:
        return response.json()
    return None

def update_product_quantity(id, quantity):
    token = request.headers.get("Authorization")
    headers = {"Authorization": token, "Content-Type": "application/json"}
    body = {"quantity": quantity}
    response = requests.put(
        f"{os.getenv('PATH_API_PRODUCTS')}/products/{id}/quantity",
        headers=headers,
        json=body)
    if response.status_code == 200:
        return response.json()
    return None