from app.controllers.product_controller import product_bp


def register_routes(app):
  app.register_blueprint(product_bp)