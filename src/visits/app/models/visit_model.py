import uuid
from app.core.database import db, ma
from sqlalchemy.dialects.postgresql import UUID

class Visit(db.Model):
    __tablename__ = 'visits'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    observations = db.Column(db.Text, nullable=False)
    register_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    customer_id = db.Column(UUID(as_uuid=True), unique=True, nullable=False)
    seller_id = db.Column(UUID(as_uuid=True), unique=True, nullable=False)

    def __init__(self, observations, register_date, customer_id, seller_id):
        self.observations = observations
        self.register_date = register_date
        self.customer_id = customer_id
        self.seller_id = seller_id

        super().__init__()
    
    def __repr__(self):
        return '<Visit %r>' % self.id
    
class VisitSchema(ma.Schema):
    class Meta:
        model = Visit
        fields = ('id', 'observations', 'register_date', 'customer_id', 'seller_id', 'created_at', 'updated_at')
    