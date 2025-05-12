from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.visit_service import VisitService
from app.models.visit_model import VisitSchema
from app.utils.response_util import format_response
from app.exceptions.http_exceptions import NotFoundError, BadRequestError
from app.utils.validate_role import validate_role

visit_bp = Blueprint('visit', __name__, url_prefix='/visits')
visit_schema = VisitSchema()
visits_schema = VisitSchema(many=True)

@visit_bp.route('/', methods=['GET'])
@jwt_required()
@validate_role("seller")
def get_visits():
    try:
        visits = VisitService.get_all()
    except ValueError as e:
        return format_response("success", 200, message=str(e), data=[])
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
        return format_response("error", e.code, error=e.description)
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

