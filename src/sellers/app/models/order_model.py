import uuid
from app.core.database import db
from sqlalchemy.dialects.postgresql import UUID

class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    seller_id = db.Column(UUID(as_uuid=True), nullable=True, default=None)
    total_amount = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
