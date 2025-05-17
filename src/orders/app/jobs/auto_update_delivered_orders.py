from datetime import datetime, time
from app.models.order_model import Order, OrderStateEnum
from app.core.database import db

def auto_update_delivered_orders(app):
    with app.app_context():
        now = datetime.combine(datetime.utcnow().date(), time.min)
        updated_rows = db.session.query(Order).filter(
            Order.delivery_date <= now,
            Order.state != OrderStateEnum.DELIVERED
        ) \
        .update({ Order.state: OrderStateEnum.DELIVERED }, synchronize_session=False)

        db.session.commit()
        
        print(f"✅ Actualizados {updated_rows} pedidos a 'DELIVERED'")