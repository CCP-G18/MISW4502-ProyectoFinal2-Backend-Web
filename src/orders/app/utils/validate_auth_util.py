import requests
import os
from urllib.parse import urljoin, urlparse
from functools import wraps
from flask import request
from app.exceptions.http_exceptions import UnauthorizedError, NotFoundError, ForbiddenError
from app.utils.response_util import format_response


PATH_API_USER = os.getenv("PATH_API_USER")
AUTH_SERVICE_URL = PATH_API_USER.replace("/users", "/verify")

def check_auth(token):
    response = requests.get(AUTH_SERVICE_URL, headers={"Authorization": token})
    if response.status_code == 401:
        raise UnauthorizedError(response.json()["error"])
    if response.status_code == 403:
        raise ForbiddenError(response.json()["error"])
    if response.status_code == 404:
        raise NotFoundError(response.json()["error"])
    return response.json().get("data")

def get_authenticated_user_id():
    try:
        token = request.headers.get("Authorization")
        if not token:
            raise UnauthorizedError("Token no enviado")
        user = check_auth(token)
        return user.get("id")
    except (UnauthorizedError, NotFoundError, ForbiddenError) as e:
        raise e