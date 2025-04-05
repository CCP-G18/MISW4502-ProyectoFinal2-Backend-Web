import uuid
import enum
from app.core.database import db, ma
from sqlalchemy.dialects.postgresql import UUID
from marshmallow_enum import EnumField

class DocumentTypeEnum(enum.Enum):
    NIT = "NIT"
    CC = "CC"
    CE = "CE"
    DNI = "DNI"
    PASSPORT = "PASSPORT"

class Customer(db.Model):
    __tablename__ = 'customer'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    identification_type = db.Column(db.Enum(DocumentTypeEnum), nullable=False, default=DocumentTypeEnum.CC)
    identification_number = db.Column(db.Integer, nullable=False)   
    country = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    user_id = db.Column(UUID(as_uuid=True), unique=True, nullable=False)
    
    def __init__(self,
                identification_type,
                identification_number,
                country,
                city,
                address,
                user_id):
        self.identification_type = identification_type
        self.identification_number = identification_number
        self.country = country
        self.city = city
        self.address = address
        self.user_id = user_id
 
        super().__init__()
    
class CustomerSchema(ma.Schema):
    identification_type = EnumField(DocumentTypeEnum, by_value=True)
    class Meta:
        model = Customer
        fields = (
            'id',            
            'identification_type',
            'identification_number',
            'country',
            'city',
            'address',
            'created_at',
            'updated_at',
            'user_id'
        )    