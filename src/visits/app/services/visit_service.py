import uuid
import re
from datetime import date, datetime, time
from zoneinfo import ZoneInfo
from app.repositories.visit_repository import VisitRepository
from app.exceptions.http_exceptions import BadRequestError, NotFoundError, UnauthorizedError, ForbiddenError
from app.models.visit_model import Visit

def validate_uuid(id):
    try:
        uuid.UUID(id, version=4)
        return True
    except ValueError:
        return False

class VisitService:

    NOT_FOUND_MESSAGE = "Visita no encontrada"
    INVALID_ID_FORMAT_MESSAGE = "El formato del id de la visita no es correcto"
    INVALID_ID_CUSTOMER_FORMAT_MESSAGE = "El formato del id del cliente no es correcto"

    @staticmethod
    def get_all():
        visits = VisitRepository.get_all()
        if not visits:
            raise ValueError("No hay visitas registradas")
        return visits

    @staticmethod
    def get_by_id(visit_id):
        if not validate_uuid(visit_id):
            raise BadRequestError(VisitService.INVALID_ID_FORMAT_MESSAGE)
            
        visit = VisitRepository.get_by_id(visit_id)
        if not visit:
            raise NotFoundError(VisitService.NOT_FOUND_MESSAGE)
        return visit
    
    @staticmethod
    def get_by_id_customer(customer_id):
        if not validate_uuid(customer_id):
            raise BadRequestError(VisitService.INVALID_ID_CUSTOMER_FORMAT_MESSAGE)
            
        visits = VisitRepository.get_by_id_customer(customer_id)
        if not visits:
            raise NotFoundError("No hay visitas registradas")
        return visits

    def create(data):
        if not data.get("observations"):
            raise BadRequestError("Las observaciones son requeridas")
        if not data.get("customer_id"):
            raise BadRequestError("El id del cliente es requerido")
        if not data.get("seller_id"):
            raise BadRequestError("El id del vendedor es requerido")
        if not validate_uuid(data.get("customer_id")):
            raise BadRequestError("El id del cliente no es válido")
        if not validate_uuid(data.get("seller_id")):
            raise BadRequestError("El id del vendedor no es válido")
        if not data.get("register_date"):
            raise BadRequestError("La fecha de registro es requerida")
        
        raw = data["register_date"]
        if isinstance(raw, str):
            try:
                register_date = datetime.strptime(raw, "%Y-%m-%d").date()
            except ValueError:
                raise BadRequestError("La fecha de registro no tiene un formato válido (YYYY-MM-DD)")
        elif isinstance(raw, date):
            register_date = raw
        else:
            raise BadRequestError("La fecha de registro debe ser un date o un string ISO (YYYY-MM-DD)")
        
        register_datetime = datetime.combine(register_date, time.min).replace(tzinfo=ZoneInfo("America/Bogota"))

        today_bogota = datetime.now(ZoneInfo("America/Bogota")).date()

        if register_datetime.date() != today_bogota:
            raise BadRequestError("La fecha de registro debe ser hoy")
        
        customer_id = uuid.UUID(data["customer_id"])
        seller_id = uuid.UUID(data["seller_id"])
        
        visit = Visit(
            observations = data["observations"], 
            register_date = register_date, 
            customer_id = customer_id,
            seller_id = seller_id
        )

        return VisitRepository.create(visit)