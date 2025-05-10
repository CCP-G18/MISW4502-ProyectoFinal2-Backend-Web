import uuid
from app.exceptions.http_exceptions import BadRequestError
from werkzeug.utils import secure_filename
from app.utils.bucket_utils import create_customer_folder, connect_to_bucket, generate_name_file
from app.repositories.recommendation_repository import RecommendationRepository


def validate_uuid(id):
    try:
        uuid.UUID(id, version=4)
        return True
    except ValueError:
        return False


class RecommendationService:

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
        bucket = connect_to_bucket("recommendations-videos")
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

        
        