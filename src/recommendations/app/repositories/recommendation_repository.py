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