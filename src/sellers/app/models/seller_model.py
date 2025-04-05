import uuid
from app.core.database import db, ma
from sqlalchemy.dialects.postgresql import UUID

class Seller(db.Model):
  __tablename__ = 'sellers'

  id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  assigned_area = db.Column(db.String(120), nullable=False)
  created_at = db.Column(db.DateTime, server_default=db.func.now())
  updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
  
  user_id = db.Column(UUID(as_uuid=True), unique=True, nullable=False)

  def __init__(self, assigned_area, user_id):
    self.assigned_area = assigned_area
    self.user_id = user_id

    super().__init__()

class SellerSchema(ma.Schema):
  
  class Meta:
    model = Seller
    fields = ('id', 'assigned_area', 'created_at', 'updated_at', 'user_id')