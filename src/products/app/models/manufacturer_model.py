import uuid
from app.core.database import db
from sqlalchemy.dialects.postgresql import UUID

class Manufacturer(db.Model):
    __tablename__ = 'producers'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(120), nullable=False)