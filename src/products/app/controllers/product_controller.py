from flask import Blueprint, request
from app.models.category_model import CategorySchema
from app.models.product_model import ProductSchema
from app.services.product_service import ProductService
from app.exceptions.http_exceptions import BadRequestError
from app.utils.response_util import format_response
from flask_jwt_extended import jwt_required
from app.utils.validate_role import validate_role

product_bp = Blueprint('product', __name__, url_prefix='/products')
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)
categories_schema = CategorySchema(many=True)


@product_bp.route('', methods=['POST'])
@jwt_required()
@validate_role(["admin"])
def create_product():
  try:
    product_data = request.get_json()
    product_created = ProductService.create(product_data)
    return format_response("success", 201, "Producto creado con éxito", product_schema.dump(product_created))
  except BadRequestError as e:
    return format_response("error", e.code, error=e.description)
        
@product_bp.route('', methods=['GET'])
@jwt_required()
@validate_role(["admin", "seller", "customer"])
def get_products():
  try:
    products = ProductService.get_all()
    return format_response("success", 200, "Productos obtenidos con éxito", products_schema.dump(products))
  except BadRequestError as e:
    return format_response("error", e.code, error=e.description)
  
@product_bp.route('/<string:product_id>', methods=['GET'])
@jwt_required()
def get_product_by_id(product_id):
    try:
        product = ProductService.get_product_by_id(product_id)
        return format_response("success", 200, "Producto obtenido con éxito", product_schema.dump(product))
    except BadRequestError as e:
        return format_response("error", e.code, error=e.description)        

@product_bp.route('/ping', methods=['GET'])
def ping():
  return format_response("success", 200, "pong")

@product_bp.route('/<string:product_id>/quantity', methods=['PUT'])
@jwt_required()
def update_product_quantity(product_id):
    try:
        request_data = request.get_json() 
        updated_product = ProductService.update_quantity(product_id, request_data)
        return format_response(
            "success",
            200,
            "Cantidad del producto actualizada con éxito",
            product_schema.dump(updated_product)
        )
    except BadRequestError as e:
        return format_response("error", e.code, error=e.description)
    
@product_bp.route('/category/<string:category_id>', methods=['GET'])
@jwt_required()
@validate_role(["admin", "seller"])
def get_products_by_category(category_id):
    try:
        products = ProductService.get_products_by_category(category_id)
        if not products:
            return format_response("success", 200, "No hay productos disponibles en esta categoría", products_schema.dump(products))
        return format_response("success", 200, "Productos obtenidos con éxito", products_schema.dump(products))
    except BadRequestError as e:
        return format_response("error", e.code, error=e.description)

@product_bp.route('/upload-preview', methods=['POST'])
@jwt_required()
@validate_role(["admin"])
def load_products_massive():
  file = request.files.get('file')
  if not file:
    return format_response("error", 400, "Debe cargar un archivo válido")
  try:
    result = ProductService.parse_and_validate_file(file)
    return format_response("success", 200, "Archivo procesado correctamente", result)
  except BadRequestError as e:
      return BadRequestError(f"Error al procesar el archivo: {str(e)}")
  
@product_bp.route('/bulk-save', methods=['POST'])
@jwt_required()
@validate_role(["admin"])
def save_products_bulk():
  data = request.get_json()

  if not data or 'products' not in data:
    return format_response("error", 400, "Debe enviar una lista de productos válida")
   
  try:
    quantity = ProductService.bulk_save_products(data['products'])
    return format_response("sucess", 201, f"{quantity} productos guardados exitosamente.")
  except BadRequestError as e:
    return BadRequestError(f"Error al guardar los productos: {str(e)}")
  
@product_bp.route('/categories', methods=['GET'])
@jwt_required()
@validate_role(["seller"])
def get_categories():
    try:
        categories = ProductService.get_categories()
        if not categories:
            return format_response("success", 200, "No hay categorías disponibles", categories_schema.dump(categories))
        return format_response("success", 200, "Categorías obtenidas con éxito", categories_schema.dump(categories))
    except BadRequestError as e:
        return format_response("error", e.code, error=e.description)