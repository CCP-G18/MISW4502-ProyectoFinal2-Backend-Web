import uuid
from app.core.database import db, ma
from sqlalchemy.dialects.postgresql import UUID

class Recommendation(db.Model):
  __tablename__ = 'recommendations'
    
  id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  video_url = db.Column(db.String(255), nullable=False)
  recommendation_date = db.Column(db.DateTime, nullable=True)
  recommendations = db.Column(db.String(500), nullable=True)
  created_at = db.Column(db.DateTime, server_default=db.func.now())
  updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

  seller_id = db.Column(UUID(as_uuid=True), nullable=False)
  customer_id = db.Column(UUID(as_uuid=True), nullable=False)

  def __init__(
    self,
    video_url,
    seller_id,
    customer_id
  ):
    self.video_url = video_url
    self.seller_id = seller_id
    self.customer_id = customer_id

class RecommendationSchema(ma.SQLAlchemyAutoSchema):
  class Meta:
    model = Recommendation
    load_instance = True
    include_relationship = True
    fields = ('id', 'video_url', 'seller_id', 'customer_id', 'created_at', 'updated_at')
