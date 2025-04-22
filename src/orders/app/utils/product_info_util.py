import requests
import os
from flask import request

def get_product_info(id):
    token = request.headers.get("Authorization")
    response = requests.get(f"{os.getenv('PRODUCT_SERVICE_URL')}/products/{id}", headers={"Authorization": token})
    if response.status_code == 200:
        return response.json()
    return None