import uuid
from datetime import datetime
from zoneinfo import ZoneInfo

from app.repositories.visit_route_repository import VisitRouteRepository
from app.exceptions.http_exceptions import BadRequestError, NotFoundError
from app.models.visit_route_model import VisitRoute

def validate_uuid(id):
    try:
        uuid.UUID(str(id), version=4)
        return True
    except ValueError:
        return False

class VisitRouteService:

    INVALID_ID_FORMAT_MESSAGE = "El formato del id de la ruta no es correcto"
    NOT_FOUND_MESSAGE = "Ruta de visita no encontrada"

    @staticmethod
    def get_all():
        routes = VisitRouteRepository.get_all()
        if not routes:
            raise ValueError("No hay rutas registradas")
        return routes

    @staticmethod
    def get_by_id(route_id):
        if not validate_uuid(route_id):
            raise BadRequestError(VisitRouteService.INVALID_ID_FORMAT_MESSAGE)

        route = VisitRouteRepository.get_by_id(route_id)
        if not route:
            raise NotFoundError(VisitRouteService.NOT_FOUND_MESSAGE)
        return route

    @staticmethod
    def get_by_seller_id(seller_id):
        if not validate_uuid(seller_id):
            raise BadRequestError("El formato del id del vendedor no es correcto")

        routes = VisitRouteRepository.get_by_seller_id(seller_id)
        if not routes:
            raise NotFoundError("No hay rutas registradas para el vendedor")
        return routes

    @staticmethod
    def get_by_seller_and_date(seller_id, visit_date):
        if not validate_uuid(seller_id):
            raise BadRequestError("El formato del id del vendedor no es correcto")

        try:
            if isinstance(visit_date, str):
                visit_date = datetime.strptime(visit_date, "%Y-%m-%d").date()
        except ValueError:
            raise BadRequestError("La fecha no tiene un formato válido (YYYY-MM-DD)")

        routes = VisitRouteRepository.get_by_seller_and_date(seller_id, visit_date)
        if not routes:
            raise NotFoundError("No hay rutas programadas para esa fecha")
        return sorted(routes, key=lambda r: r.estimated_time)

    @staticmethod
    def create(data):
        required_fields = ["route_name", "visit_date", "origin_address", "origin_lat", "origin_lng", "destination_address", "destination_lat", "destination_lng", "estimated_time", "seller_id"]
        for field in required_fields:
            if not data.get(field):
                raise BadRequestError(f"El campo {field} es requerido")

        if not validate_uuid(data["seller_id"]):
            raise BadRequestError("El id del vendedor no es válido")

        try:
            visit_date = datetime.strptime(data["visit_date"], "%Y-%m-%d").date()
        except ValueError:
            raise BadRequestError("La fecha de visita no tiene un formato válido (YYYY-MM-DD)")
        
        today = datetime.now(ZoneInfo("America/Bogota")).date()
        if visit_date < today:
            raise BadRequestError("La fecha de la visita no puede ser anterior al día de hoy")

        seller_id = uuid.UUID(data["seller_id"])

        route = VisitRoute(
            route_name=data["route_name"],
            visit_date=visit_date,
            origin_address=data["origin_address"],
            origin_lat=data["origin_lat"],
            origin_lng=data["origin_lng"],
            destination_address=data["destination_address"],
            destination_lat=data["destination_lat"],
            destination_lng=data["destination_lng"],
            estimated_time=data["estimated_time"],
            seller_id=seller_id
        )

        return VisitRouteRepository.create(route)