from app.controllers.recommendation_controller import recommendation_bp


def register_routes(app):
  app.register_blueprint(recommendation_bp)