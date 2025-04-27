import uuid
from datetime import datetime
from app.repositories.order_repository import OrderRepository
from app.repositories.order_product_repository import OrderProductRepository
from app.exceptions.http_exceptions import BadRequestError, NotFoundError
from app.models.order_model import Order
from app.models.order_product_model import OrderProducts
from app.utils.delivery_date_util import get_delivery_date
from app.utils.product_info_util import get_product_info, update_product_quantity
from sqlalchemy.exc import SQLAlchemyError
from app.core.database import db


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
    def create_order(customer_id, order_data):
        if not order_data.get("date"):
             raise BadRequestError("El campo 'date' es obligatorio")
        if not order_data.get("items") or not isinstance(order_data.get("items"), list):
            raise BadRequestError("La petición debe contener una lista de productos válida")
        
        validated_items, total_amount, summary = OrderService.validate_products(order_data["items"])

        try:
            with db.session.begin():
                order = Order(
                    customer_id=customer_id,
                    total_amount=total_amount,
                    delivery_date=get_delivery_date(order_data["date"])
                )
                order_created = OrderRepository.create_order(order)

                for item in validated_items:
                    order_product = OrderProducts(
                        order_id=order_created.id,
                        product_id=item["product_id"],
                        quantity_ordered=item["quantity"],
                        amount=item["amount"]
                    )
                    OrderProductRepository.create_order_product(order_product)

                    update_product_quantity(item["product_id"], item["quantity"])

        except SQLAlchemyError as e:
            db.session.rollback()
            raise BadRequestError("Ocurrió un error al crear la orden. Inténtalo de nuevo.")
        
        response = {
            "order_id": str(order_created.id),
            "summary": ", ".join(summary[:3]) + ("..." if len(summary) > 3 else ""),
            "date": order_created.delivery_date.strftime("%Y-%m-%d"),
            "total": total_amount,
            "status": order_created.state.value,
            "items": [
                {
                    "title": item["name"],
                    "quantity": item["quantity"],
                    "price": item["price"],
                    "image_url": item["image_url"]
                }
                for item in validated_items
            ]
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
    
    @staticmethod
    def validate_products(items):
        total_amount = 0.0
        validated_items = []
        summary = []
        
        for product_data in items:
            product_id = product_data.get("product_id")
            quantity = product_data.get("quantity")

            if "product_id" not in product_data or "quantity" not in product_data:
                raise BadRequestError("Cada producto debe incluir 'product_id' y 'quantity'")
           
            if not product_id or not validate_uuid(product_id):
                raise BadRequestError("El ID del producto no es válido")
            if not isinstance(quantity, int) or quantity <= 0:
                raise BadRequestError("La cantidad debe ser un número entero positivo")

            product_info = get_product_info(str(product_id))
            if not product_info:
                raise NotFoundError(f"Producto con ID {product_id} no encontrado")
            
            product_quantity = product_info["data"].get("quantity", 0)
            if product_quantity - quantity < 0:
                raise BadRequestError(f"No hay suficiente cantidad del producto {product_info['data'].get('name')} en stock")

            product_price = product_info["data"].get("unit_amount", 0.0)
            amount = product_price * quantity
            total_amount += amount

            validated_items.append({
                "product_id": product_id,
                "quantity": quantity,
                "amount": amount,
                "name": product_info["data"].get("name"),
                "image_url": product_info["data"].get("image_url"),
                "price": product_price
            })

            if product_info["data"].get("name"):
                summary.append(product_info["data"].get("name"))

        return validated_items, total_amount, summary