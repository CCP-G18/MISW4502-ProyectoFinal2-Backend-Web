order_bp = Blueprint('order', __name__, url_prefix="/orders")
order_schema = OrderSchema()


@order_bp.route('/', methods=['GET'])
@jwt_required()
def get_orders():
    try:
        orders = OrderService.get_all()
        return format_response("success", 200, "", orders)
    except BadRequestError as e:
        return format_response("error", e.code, error=e.description)
  
@order_bp.route('/ping', methods=['GET'])
def ping():
    return format_response("success", 200, "pong")
