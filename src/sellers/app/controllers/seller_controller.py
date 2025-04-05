from flask import Blueprint, request
from app.services.seller_service import SellerService
from app.utils.response_util import format_response
from app.utils.validate_role import validate_role
from app.exceptions.http_exceptions import BadRequestError
from app.models.seller_model import SellerSchema
from flask_jwt_extended import jwt_required

seller_bp = Blueprint('seller', __name__, url_prefix="/sellers")
seller_schema = SellerSchema()

@seller_bp.route('/', methods=['POST'])
@jwt_required()
@validate_role("admin")
def create_seller():
  try:
    seller_data = request.get_json()
    seller = SellerService.create(seller_data)
    return format_response("success", 201, "Vendedor creado con éxito", seller_schema.dump(seller))
  except BadRequestError as e:
    return format_response("error", e.code, error=e.description)
  
@seller_bp.route('/ping', methods=['GET'])
def ping():
    return format_response("success", 200, "pong")