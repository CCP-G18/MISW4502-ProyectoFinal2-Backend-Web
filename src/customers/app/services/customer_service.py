import uuid
import re
import requests
import os
from app.repositories.customer_repository import CustomerRepository
from app.exceptions.http_exceptions import BadRequestError
from app.models.customer_model import Customer, DocumentTypeEnum
from flask import request

def validate_uuid(id):
    try:
        uuid.UUID(id, version=4)
        return True
    except ValueError:
        return False    

def is_valid_data(data):
    pattern = r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$"
    return re.match(pattern, data) is not None

class CustomerService:

    BASE_URL_USER_API = os.getenv("PATH_API_USER")

    @staticmethod
    def get_all():

        customers = CustomerRepository.get_all()
        if not customers:
            raise ValueError("No hay clientes registrados")
        
        customers_dict = []
        token = request.headers.get("Authorization").split(" ")[1]

        for customer in customers:
            headers = {
                'Authorization': f'Bearer {token}',
            }
            response = requests.get(f'{CustomerService.BASE_URL_USER_API}/{customer.user_id}', headers=headers)

            if response.status_code != 200:
                raise BadRequestError(f"No se pudo obtener los datos del usuario con ID {customer.user_id}")
            user_data = response.json().get("data")

            if isinstance(customer.identification_type, DocumentTypeEnum):
                identification_type = customer.identification_type.value
            elif isinstance(customer.identification_type, str):
                identification_type = customer.identification_type
            else:
                raise BadRequestError(f"Tipo de identificación inválido para el cliente con ID {customer.id}")
            customer_dict = {
                "id": str(customer.id),
                "identification_type": identification_type,
                "identification_number": customer.identification_number,
                "country": customer.country,
                "city": customer.city,
                "address": customer.address,
                "name": f"{user_data.get('name')} {user_data.get('lastname')}",
                "email": user_data.get('email')
            }
            customers_dict.append(customer_dict)

        return customers_dict

    @staticmethod
    def create(customer_data):

        if not customer_data.get("identificationType"):
            raise BadRequestError("El tipo de identificación es requerido")               
        if customer_data.get("identificationType") not in ["CC", "NIT", "CE", "DNI", "PASSPORT"]:
            raise BadRequestError("El tipo de identificación no es válido, debe ser CC, NIT, CE, DNI o PASSPORT")
        
        if not customer_data.get("identificationNumber"):
            raise BadRequestError("El número de identificación es requerido")
        if not str(customer_data.get("identificationNumber")).isdigit():
            raise BadRequestError("El número de identificación no es válido, debe ser un valor numerico")        
        
        if not customer_data.get("country"):
            raise BadRequestError("El país es requerido")
        if not is_valid_data(customer_data.get("country")):
            raise BadRequestError("El país debe contener solo letras y espacios")  
        
        if not customer_data.get("city"):
            raise BadRequestError("La ciudad es requerida")
        if not is_valid_data(customer_data.get("city")):
            raise BadRequestError("La ciudad debe contener solo letras y espacios")  
        
        if not customer_data.get("address"):
            raise BadRequestError("La dirección es requerida")
        
        if not customer_data.get("user"):
            raise BadRequestError("Los datos del cliente son requeridos") 
        
        user_data = customer_data["user"]
        if "role" not in user_data:
            user_data["role"] = "customer"        

        user_service_url = CustomerService.BASE_URL_USER_API
        user_response = requests.post(user_service_url, json=user_data)

        if user_response.status_code != 201:
            raise BadRequestError(f"Error al crear el usuario: {user_response.json().get('error')}")
      
        customer = Customer(
            user_id = user_response.json().get("data").get("id"),
            identification_type = customer_data["identificationType"],
            identification_number = customer_data["identificationNumber"],
            country = customer_data["country"],
            city = customer_data["city"],
            address = customer_data["address"])
        return CustomerRepository.create(customer)