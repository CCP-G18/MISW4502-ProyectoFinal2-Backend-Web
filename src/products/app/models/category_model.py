import uuid
from app.core.database import db, ma
from sqlalchemy.dialects.postgresql import UUID

class Category(db.Model):
  __tablename__ = 'categories'
    
  id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  name = db.Column(db.String(120), nullable=False)

  created_at = db.Column(db.DateTime, server_default=db.func.now())
  updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    
  def __init__(self, name):
    self.name = name
        
    super().__init__()
        
class CategorySchema(ma.Schema):
  class Meta:
    model = Category
    fields = (
      'id',
      'name',
      'created_at',
      'updated_at'
    )