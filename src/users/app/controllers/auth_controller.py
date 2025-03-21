from flask import Blueprint, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.exceptions.http_exceptions import UnauthorizedError, BadRequestError, ForbiddenError, NotFoundError
from app.utils.response_util import format_response
from app.services.user_service import UserService
from app.models.user_model import UserSchema

auth_bp = Blueprint('auth', __name__)
user_schema = UserSchema(only=("id", "email", "username"))

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        user_data = request.get_json()
        user = UserService.check_credentials(user_data)
    except (UnauthorizedError, BadRequestError, ForbiddenError) as e:
        return format_response("error", e.code, error=e.description), e.code
    else:
        response: dict = {
            "user": user_schema.dump(user),
            "access_token": create_access_token(identity=user.id)
        }
        return format_response("success", 200, message="Usuario logueado con éxito", data=response)
    
@auth_bp.route('/verify', methods=['GET'])    
@jwt_required()
def verify():
    user_id = get_jwt_identity()
    try:
        user = UserService.get_by_id_and_status(user_id)
    except (NotFoundError, BadRequestError, ForbiddenError) as e:
        return format_response("error", e.code, error=e.description)
    else:
        return format_response("success", 200, message = "Usuario verificado con éxito", data = user_schema.dump(user))
