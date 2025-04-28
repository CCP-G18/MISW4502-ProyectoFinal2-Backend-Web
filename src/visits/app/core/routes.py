from app.controllers.visit_controller import visit_bp

def register_routes(app):
    app.register_blueprint(visit_bp)