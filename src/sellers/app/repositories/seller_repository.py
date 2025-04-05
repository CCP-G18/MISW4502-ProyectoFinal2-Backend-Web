from app.models.seller_model import Seller
from app.core.database import db

class SellerRepository:
    
    @staticmethod
    def get_all():
        sellers = Seller.query.all()
        
        return sellers
    
    @staticmethod
    def create(seller):
        seller = Seller(
            assigned_area=seller.get("assigned_area"),
            user_id=seller.get("user_id")
        )
        db.session.add(seller)
        db.session.commit()

        return seller