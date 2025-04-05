from app.controllers.seller_controller import seller_bp


def register_routes(app):
  app.register_blueprint(seller_bp)