from app.models.customer_model import Customer
from app.core.database import db

class CustomerRepository:
    @staticmethod
    def get_all():
        return Customer.query.all()

    @staticmethod
    def create(customer: Customer):
        db.session.add(customer)
        db.session.commit()
        return customer