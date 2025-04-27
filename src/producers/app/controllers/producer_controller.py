from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.producer_service import ProducerService
from app.models.producer_model import ProducerSchema
from app.utils.response_util import format_response
from app.exceptions.http_exceptions import NotFoundError, BadRequestError
from app.utils.validate_role import validate_role

producer_bp = Blueprint('producer', __name__, url_prefix='/producers')
producer_schema = ProducerSchema()
producers_schema = ProducerSchema(many=True)

@producer_bp.route('/', methods=['GET'])
@jwt_required()
@validate_role("admin")
def get_producers():
    try:
        producers = ProducerService.get_all()
    except ValueError as e:
        return format_response("success", 200, message=str(e), data=[])
    else:
        return format_response("success", 200, message="Todos los fabricantes han sido obtenidos", data=producers_schema.dump(producers))


@producer_bp.route('/<string:id>', methods=['GET'])
@jwt_required()
@validate_role("admin")
def get_producer(id:str):
    try:
        producer = ProducerService.get_by_id(id)
    except (NotFoundError, BadRequestError) as e:
        return format_response("error", e.code, error=e.description)
    else:
        return format_response("success", 200, "Fabricante encontrado con éxito", producer_schema.dump(producer))

@producer_bp.route('/', methods=['POST'])
@jwt_required()
@validate_role("admin")
def create_producer():
    try:
        producer_data = request.get_json()
        producer = ProducerService.create(producer_data)
    except BadRequestError as e:
        return format_response("error", e.code, error=e.description)
    else:
        return format_response("success", 201, "Fabricante creado con éxito", producer_schema.dump(producer))
    
@producer_bp.route('/ping', methods=['GET'])
def ping():
    return format_response("success", 200, "pong")

