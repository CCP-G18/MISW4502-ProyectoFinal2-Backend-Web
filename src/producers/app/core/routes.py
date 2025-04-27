from app.controllers.producer_controller import producer_bp

def register_routes(app):
    app.register_blueprint(producer_bp)