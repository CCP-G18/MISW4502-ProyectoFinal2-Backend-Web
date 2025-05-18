from flask import Blueprint, request
from app.models.warehouse_model import WarehouseSchema
from app.models.warehouse_products_model import WarehouseProductsSchema
from app.services.warehouse_service import WarehouseService
from app.exceptions.http_exceptions import BadRequestError
from app.utils.response_util import format_response
from flask_jwt_extended import jwt_required
from app.utils.validate_role import validate_role

warehouse_bp = Blueprint('warehouse', __name__, url_prefix='/warehouses')
warehouse_schema = WarehouseSchema()
warehouses_schema = WarehouseSchema(many=True)
warehouses_products_schema = WarehouseProductsSchema(many=True)

@warehouse_bp.route('/', methods=['POST'])
@jwt_required()
@validate_role(["admin"])
def create_warehouse():
  try:
    warehouse_data = request.get_json()
    warehouse_created = WarehouseService.create(warehouse_data)
    return format_response("success", 201, "Bodega creada con éxito", warehouse_schema.dump(warehouse_created))
  except BadRequestError as e:
    return format_response("error", e.code, error=e.description)
        
@warehouse_bp.route('/', methods=['GET'])
@jwt_required()
@validate_role(["admin"])
def get_warehouses():
  try:
    warehouses = WarehouseService.get_all()
    return format_response("success", 200, "Bodegas obtenidos con éxito", warehouses_schema.dump(warehouses))
  except BadRequestError as e:
    return format_response("error", e.code, error=e.description)
  
@warehouse_bp.route('/<string:warehouse_id>', methods=['GET'])
@jwt_required()
def get_warehouse_by_id(warehouse_id):
    try:
        warehouse = WarehouseService.get_by_id(warehouse_id)
        return format_response("success", 200, "Bodega obtenido con éxito", warehouse_schema.dump(warehouse))
    except BadRequestError as e:
        return format_response("error", e.code, error=e.description)

@warehouse_bp.route('/product/<string:product_id>', methods=['GET'])
@jwt_required()
def get_warehouses_by_product_id(product_id):
    try:
        warehouses = WarehouseService.get_warehouses_by_product_id(product_id)
        return format_response("success", 200, "Bodegas obtenidas con éxito", warehouses_products_schema.dump(warehouses))
    except BadRequestError as e:
        return format_response("error", e.code, error=e.description)

@warehouse_bp.route('/ping', methods=['GET'])
def ping():
  return format_response("success", 200, "pong")