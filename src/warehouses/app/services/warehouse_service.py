import uuid
from app.repositories.warehouse_repository import WarehouseRepository, Warehouse
from app.models.warehouse_model import Warehouse
from app.models.warehouse_products_model import WarehouseProducts
from app.exceptions.http_exceptions import BadRequestError, NotFoundError

def validate_uuid(id):
  try:
    uuid.UUID(id, version=4)
    return True
  except ValueError:
    return False
    
class WarehouseService:

  INVALID_ID_FORMAT_MESSAGE = "El formato del id de la bodega no es correcto"
  NOT_FOUND_MESSAGE = "Bodega no encontrada"
    
  @staticmethod
  def get_all():
    warehouses = WarehouseRepository.get_all()
    if not warehouses:
      raise ValueError("No hay bodegas registradas")
    return warehouses
    
  @staticmethod
  def create(warehouse_data):
    if not warehouse_data.get("name"):
      raise BadRequestError("El nombre es requerido")
    if not warehouse_data.get("location"):
      raise BadRequestError("la ubicación es requerida")
      
    warehouse = Warehouse(name=warehouse_data.get("name"), location=warehouse_data.get("location"))
      
    return WarehouseRepository.create(warehouse)
  
  @staticmethod
  def get_by_id(warehouse_id):
    if not validate_uuid(warehouse_id):
      raise BadRequestError("El formato del id de la bodega no es correcto")   
    warehouse = WarehouseRepository.get_by_id(warehouse_id)
    if not warehouse:
      raise NotFoundError("Bodega no encontrada")    
    return warehouse
  

  @staticmethod
  def get_warehouses_by_product_id(product_id):
    if not validate_uuid(product_id):
      raise BadRequestError("El formato del id del producto no es correcto") 
    warehouses = WarehouseRepository.get_warehouses_by_product_id(product_id)
    if not warehouses:
      raise NotFoundError("Bodegas no encontradas")
    return warehouses
  
  @staticmethod
  def create_warehouse_by_product(warehouse_data):
    if not warehouse_data.get("quantity"):
      raise BadRequestError("La cantidad es requerida")
    if not warehouse_data.get("product_id"):
      raise BadRequestError("El id del producto es requerido")
    if not warehouse_data.get("warehouse_id"):
      raise BadRequestError("El id de la bodega es requerido")
    if not warehouse_data.get("place"):
      raise BadRequestError("El lugar es requerido")
      
    if not validate_uuid(warehouse_data.get("product_id")):
      raise BadRequestError("El formato del id del producto no es correcto")
    if not validate_uuid(warehouse_data.get("warehouse_id")):
      raise BadRequestError("El formato del id de la bodega no es correcto")
    
    warehouse_product = WarehouseProducts(
      warehouse_id=warehouse_data.get("warehouse_id"),
      product_id=warehouse_data.get("product_id"),
      quantity=warehouse_data.get("quantity"),
      place=warehouse_data.get("place")
    )

    return WarehouseRepository.create_warehouse_by_product(warehouse_product)