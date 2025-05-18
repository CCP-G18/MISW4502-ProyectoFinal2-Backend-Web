from app.models.warehouse_model import Warehouse
from app.models.warehouse_products_model import WarehouseProducts
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
  
  @staticmethod
  def get_warehouses_by_product_id(product_id):
    return WarehouseProducts.query.filter(WarehouseProducts.product_id == product_id).all()
  
  @staticmethod
  def create_warehouse_by_product(warehouse_product: WarehouseProducts):
    db.session.add(warehouse_product)
    db.session.commit()
    
    return warehouse_product