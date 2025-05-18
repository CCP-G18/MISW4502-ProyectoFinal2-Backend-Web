import uuid
import os
from app.exceptions.http_exceptions import BadRequestError
from werkzeug.utils import secure_filename
from app.utils.bucket_utils import create_customer_folder, connect_to_bucket, generate_name_file, download_video_from_gcs, cleanup_files
from app.utils.extract_frames import extract_frames
from app.utils.generate_recommendations import ask_gpt_with_images
from app.repositories.recommendation_repository import RecommendationRepository


def validate_uuid(id):
    try:
        uuid.UUID(id, version=4)
        return True
    except ValueError:
        return False


class RecommendationService:

    BUCKET_NAME = os.getenv("NAME_BUCKET_RECOMMENDATIONS")
    DESTINATION_FILE = "video.mp4"
    OUTPUT_DIR = "frames"

    @staticmethod
    def create(recommendation_data, video):
        if not video:
            raise BadRequestError("El video no se encuentra cargado")
        if not recommendation_data.get("seller_id"):
            raise BadRequestError("El vendedor es requerido")
        if not validate_uuid(recommendation_data.get("seller_id")):
            raise BadRequestError("El vendedor no es valido")
        if not recommendation_data.get("customer_id"):
            raise BadRequestError("El cliente es requerido")
        if not validate_uuid(recommendation_data.get("customer_id")):
            raise BadRequestError("El cliente no es valido")
        
        filename_secure = secure_filename(generate_name_file(video.filename))
        bucket = connect_to_bucket(RecommendationService.BUCKET_NAME)
        folder_user = create_customer_folder(recommendation_data.get("customer_id"))
        filename_path = f'{folder_user}{filename_secure}'

        blob = bucket.blob(filename_path)
        blob.upload_from_file(video)

        recommendation = {
            "customer_id": recommendation_data.get("customer_id"),
            "seller_id": recommendation_data.get("seller_id"),
            "video_url": filename_path
        }

        return RecommendationRepository.create(recommendation)

    @staticmethod
    def generate(recommendation_id):
        recommendation = RecommendationRepository.get_by_id(recommendation_id)
        if not recommendation:
            raise BadRequestError("La recomendación no existe")
        download_video_from_gcs(
            RecommendationService.BUCKET_NAME, 
            recommendation.video_url, 
            RecommendationService.DESTINATION_FILE
        )
        extract_frames(
            RecommendationService.DESTINATION_FILE,
            RecommendationService.OUTPUT_DIR,
            int(os.getenv("OPENAI_NRO_FRAMES"))
        )
        prompt= os.getenv("OPENAI_PROMPT")
        image_paths = [
            os.path.join(RecommendationService.OUTPUT_DIR, f) 
            for f in os.listdir(RecommendationService.OUTPUT_DIR)
        ]
        response = ask_gpt_with_images(image_paths, prompt)

        cleanup_files(RecommendationService.DESTINATION_FILE, RecommendationService.OUTPUT_DIR)

        return RecommendationRepository.update_recommendation(recommendation, response)
    
    @staticmethod
    def get_recommendations_by_seller_by_customer(seller_id:str, customer_id: str):
        recommendations = RecommendationRepository.get_recommendations_by_seller_by_customer(seller_id, customer_id)
        return recommendations