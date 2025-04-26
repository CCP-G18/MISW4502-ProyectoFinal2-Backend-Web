from app.models.producer_model import Producer
from app.core.database import db

class ProducerRepository:
    @staticmethod
    def get_all():
        return Producer.query.all()

    @staticmethod
    def get_by_id(producer_id):
        return Producer.query.get(producer_id)
    
    @staticmethod
    def get_by_email(email):
        return Producer.query.filter_by(email=email).first()

    @staticmethod
    def create(producer: Producer):
        db.session.add(producer)
        db.session.commit()
        return producer
    