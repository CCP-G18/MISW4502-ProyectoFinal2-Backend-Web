from app.models.seller_model import Seller
from app.models.sales_plan_model import SalesPlan
from app.models.order_model import Order
from app.core.database import db

class SellerRepository:
    
    @staticmethod
    def get_all():
        sellers = Seller.query.all()
        
        return sellers
    
    def get_by_id(seller_id):
        return Seller.query.filter_by(id=seller_id).first()
    
    @staticmethod
    def create(seller):
        seller = Seller(
            assigned_area=seller.get("assigned_area"),
            user_id=seller.get("user_id")
        )
        db.session.add(seller)
        db.session.commit()

        return seller
    
    @staticmethod
    def get_all_sales_plan_by_seller(seller_id):
        return SalesPlan.get_sales_plan_by_seller(seller_id)
    
    @staticmethod
    def create_sales_plan_by_seller(seller_id, sales_plan):
        sales_plan = SalesPlan(
            initial_date=sales_plan.get("initial_date"),
            end_date=sales_plan.get("end_date"),
            sales_goals=sales_plan.get("sales_goals"),
            seller_id=seller_id
        )
        db.session.add(sales_plan)
        db.session.commit()

        return sales_plan
    
    @staticmethod
    def get_all_orders_by_seller(seller_id):
        return Order.query.filter_by(seller_id=seller_id).all()
