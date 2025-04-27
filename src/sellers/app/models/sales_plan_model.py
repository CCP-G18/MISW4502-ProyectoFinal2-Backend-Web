import uuid
from app.core.database import db, ma
from sqlalchemy.dialects.postgresql import UUID

class SalesPlan(db.Model):
  __tablename__ = 'sales_plan'

  id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  initial_date = db.Column(db.DateTime, nullable=False)
  end_date = db.Column(db.DateTime, nullable=False)
  sales_goals = db.Column(db.Float, nullable=False)
  created_at = db.Column(db.DateTime, server_default=db.func.now())
  updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

  seller_id = db.Column(UUID(as_uuid=True), nullable=False)

  def __init__(self, initial_date, end_date, sales_goals, seller_id):
    self.initial_date = initial_date
    self.end_date = end_date
    self.sales_goals = sales_goals
    self.seller_id = seller_id

    super().__init__()

  @staticmethod
  def get_sales_plan_by_seller(seller_id):
    return db.session.query(SalesPlan).filter(SalesPlan.seller_id == seller_id).all()

class SalesPlanSchema(ma.SQLAlchemyAutoSchema):
  class Meta:
    model = SalesPlan
    load_instance = True
    include_relationship = True
    fields = ('id', 'initial_date', 'end_date', 'sales_goals', 'seller_id', 'created_at', 'updated_at')
