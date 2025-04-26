import uuid
import re
from app.repositories.producer_repository import ProducerRepository
from app.exceptions.http_exceptions import BadRequestError, NotFoundError, UnauthorizedError, ForbiddenError
from app.models.producer_model import Producer

def validate_uuid(id):
    try:
        uuid.UUID(id, version=4)
        return True
    except ValueError:
        return False
    
def is_valid_email(email):
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email) is not None

class ProducerService:

    NOT_FOUND_MESSAGE = "Fabricante no encontrado"
    INVALID_ID_FORMAT_MESSAGE = "El formato del id del fabricante no es correcto"

    @staticmethod
    def get_all():
        producers = ProducerRepository.get_all()
        if not producers:
            raise ValueError("No hay fabricantes registrados")
        return producers

    @staticmethod
    def get_by_id(producer_id):
        if not validate_uuid(producer_id):
            raise BadRequestError(ProducerService.INVALID_ID_FORMAT_MESSAGE)
            
        producer = ProducerRepository.get_by_id(producer_id)
        if not producer:
            raise NotFoundError(ProducerService.NOT_FOUND_MESSAGE)
        return producer

    def create(data):
        if not data.get("name"):
            raise BadRequestError("El nombre es requerido")
        if not data.get("country"):
            raise BadRequestError("El país es requerido")
        if not data.get("email"):
            raise BadRequestError("El email es requerido")
        if is_valid_email(data.get("email")) is False:
            raise BadRequestError("El email no es válido")
        if ProducerRepository.get_by_email(data["email"]):
            raise BadRequestError("El email se encuentra en uso")
        if not data.get("address"):
            raise BadRequestError("La direccion es requerida")
        if not data.get("phone"):
            raise BadRequestError("El telefono es requerido")
        if not data.get("website"):
            raise BadRequestError("El sitio web es requerido")
        if not data.get("contact_name"):
            raise BadRequestError("El nombre del contacto es requerido")
        if not data.get("contact_lastname"):
            raise BadRequestError("El apellido del contacto es requerido")
        if not data.get("contact_email"):
            raise BadRequestError("El email del contacto es requerido")
        if not data.get("contact_phone"):
            raise BadRequestError("El telefono del contacto es requerido")
        
        producer = Producer(
            name = data["name"], 
            country = data["country"], 
            email = data["email"], 
            address = data["address"], 
            phone = data["phone"], 
            website = data["website"], 
            contact_name = data["contact_name"], 
            contact_lastname = data["contact_lastname"], 
            contact_email = data["contact_email"], 
            contact_phone = data["contact_phone"]
        )

        return ProducerRepository.create(producer)