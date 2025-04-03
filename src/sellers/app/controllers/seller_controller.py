from flask import Blueprint, request
from app.services.seller_service import SellerService
from app.utils.response_util import format_response
from app.exceptions.http_exceptions import BadRequestError
from app.models.seller_model import SellerSchema

seller_bp = Blueprint('seller', __name__, url_prefix="/sellers")
seller_schema = SellerSchema()

@seller_bp.route('/', methods=['POST'])
def create_seller():
  try:
    seller_data = request.get_json()
    seller = SellerService.create(seller_data)
    return format_response("success", 201, "Vendedor creado con éxito", seller_schema.dump(seller))
  except BadRequestError as e:
    return format_response("error", e.code, error=e.description)