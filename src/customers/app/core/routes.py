from app.controllers.customer_controller import customer_bp


def register_routes(app):
    app.register_blueprint(customer_bp)