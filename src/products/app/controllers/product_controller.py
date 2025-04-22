from flask import Blueprint, request
from app.models.product_model import ProductSchema
from app.services.product_service import ProductService
from app.exceptions.http_exceptions import BadRequestError
from app.utils.response_util import format_response
from flask_jwt_extended import jwt_required
from app.utils.validate_role import validate_role

product_bp = Blueprint('product', __name__, url_prefix='/products')
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)


@product_bp.route('/', methods=['POST'])
@jwt_required()
@validate_role("admin")
def create_product():
  try:
    product_data = request.get_json()
    product_created = ProductService.create(product_data)
    return format_response("success", 201, "Producto creado con éxito", product_schema.dump(product_created))
  except BadRequestError as e:
    return format_response("error", e.code, error=e.description)
        
@product_bp.route('/', methods=['GET'])
@jwt_required()
@validate_role("admin")
def get_products():
  try:
    products = ProductService.get_all()
    return format_response("success", 200, "Productos obtenidos con éxito", products_schema.dump(products))
  except BadRequestError as e:
    return format_response("error", e.code, error=e.description)
        

@product_bp.route('/ping', methods=['GET'])
def ping():
  return format_response("success", 200, "pong")