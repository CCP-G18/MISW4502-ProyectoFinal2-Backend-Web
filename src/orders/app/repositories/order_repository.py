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
    
    def create_order(order: Order):
        """
        Agrega la orden a la sesión y sincroniza con la base de datos para obtener el ID.
        """
        db.session.add(order)
        db.session.flush()  # Sincroniza con la base de datos para obtener el ID
        return order
    
    @staticmethod
    def update(order: Order):
        db.session.commit()
        return order