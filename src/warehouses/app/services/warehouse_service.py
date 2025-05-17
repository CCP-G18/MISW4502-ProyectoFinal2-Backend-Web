import uuid
from app.repositories.warehouse_repository import WarehouseRepository, Warehouse
from app.models.warehouse_model import Warehouse
from app.exceptions.http_exceptions import BadRequestError

def validate_uuid(id):
  try:
    uuid.UUID(id, version=4)
    return True
  except ValueError:
    return False
    
class WarehouseService:
    
  @staticmethod
  def get_all():
    warehouses = WarehouseRepository.get_all()
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
  def get_warehouse_by_id(warehouse_id):
    if not validate_uuid(warehouse_id):
      raise BadRequestError("El id no es válido")   
    warehouse = WarehouseRepository.get_warehouse_by_id(warehouse_id)
    if not warehouse:
      raise BadRequestError("La bodega no existe")    
    return warehouse