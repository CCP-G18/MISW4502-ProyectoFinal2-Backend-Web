import uuid
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import db, ma
import enum
from marshmallow_enum import EnumField
from sqlalchemy.orm import relationship

class OrderStateEnum(enum.Enum):
    PREPARING = "PREPARING"
    ON_ROUTE = "ON_ROUTE"
    DELIVERED = "DELIVERED"

class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, server_default=db.text("gen_random_uuid()"), unique=True, nullable=False)
    customer_id = db.Column(UUID(as_uuid=True), nullable=False)
    seller_id = db.Column(UUID(as_uuid=True), nullable=True, default=None)
    state = db.Column(db.Enum(OrderStateEnum), nullable=False, default=OrderStateEnum.PREPARING)
    total_amount = db.Column(db.Float, nullable=False)
    delivery_date = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    items = relationship("OrderProducts", backref="order", lazy="joined")
    
    def __init__(self,
                customer_id,
                total_amount,
                delivery_date,
                state=OrderStateEnum.PREPARING,
                seller_id=None):
        self.customer_id = customer_id
        self.state = state
        self.total_amount = total_amount
        self.delivery_date = delivery_date
        self.seller_id = seller_id
        
        super().__init__()
    
class OrderSchema(ma.Schema):
    state = EnumField(OrderStateEnum, by_value=True)
    class Meta:
        model = Order
        fields = (
            'id',
            'customer_id',
            'seller_id',
            'state',
            'total_amount',
            'delivery_date',
            'created_at',
            'updated_at')