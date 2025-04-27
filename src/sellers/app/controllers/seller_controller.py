from flask import Blueprint, request
from app.services.seller_service import SellerService
from app.utils.response_util import format_response
from app.utils.validate_role import validate_role
from app.exceptions.http_exceptions import BadRequestError
from app.models.seller_model import SellerSchema
from app.models.sales_plan_model import SalesPlanSchema
from flask_jwt_extended import jwt_required

seller_bp = Blueprint('seller', __name__, url_prefix="/sellers")

seller_schema = SellerSchema()
sales_plan_schema = SalesPlanSchema()
sales_plans_schema = SalesPlanSchema(many=True)


@seller_bp.route('', methods=['GET'])
@jwt_required()
@validate_role("admin")
def get_sellers():
  try:
    sellers = SellerService.get_all()
    return format_response("success", 200, "Vendedores obtenidos con éxito", sellers)
  except BadRequestError as e:
    return format_response("error", e.code, error=e.description)

@seller_bp.route('', methods=['POST'])
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

@seller_bp.route('/<string:seller_id>/sales-plans', methods=['GET'])
@jwt_required()
@validate_role("admin")
def get_sales_plan_by_seller(seller_id):
  try:
    sales_plans = SellerService.get_sales_plan_by_seller(seller_id)
    return format_response("success", 200, "Planes de Ventas obtenidos con éxito", sales_plans_schema.dump(sales_plans))
  except BadRequestError as e:
    return format_response("error", e.code, error=e.description)

@seller_bp.route('/<string:seller_id>/sales-plans', methods=['POST'])
@jwt_required()
@validate_role("admin")
def create_sales_plans_by_seller(seller_id):
  try:
    sales_plan_data = request.get_json()
    sales_plan = SellerService.create_sales_plan_by_seller(seller_id, sales_plan_data)
    return format_response("success", 201, "Plan de Ventas creado con éxito", sales_plan_schema.dump(sales_plan) )
  except BadRequestError as e:
    return format_response("error", e.code, error=e.description)