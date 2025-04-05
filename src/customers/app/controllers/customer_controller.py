from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.customer_service import CustomerService
from app.models.customer_model import CustomerSchema
from app.utils.response_util import format_response
from app.exceptions.http_exceptions import BadRequestError

customer_bp = Blueprint('customer', __name__, url_prefix='/customers')
customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)

@customer_bp.route('/', methods=['POST'])
def create_customer():
    try:
        customer_data = request.get_json()        
        CustomerService.create(customer_data)
    except BadRequestError as e:
        return format_response("error", e.code, error=e.description)
    else:
        if "user" in customer_data:
            customer_data["user"].pop("password", None)
        return format_response("success", 201, "Cliente creado con éxito", customer_data)


@customer_bp.route('/', methods=['GET'])
@jwt_required()
def get_customers():
    try:
        customers = CustomerService.get_all()
    except ValueError as e:
        return format_response("success", 200, message=str(e), data=[])
    else:
        return format_response("success", 200, message="Todos los clientes han sido obtenidos", data=customers_schema.dump(customers))


@customer_bp.route('/ping', methods=['GET'])
def ping():
    return format_response("success", 200, "pong")