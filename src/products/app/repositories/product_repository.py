from app.models.product_model import Product
from app.core.database import db

class ProductRepository:
    @staticmethod
    def create(product: Product):
        db.session.add(product)
        db.session.commit()
        return product