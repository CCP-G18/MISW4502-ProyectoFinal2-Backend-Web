import uuid
import re
from app.repositories.customer_repository import CustomerRepository
from app.exceptions.http_exceptions import BadRequestError, NotFoundError, UnauthorizedError, ForbiddenError
from app.models.customer_model import Customer


def validate_uuid(id):
    try:
        uuid.UUID(id, version=4)
        return True
    except ValueError:
        return False
    
# def is_valid_email(email):
#     pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
#     return re.match(pattern, email) is not None

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
        # if is_valid_email(customer_data.get("email")) is False:
        #     raise BadRequestError("El email no es válido")
        
        customer = Customer(
            identification_type = customer_data["identificationType"],
            identification_number = customer_data["identificationNumber"],
            country = customer_data["country"],
            city = customer_data["city"],
            address = customer_data["address"])
        return CustomerRepository.create(customer)
    