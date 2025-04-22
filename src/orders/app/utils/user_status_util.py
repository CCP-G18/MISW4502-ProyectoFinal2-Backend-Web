import requests
import os
from flask import request

USER_SERVICE_URL = f"{os.getenv('USER_SERVICE_URL')}/users/"

def set_user_status():
    token = request.headers.get("Authorization")
    requests.patch(USER_SERVICE_URL, headers={"Authorization": token}, json={"status": "BLOCKED"})