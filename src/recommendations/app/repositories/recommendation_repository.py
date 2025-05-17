from app.models.recommendation_model import Recommendation
from app.core.database import db

class RecommendationRepository:

    @staticmethod
    def create(recommendation):
        recommendation = Recommendation(
            customer_id=recommendation.get("customer_id"),
            seller_id=recommendation.get("seller_id"),
            video_url=recommendation.get("video_url"),
        )

        db.session.add(recommendation)
        db.session.commit()

        return recommendation
    
    @staticmethod
    def get_by_id(recommendation_id) -> Recommendation:
        return Recommendation.query.filter_by(id=recommendation_id).first()
    
    @staticmethod
    def update_recommendation(recommendation_updated: Recommendation, recommendations):
        recommendation_updated.recommendations = recommendations
        db.session.commit()

        return recommendation_updated