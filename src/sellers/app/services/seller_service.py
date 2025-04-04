import os
import uuid
import re
import requests
from app.exceptions.http_exceptions import BadRequestError
from app.repositories.seller_repository import SellerRepository
from flask import request
from app.models.seller_model import SellerSchema

seller_schema = SellerSchema()

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
  def get_all():
    sellers = SellerRepository.get_all()
    sellers_dict = []
    token = request.headers.get("Authorization").split(" ")[1]
    for seller in sellers:
      headers = {
        'Authorization': f'Bearer {token}',
      }
      response = requests.get(f'{SellerService.BASE_URL_USER_API}/{seller.user_id}', headers=headers)
      if response.status_code != 200:
        raise BadRequestError("No se pudo obtener el vendedor")
      seller_dict = seller_schema.dump(seller)
      seller_data = response.json().get("data")
      seller_dict['name'] = f"{seller_data.get('name')} {seller_data.get('lastname')}"
      seller_dict['email'] = seller_data.get('email')
      sellers_dict.append(seller_dict)
    if not sellers_dict:
      raise BadRequestError("No hay vendedores registrados")
    return sellers_dict
  
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