from app.models.warehouse_model import Warehouse
from app.core.database import db

class WarehouseRepository:
  
  @staticmethod
  def get_all():
    warehouses = Warehouse.query.all()    
    return warehouses
  
  @staticmethod
  def create(warehouse: Warehouse):
    db.session.add(warehouse)
    db.session.commit()
    
    return warehouse
  
  @staticmethod
  def get_by_id(warehouse_id):
    return Warehouse.query.get(warehouse_id)