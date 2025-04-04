import os
import uuid
import re
import requests
from app.exceptions.http_exceptions import BadRequestError
from app.repositories.seller_repository import SellerRepository

def validate_uuid(id):
    try:
        uuid.UUID(id, version=4)
        return True
    except ValueError:
        return False
    
def is_valid_email(email):
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email) is not None

class SellerService:
  
  BASE_URL_USER_API = os.getenv('PATH_API_USER')
  PASSWORD_DEFAULT = os.getenv('PASSWORD_DEFAULT')
  
  @staticmethod
  def create(seller_data):
    if not seller_data.get("name"):
      raise BadRequestError("El nombre es requerido")
    if not seller_data.get("lastname"):
      raise BadRequestError("El apellido es requerido")
    if not seller_data.get("email"):
      raise BadRequestError("El email es requerido")
    if is_valid_email(seller_data.get("email")) is False:
      raise BadRequestError("El email no es válido")
    external_api_url = f'{SellerService.BASE_URL_USER_API}'
  
    payload = {
      "name": seller_data.get("name"),
      "lastname": seller_data.get("lastname"),
      "email": seller_data.get("email"),
      "password": SellerService.PASSWORD_DEFAULT,
      "role": "seller"
    }
    response = requests.post(external_api_url, json=payload)
    if response.status_code != 201:
      raise BadRequestError(response.json().get("error"))
    seller = {
      "assigned_area": seller_data.get("assignedArea"),
      "user_id": response.json().get("data").get("id"),
    }
    
    return SellerRepository.create(seller)