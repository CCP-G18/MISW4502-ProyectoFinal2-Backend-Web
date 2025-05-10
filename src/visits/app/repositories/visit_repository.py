
import uuid
from app.models.visit_model import Visit
from app.core.database import db

class VisitRepository:
    @staticmethod
    def get_all():
        return Visit.query.all()

    @staticmethod
    def get_by_id(visit_id):
        if isinstance(visit_id, str):
            visit_id = uuid.UUID(visit_id)
        return Visit.query.get(visit_id)
    
    @staticmethod
    def get_by_id_customer(customer_id):
        if isinstance(customer_id, str):
            customer_id = uuid.UUID(customer_id)
        return Visit.query.filter_by(customer_id=customer_id).all()
    
    @staticmethod
    def get_by_email(email):
        return Visit.query.filter_by(email=email).first()

    @staticmethod
    def create(visit: Visit):
        db.session.add(visit)
        db.session.commit()
        return visit
    