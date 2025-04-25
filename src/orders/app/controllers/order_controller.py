from flask import Blueprint, request
from app.services.order_service import OrderService
from app.models.order_model import OrderSchema
from app.utils.response_util import format_response
from app.utils.validate_auth_util import get_authenticated_user_id, auth_required, auth_required_with_id
from app.utils.user_status_util import set_user_status
from app.exceptions.http_exceptions import NotFoundError, BadRequestError

order_bp = Blueprint('orders', __name__, url_prefix='/orders')
order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)

@order_bp.route('/', methods=['GET'])
@auth_required
def get_orders():
    try:
        customer_id = get_authenticated_user_id()
        orders = OrderService.get_orders_by_customer(customer_id)
        if not orders:
            return format_response("success", 200, message="No hay pedidos registrados", data=[])
        return format_response("success", 200, message="Todos los pedidos han sido obtenidos", data=orders)
    except Exception as e:
        return format_response("error", 500, message="Ocurrió un error al obtener los pedidos", error=str(e))

@order_bp.route('/<string:id>', methods=['GET'])
def get_order(id:str):
    try:
        order = OrderService.get_by_id(id)
    except (NotFoundError, BadRequestError) as e:
        return format_response("error", e.code, error=e.description)
    else:
        return format_response("success", 200, "Pedido encontrado con éxito", order_schema.dump(order))

    
@order_bp.route('/', methods=['POST'])
@auth_required
def create_order():
    try:
        order_data = request.get_json()
        user_id = get_authenticated_user_id()
        order = OrderService.create(user_id, order_data)
    except (BadRequestError, NotFoundError) as e:
        set_user_status()
        return format_response("error", e.code, error=e.description)
    else:
        return format_response("success", 201, "Pedido creado con éxito", data=order)

@order_bp.route('/ping', methods=['GET'])
def ping():
    return format_response("success", 200, "pong")
