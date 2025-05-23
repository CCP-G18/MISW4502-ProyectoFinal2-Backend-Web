from app.models.order_product_model import OrderProducts
from app.core.database import db

class OrderProductRepository:

    @staticmethod
    def create(order_product: OrderProducts):
        db.session.add(order_product)
        db.session.commit()
        return order_product
    
    @staticmethod
    def create_order_product(order_product: OrderProducts):
        db.session.add(order_product)
        return order_product