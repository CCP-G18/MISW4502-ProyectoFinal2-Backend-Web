from app.models.product_model import Product
from app.models.category_model import Category
from app.core.database import db

class ProductRepository:
  
  @staticmethod
  def get_all():
    products = Product.query.all()    
    return products
  
  @staticmethod
  def create(product: Product):
    db.session.add(product)
    db.session.commit()
    
    return product
  
  @staticmethod
  def get_product_by_id(product_id):
    return Product.query.get(product_id)
  
  @staticmethod
  def update(product: Product):
    db.session.commit()
    return product
  
  @staticmethod
  def get_products_by_category(category_id):
    products = Product.query.filter_by(category_id=category_id).all()  
    return products
  
  @staticmethod
  def get_categories():
    categories = Category.query.all()    
    return categories