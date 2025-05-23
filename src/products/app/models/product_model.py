import uuid
from app.core.database import db, ma
from sqlalchemy.dialects.postgresql import UUID


class Product(db.Model):
  __tablename__ = 'products'
    
  id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  name = db.Column(db.String(120), nullable=False)
  description = db.Column(db.String(255), nullable=False)
  unit_amount = db.Column(db.Float, nullable=False)
  quantity = db.Column(db.Integer, nullable=False)
  image_url = db.Column(db.String(255), nullable=True)
  
  manufacturer_id = db.Column(UUID(as_uuid=True), nullable=False)
  category_id = db.Column(UUID(as_uuid=True), nullable=False)
  
  created_at = db.Column(db.DateTime, server_default=db.func.now())
  updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    
  def __init__(self,
                name,
                description,
                unit_amount,
                quantity,
                image_url,
                manufacturer_id,
                category_id):
    self.name = name
    self.description = description
    self.unit_amount = unit_amount
    self.quantity = quantity
    self.image_url = image_url 
    self.manufacturer_id = manufacturer_id
    self.category_id = category_id
        
    super().__init__()
        
class ProductSchema(ma.Schema):
  class Meta:
    model = Product
    fields = (
      'id',
      'name',
      'description',
      'unit_amount',
      'quantity',
      'image_url',
      'manufacturer_id',
      'category_id',
      'created_at',
      'updated_at'
    )