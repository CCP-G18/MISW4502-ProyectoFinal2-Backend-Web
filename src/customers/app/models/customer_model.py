import uuid
import enum
from app.core.database import db, ma
from sqlalchemy.dialects.postgresql import UUID
from werkzeug.security import generate_password_hash, check_password_hash
from marshmallow_enum import EnumField

class DocumentTypeEnum(enum.Enum):
    NIT = "NIT"
    CC = "CC"
    CE = "CE"
    DNI = "DNI"
    PASSPORT = "PASSPORT"

class RoleEnum(enum.Enum):
    CLIENTE = "Cliente"

class Customer(db.Model):
    __tablename__ = 'customer'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    identification_type = db.Column(db.Enum(DocumentTypeEnum), nullable=False, default=DocumentTypeEnum.CC)
    identification_number = db.Column(db.Integer, nullable=False)
    role = db.Column(db.Enum(RoleEnum), nullable=False, default=RoleEnum.CLIENTE)    
    country = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def __repr__(self):
        return '<Customer %r>' % self.identification_number
    
class CustomerSchema(ma.Schema):
    identification_type = EnumField(DocumentTypeEnum, by_value=True)
    role = EnumField(RoleEnum, by_value=True)
    class Meta:
        model = Customer
        fields = (
            'id',
            'identification_type',
            'identification_number',
            'role',
            'country',
            'city',
            'address',
            'created_at',
            'updated_at'
        )    