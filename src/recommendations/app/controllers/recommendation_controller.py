from flask import Blueprint, request
from app.utils.response_util import format_response
from flask_jwt_extended import jwt_required
from app.services.recommendation_service import RecommendationService
from app.models.recommendation_model import RecommendationSchema
from app.exceptions.http_exceptions import BadRequestError


recommendation_bp = Blueprint('recommendation', __name__, url_prefix='/recommendations')
recommendation_schema = RecommendationSchema()
recommendations_schema = RecommendationSchema(many=True)

@recommendation_bp.route('', methods=['POST'])
@jwt_required()
def create_recommendation():
    try:
        video = request.files['video']
        recommendation_data = {
            'customer_id': request.form['customer_id'],
            'seller_id': request.form['seller_id']
        }
        recommendation = RecommendationService.create(recommendation_data, video)
        return format_response("success", 201, "Recomendación creada correctamente", recommendation_schema.dump(recommendation))
    except BadRequestError as e:
        return format_response("error", e.code, error=e.description)
    

@recommendation_bp.route('<string:recommendation_id>', methods=['PUT'])
@jwt_required()
def generate_recommendation(recommendation_id):
    try:
        recommendation = RecommendationService.generate(recommendation_id)
        return format_response("success", 200, "Recomendación generada correctamente", recommendation_schema.dump(recommendation))
    except BadRequestError as e:
        return format_response('error', e.code, error=e.description)

@recommendation_bp.route('/sellers/<string:seller_id>/customers/<string:customer_id>', methods=['GET'])
def get_recommendations_seller_customer(seller_id, customer_id):
    try:
        recommendations = RecommendationService.get_recommendations_by_seller_by_customer(seller_id, customer_id)
        if not recommendations:
            return format_response("success", 200, "No hay recomendaciones", recommendations_schema.dump(recommendations))
        return format_response("success", 200, "Recomendaciones obtenidas con exito", recommendations_schema.dump(recommendations))
    except BadRequestError as e:
        return format_response('error', e.code, error=e.description)


@recommendation_bp.route('/ping', methods=['GET'])
def ping():
    return format_response("success", 200, "pong")