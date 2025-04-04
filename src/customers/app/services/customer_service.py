import uuid
import re
import requests
import os
from app.repositories.customer_repository import CustomerRepository
from app.exceptions.http_exceptions import BadRequestError
from app.models.customer_model import Customer

BASE_URL_USER_API = os.getenv("PATH_API_USER")

def validate_uuid(id):
    try:
        uuid.UUID(id, version=4)
        return True
    except ValueError:
        return False
    
def is_valid_email(email):
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email) is not None

class CustomerService:
    @staticmethod
    def get_all():
        customers = CustomerRepository.get_all()
        if not customers:
            raise ValueError("No hay clientes registrados")
        return customers  

    @staticmethod
    def create(customer_data):
        if not customer_data.get("identificationType"):
            raise BadRequestError("El tipo de identificación es requerido")
        if not customer_data.get("identificationNumber"):
            raise BadRequestError("El número de identificación es requerido")
        if not customer_data.get("country"):
            raise BadRequestError("El país es requerido")     
        if not customer_data.get("city"):
            raise BadRequestError("La ciudad es requerida")
        if not customer_data.get("address"):
            raise BadRequestError("La dirección es requerida")
        if not customer_data.get("user"):
            raise BadRequestError("Los datos del usuario son requeridos")

        # Validar los datos del usuario
        user_data = customer_data["user"]
        if not user_data.get("name"):
            raise BadRequestError("El nombre es requerido")
        if not user_data.get("lastname"):
            raise BadRequestError("El apellido es requerido")
        if not user_data.get("password"):
            raise BadRequestError("La contraseña es requerida")
        if not user_data.get("email"):
            raise BadRequestError("El email es requerido")
        if not is_valid_email(user_data.get("email")):
            raise BadRequestError("El email no es válido")    

        # Crear el usuario en el servicio de usuarios
        user_service_url = os.getenv("USER_SERVICE_URL") + "/users"
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