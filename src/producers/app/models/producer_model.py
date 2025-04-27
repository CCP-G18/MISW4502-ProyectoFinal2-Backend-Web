import uuid
from app.core.database import db, ma
from sqlalchemy.dialects.postgresql import UUID

class Producer(db.Model):
    __tablename__ = 'producers'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(120), nullable=False)
    country = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    address = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(255), nullable=False)
    website = db.Column(db.String(255), nullable=False)
    contact_name = db.Column(db.String(255), nullable=False)
    contact_lastname = db.Column(db.String(255), nullable=False)
    contact_email = db.Column(db.String(255), nullable=False)
    contact_phone = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def __init__(self, name, country, email, address, phone, website, contact_name, contact_lastname, contact_email, contact_phone):
        self.name = name
        self.country = country
        self.email = email
        self.address = address
        self.phone = phone
        self.website = website
        self.contact_name = contact_name
        self.contact_lastname = contact_lastname
        self.contact_email = contact_email
        self.contact_phone = contact_phone

        super().__init__()
    
    def __repr__(self):
        return '<Producer %r>' % self.id
    
class ProducerSchema(ma.Schema):
    class Meta:
        model = Producer
        fields = ('id', 'name', 'country', 'email', 'created_at', 'updated_at')
    