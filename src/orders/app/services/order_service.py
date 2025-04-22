import uuid
from datetime import datetime
from app.repositories.order_repository import OrderRepository
from app.repositories.order_product_repository import OrderProductRepository
from app.exceptions.http_exceptions import BadRequestError, NotFoundError
from app.models.order_model import Order
from app.models.order_product_model import OrderProducts
from app.utils.delivery_date_util import get_delivery_date
from app.utils.product_info_util import get_product_info


def validate_uuid(id):
    try:
        uuid.UUID(id, version=4)
        return True
    except ValueError:
        return False

class OrderService:
    @staticmethod
    def get_all():
        orders = OrderRepository.get_all()
        if not orders:
            raise ValueError("No hay pedidos registrados")
        return orders

    @staticmethod
    def get_by_id(order_id):

        if not validate_uuid(order_id):
            raise BadRequestError("El formato del id del pedido no es correcto")
        
        order = OrderRepository.get_by_id(order_id)
        if not order:
            raise NotFoundError("Pedido no encontrado")
        return order

    @staticmethod
    def create(user_id, order_data):
        if set(order_data.keys()) != {"products_id_list"}:
            raise BadRequestError("Existen datos inconsistentes en la petición, se hará un bloqueo preventivo de su cuenta")
        
        order = Order(user_id=user_id, delivery_date=get_delivery_date(datetime.today().date()))
        OrderRepository.create(order)

        for product_id in order_data.get("products_id_list"):
            product = get_product_info(str(product_id))
            if not product:
                raise NotFoundError("Producto no encontrado, se hará un bloqueo preventivo de su cuenta por datos inconsistentes")
            OrderProductRepository.create(OrderProducts(order_id=str(order.id), product_id=product_id, quantity=1))
        
        return order
    
    @staticmethod
    def get_orders_by_customer(customer_id):
        orders = Order.query.filter_by(customer_id=customer_id).all()
        result = []

        for order in orders:
            items = []
            summary = []
            for order_product in order.order_products:
                product_info = get_product_info(order_product.product_id)
                if product_info:
                    items.append({
                        "title": product_info.get("name"),
                        "quantity": order_product.quantity_ordered,
                        "price": order_product.amount,
                        #"image_url": product_info.get("image_url")
                    })
                    summary.append(product_info.get("name"))

            result.append({
                "id": str(order.id),
                "summary": ", ".join(summary[:3]) + ("..." if len(summary) > 3 else ""),
                "date": order.delivery_date.strftime("%Y-%m-%d"),
                "total": order.total_amount,
                "status": order.state.value,
                "items": items
            })

        print(result)
        return result