from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.customer_service import CustomerService
from app.models.customer_model import CustomerSchema
from app.utils.response_util import format_response
from app.exceptions.http_exceptions import NotFoundError, BadRequestError

customer_bp = Blueprint('customer', __name__, url_prefix='/customers')
customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)

@customer_bp.route('/', methods=['POST'])
# @jwt_required()
def create_customer():
    try:
        customer_data = request.get_json()        
        customer = CustomerService.create(customer_data)
    except BadRequestError as e:
        return format_response("error", e.code, error=e.description)
    else:
        return format_response("success", 201, "Cliente creado con éxito", customer_schema.dump(customer))


# @user_bp.route('/', methods=['GET'])
# @jwt_required()
# def get_users():
#     try:
#         users = UserService.get_all()
#     except ValueError as e:
#         return format_response("success", 200, message=str(e), data=[])
#     else:
#         return format_response("success", 200, message="Todos los usuarios han sido obtenidos", data=users_schema.dump(users))

# @user_bp.route('/<string:id>', methods=['GET'])
# @jwt_required()
# def get_user(id:str):
#     try:
#         user = UserService.get_by_id(id)
#     except (NotFoundError, BadRequestError) as e:
#         return format_response("error", e.code, error=e.description)
#     else:
#         return format_response("success", 200, "Usuario encontrado con éxito", user_schema.dump(user))

# @user_bp.route('/', methods=['PATCH'])
# @jwt_required()
# def update_user_status():
#     try:
#         user_data = request.get_json()
#         user = UserService.update_status(get_jwt_identity(), user_data)
#     except (NotFoundError, BadRequestError) as e:
#         return format_response("error", e.code, error=e.description)
#     else:
#         return format_response("success", 200, "Usuario actualizado con éxito", user_schema.dump(user))

# @user_bp.route('/ping', methods=['GET'])
# def ping():
#     return format_response("success", 200, "pong")
