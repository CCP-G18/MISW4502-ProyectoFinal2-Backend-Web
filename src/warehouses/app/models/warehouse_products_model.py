import uuid
from app.core.database import db, ma
from sqlalchemy.dialects.postgresql import UUID


class WarehouseProducts(db.Model):
  __tablename__ = 'warehouses_products'
    
  id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  warehouse_id = db.Column(UUID(as_uuid=True), db.ForeignKey('warehouses.id', ondelete='CASCADE'), nullable=False)
  product_id = db.Column(UUID(as_uuid=True), nullable=False)
    
  quantity = db.Column(db.Integer, nullable=False)
  place = db.Column(db.Text, nullable=False)
  created_at = db.Column(db.DateTime, server_default=db.func.now())
  updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

  warehouse = db.relationship('Warehouse', back_populates='warehouse_products')

  def __init__(self, warehouse_id, product_id, quantity, place):
    self.quantity = quantity
    self.place = place
    self.warehouse_id = warehouse_id
    self.product_id = product_id
        
    super().__init__()
        
class WarehouseProductsSchema(ma.Schema):
  class Meta:
    model = WarehouseProducts
    load_instance = True
    fields = (
      'id',
      'warehouse_id',
      'product_id',
      'quantity',
      'place',
      'created_at',
      'updated_at'
    )

  warehouse = ma.Nested('WarehouseSchema')