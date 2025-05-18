import uuid
from app.models.visit_route_model import VisitRoute
from app.core.database import db

class VisitRouteRepository:
    @staticmethod
    def get_all():
        return VisitRoute.query.all()

    @staticmethod
    def get_by_id(route_id):
        if isinstance(route_id, str):
            route_id = uuid.UUID(route_id)
        return VisitRoute.query.get(route_id)

    @staticmethod
    def get_by_seller_id(seller_id):
        if isinstance(seller_id, str):
            seller_id = uuid.UUID(seller_id)
        return VisitRoute.query.filter_by(seller_id=seller_id).all()

    @staticmethod
    def get_by_seller_and_date(seller_id, visit_date):
        if isinstance(seller_id, str):
            seller_id = uuid.UUID(seller_id)
        return VisitRoute.query.filter_by(seller_id=seller_id, visit_date=visit_date).all()

    @staticmethod
    def create(visit_route: VisitRoute):
        db.session.add(visit_route)
        db.session.commit()
        return visit_route