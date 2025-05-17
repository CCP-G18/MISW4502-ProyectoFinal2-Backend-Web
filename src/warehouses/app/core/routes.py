from app.controllers.warehouse_controller import warehouse_bp


def register_routes(app):
  app.register_blueprint(warehouse_bp)