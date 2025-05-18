from werkzeug.exceptions import HTTPException
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.visit_service import VisitService
from app.models.visit_model import VisitSchema
from app.services.visit_route_service import VisitRouteService
from app.models.visit_route_model import VisitRouteSchema
from app.utils.response_util import format_response
from app.exceptions.http_exceptions import NotFoundError, BadRequestError
from app.utils.validate_role import validate_role

visit_bp = Blueprint('visit', __name__, url_prefix='/visits')
visit_schema = VisitSchema()
visits_schema = VisitSchema(many=True)
visit_route_schema = VisitRouteSchema()
visit_routes_schema = VisitRouteSchema(many=True)

@visit_bp.route('/', methods=['GET'])
@jwt_required()
@validate_role("seller")
def get_visits():
    try:
        visits = VisitService.get_all()
        if not visits:
            return format_response("success", 200, message="No hay rutas de visitas registrados", data=[])
    except HTTPException as e:
        return format_response("error", e.code, error=e.description)
    else:
        return format_response("success", 200, message="Todas las visitas han sido obtenidas", data=visits_schema.dump(visits))


@visit_bp.route('/<string:id>', methods=['GET'])
@jwt_required()
@validate_role("seller")
def get_visit(id:str):
    try:
        visit = VisitService.get_by_id(id)
    except (NotFoundError, BadRequestError) as e:
        return format_response("error", e.code, error=e.description)
    else:
        return format_response("success", 200, "Visita encontrada con éxito", visit_schema.dump(visit))
    
@visit_bp.route('/customer/<string:id>', methods=['GET'])
@jwt_required()
@validate_role("seller")
def get_visits_by_customer(id:str):
    try:
        visit = VisitService.get_by_id_customer(id)
    except (NotFoundError, BadRequestError) as e:
        return format_response("error", e.code, error=e.description, data=[])
    else:
        return format_response("success", 200, "Visitas encontradas con éxito", visits_schema.dump(visit))

@visit_bp.route('/', methods=['POST'])
@jwt_required()
@validate_role("seller")
def create_visit():
    try:
        visit_data = request.get_json()
        visit = VisitService.create(visit_data)
    except BadRequestError as e:
        return format_response("error", e.code, error=e.description)
    else:
        return format_response("success", 201, "Visita creada con éxito", visit_schema.dump(visit))
    
@visit_bp.route('/ping', methods=['GET'])
def ping():
    return format_response("success", 200, "pong")

@visit_bp.route('/routes', methods=['GET'])
@jwt_required()
@validate_role("admin")
def get_visit_routes():
    try:
        routes = VisitRouteService.get_all()
    except HTTPException as e:
        return format_response("error", e.code, error=e.description)
    else:
        return format_response("success", 200, "Todas las rutas de visita han sido obtenidas", visit_routes_schema.dump(routes))


@visit_bp.route('/routes/<string:id>', methods=['GET'])
@jwt_required()
@validate_role("seller")
def get_visit_route_by_id(id: str):
    try:
        route = VisitRouteService.get_by_id(id)
    except (NotFoundError, BadRequestError) as e:
        return format_response("error", e.code, error=e.description)
    else:
        return format_response("success", 200, "Ruta de visita encontrada con éxito", visit_route_schema.dump(route))


@visit_bp.route('/routes/seller/<string:seller_id>', methods=['GET'])
@jwt_required()
@validate_role("seller")
def get_visit_routes_by_seller_id(seller_id: str):
    try:
        routes = VisitRouteService.get_by_seller_id(seller_id)
    except (NotFoundError, BadRequestError) as e:
        return format_response("error", e.code, error=e.description)
    else:
        return format_response("success", 200, "Rutas de visita encontradas con éxito", visit_routes_schema.dump(routes))


@visit_bp.route('/routes/seller/<string:seller_id>/date/<string:visit_date>', methods=['GET'])
@jwt_required()
@validate_role("seller")
def get_visit_routes_by_seller_and_date(seller_id: str, visit_date: str):
    try:
        routes = VisitRouteService.get_by_seller_and_date(seller_id, visit_date)
    except (NotFoundError, BadRequestError) as e:
        return format_response("error", e.code, error=e.description)
    else:
        return format_response("success", 200, "Rutas encontradas con éxito", visit_routes_schema.dump(routes))


@visit_bp.route('/routes', methods=['POST'])
@jwt_required()
@validate_role("admin")
def create_visit_route():
    try:
        route_data = request.get_json()
        route = VisitRouteService.create(route_data)
    except BadRequestError as e:
        return format_response("error", e.code, error=e.description)
    except Exception as e:
        return format_response("error", 500, error="Error interno del servidor: " + str(e))
    else:
        return format_response("success", 201, "Ruta de visita creada con éxito", visit_route_schema.dump(route))