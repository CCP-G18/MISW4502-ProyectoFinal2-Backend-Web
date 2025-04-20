import uuid
from app.repositories.product_repository import ProductRepository, Product
from app.exceptions.http_exceptions import BadRequestError

def validate_uuid(id):
    try:
        uuid.UUID(id, version=4)
        return True
    except ValueError:
        return False
    
class ProductService:
        
    @staticmethod
    def create(product_data):
        if not product_data.get("name"):
            raise BadRequestError("El nombre es requerido")
        if not product_data.get("description"):
            raise BadRequestError("La descripción es requerida")
        if not product_data.get("unit_amount"):
            raise BadRequestError("El monto es requerido")
        if not product_data.get("quantity"):
            raise BadRequestError("La cantidad es requerida")
        if not product_data.get("manufacturer_id"):
            raise BadRequestError("El fabricante es requerido")
        if not product_data.get("category_id"):
            raise BadRequestError("La categoría es requerida")
        if not validate_uuid(product_data.get("manufacturer_id")):
            raise BadRequestError("El fabricante no es válido")
        if not validate_uuid(product_data.get("category_id")):
            raise BadRequestError("La categoría no es válida")
        
        product = Product(
            name=product_data.get("name"),
            unit_amount=product_data.get("unit_amount"),
            quantity=product_data.get("quantity"),
            manufacturer_id=product_data.get("manufacturer_id"),
            category_id=product_data.get("category_id"),
        )
        
        return ProductRepository.create(product)