import uuid
from app.core.database import db, ma
from sqlalchemy.dialects.postgresql import UUID

class VisitRoute(db.Model):
    __tablename__ = 'visit_routes'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    route_name = db.Column(db.String(255), nullable=False)
    visit_date = db.Column(db.Date, nullable=False)
    origin_address = db.Column(db.String(255), nullable=False)
    origin_lat = db.Column(db.Float, nullable=False)
    origin_lng = db.Column(db.Float, nullable=False)
    destination_address = db.Column(db.String(255), nullable=False)
    destination_lat = db.Column(db.Float, nullable=False)
    destination_lng = db.Column(db.Float, nullable=False)
    estimated_time = db.Column(db.String(50), nullable=False)
    seller_id = db.Column(UUID(as_uuid=True), nullable=False)
    
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())    

    def __init__(self, route_name, visit_date, origin_address, origin_lat, origin_lng, destination_address, destination_lat, destination_lng, estimated_time, seller_id):
        self.route_name = route_name
        self.visit_date = visit_date
        self.origin_address = origin_address
        self.origin_lat = origin_lat
        self.origin_lng = origin_lng
        self.destination_address = destination_address
        self.destination_lat = destination_lat
        self.destination_lng = destination_lng
        self.estimated_time = estimated_time
        self.seller_id = seller_id
        super().__init__()

    def __repr__(self):
        return f'<VisitRoute {self.id}>'

class VisitRouteSchema(ma.Schema):
    class Meta:
        model = VisitRoute
        fields = (
            'id',
            'route_name',
            'visit_date',
            'origin_address',
            'origin_lat',
            'origin_lng',
            'destination_address',
            'destination_lat',
            'destination_lng',
            'estimated_time',
            'seller_id',
            'created_at',
            'updated_at'
        )