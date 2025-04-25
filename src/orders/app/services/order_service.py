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
    def create(customer_id, order_data):
        if "items" not in order_data or not isinstance(order_data["items"], list):
            raise BadRequestError("La petición debe contener una lista de productos válida")

        order = Order(
            customer_id=customer_id,
            total_amount=order_data["total"],            
            delivery_date=get_delivery_date(order_data["date"])
        )
        order = OrderRepository.create(order)
        items = []
        summary = []

        for product_data in order_data["items"]:
            product_id = product_data.get("product_id")
            quantity = product_data.get("quantity")        
            amount = product_data.get("price")
           
            if not product_id or not validate_uuid(product_id):
                raise BadRequestError("El ID del producto no es válido")
            if not isinstance(quantity, int) or quantity <= 0:
                raise BadRequestError("La cantidad debe ser un número entero positivo")

            product_info = get_product_info(str(product_id))
            if not product_info:
                raise NotFoundError("Producto no encontrado, se hará un bloqueo preventivo de su cuenta por datos inconsistentes")
          
            product_name = product_info["data"].get("name")
            product_price = product_info["data"].get("unit_amount", 0.0)
            product_image_url = product_info["data"].get("image_url")

            if product_name:
                summary.append(product_name)


            order_product = OrderProducts(
                order_id=str(order.id),
                product_id=product_id,
                quantity_ordered=quantity,
                amount=amount
            )
            OrderProductRepository.create(order_product)

            items.append({
                "title": product_name,
                "quantity": quantity,
                "price": product_price,
                "image_url": product_image_url
            })

        OrderRepository.update_total_amount(order.id, order_data["total"])

        response = {
            "order_id": str(order.id),
            "summary": ", ".join(summary[:3]) + ("..." if len(summary) > 3 else ""),
            "date": order.delivery_date.strftime("%Y-%m-%d"),
            "total": order.total_amount,
            "status": order.state.value,
            "items": items
        }

        return response
    
    @staticmethod
    def get_orders_by_customer(customer_id):        
        orders = Order.query.filter(Order.customer_id == customer_id).all()
        result = []

        for order in orders:
            items = []
            summary = []
            for order_product in order.items:
                product_info = get_product_info(order_product.product_id)
                if product_info and product_info.get("data"):
                    product_name = product_info["data"].get("name")
                    if product_name:
                        summary.append(product_name)
                    items.append({
                        "title": product_name,
                        "quantity": order_product.quantity_ordered,
                        "price": order_product.amount,
                        "image_url": product_info["data"].get("image_url")
                    })

            result.append({
                "order_id": str(order.id),
                "summary": ", ".join(summary[:3]) + ("..." if len(summary) > 3 else ""),
                "date": order.delivery_date.strftime("%Y-%m-%d"),
                "total": order.total_amount,
                "status": order.state.value,
                "items": items
            })

        return result