from app.models.order_model import Order
from app.core.database import db

class OrderRepository:
    @staticmethod
    def get_all():
        return Order.query.all()

    @staticmethod
    def get_by_id(order_id):
        return Order.query.get(order_id)

    @staticmethod
    def create(order: Order):
        db.session.add(order)
        db.session.commit()
        return order
    
    @staticmethod
    def update_total_amount(order_id, total_amount):
        order = Order.query.get(order_id)
        order.total_amount = total_amount
        db.session.commit()
        return order