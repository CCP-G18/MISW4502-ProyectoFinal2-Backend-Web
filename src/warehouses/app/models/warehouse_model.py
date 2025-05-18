import uuid
from app.core.database import db, ma
from sqlalchemy.dialects.postgresql import UUID


class Warehouse(db.Model):
  __tablename__ = 'warehouses'
    
  id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  name = db.Column(db.String(120), nullable=False)
  location = db.Column(db.Text, nullable=False)
  
  created_at = db.Column(db.DateTime, server_default=db.func.now())
  updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

  warehouse_products = db.relationship(
    'WarehouseProducts',
    back_populates='warehouse',
    cascade='all, delete-orphan'
  )
    
  def __init__(self, name, location):
    self.name = name
    self.location = location
        
    super().__init__()
        
class WarehouseSchema(ma.Schema):
  class Meta:
    model = Warehouse
    load_instance = True
    fields = (
      'id',
      'name',
      'location',
      'created_at',
      'updated_at'
    )