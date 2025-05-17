from flask import Blueprint, request
from app.utils.response_util import format_response
from flask_jwt_extended import jwt_required
from app.services.recommendation_service import RecommendationService
from app.models.recommendation_model import RecommendationSchema
from app.exceptions.http_exceptions import BadRequestError


recommendation_bp = Blueprint('recommendation', __name__, url_prefix='/recommendations')
recommendation_schema = RecommendationSchema()

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

@recommendation_bp.route('/ping', methods=['GET'])
def ping():
    return format_response("success", 200, "pong")