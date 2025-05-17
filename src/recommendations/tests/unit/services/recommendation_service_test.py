import pytest
import os
from unittest.mock import patch, MagicMock
from app.services.recommendation_service import RecommendationService
from app.exceptions.http_exceptions import BadRequestError

@pytest.fixture
def valid_recommendation_data():
    return {
        "seller_id": "e2c1f6cb-648e-4c27-b3fb-f01d1bfc2a56",
        "customer_id": "9cb2380f-c4be-4be0-983f-4e4c2556f4d4"
    }

@pytest.fixture
def mock_video():
    mock = MagicMock()
    mock.filename = "test_video.mp4"
    return mock

def test_create_should_raise_if_video_missing(valid_recommendation_data):
    with pytest.raises(BadRequestError, match="El video no se encuentra cargado"):
        RecommendationService.create(valid_recommendation_data, None)

def test_create_should_raise_if_seller_id_missing(mock_video):
    data = {"customer_id": "9cb2380f-c4be-4be0-983f-4e4c2556f4d4"}
    with pytest.raises(BadRequestError, match="El vendedor es requerido"):
        RecommendationService.create(data, mock_video)

def test_create_should_raise_if_customer_id_invalid(mock_video):
    data = {
        "seller_id": "e2c1f6cb-648e-4c27-b3fb-f01d1bfc2a56",
        "customer_id": "invalid-uuid"
    }
    with pytest.raises(BadRequestError, match="El cliente no es valido"):
        RecommendationService.create(data, mock_video)

@patch("app.services.recommendation_service.RecommendationRepository.create")
@patch("app.services.recommendation_service.create_customer_folder", return_value="cliente/")
@patch("app.services.recommendation_service.connect_to_bucket")
@patch("app.services.recommendation_service.generate_name_file", return_value="video_20250430_123456.mp4")
def test_create_successful(mock_generate_name_file, mock_connect_to_bucket, mock_create_folder, mock_repo, valid_recommendation_data, mock_video):
    mock_blob = MagicMock()
    mock_bucket = MagicMock()
    mock_bucket.blob.return_value = mock_blob
    mock_connect_to_bucket.return_value = mock_bucket
    mock_repo.return_value = {"id": "abc123"}

    result = RecommendationService.create(valid_recommendation_data, mock_video)

    expected_path = "cliente/video_20250430_123456.mp4"
    mock_blob.upload_from_file.assert_called_once_with(mock_video)
    mock_repo.assert_called_once_with({
        "customer_id": valid_recommendation_data["customer_id"],
        "seller_id": valid_recommendation_data["seller_id"],
        "video_url": expected_path
    })
    assert result == {"id": "abc123"}

@patch("app.services.recommendation_service.RecommendationRepository.get_by_id", return_value=None)
def test_generate_should_raise_if_recommendation_not_found(mock_get_by_id):
    with pytest.raises(BadRequestError, match="La recomendación no existe"):
        RecommendationService.generate("nonexistent-id")

@patch("app.services.recommendation_service.ask_gpt_with_images", return_value="Recomendación generada")
@patch("app.services.recommendation_service.extract_frames")
@patch("app.services.recommendation_service.download_video_from_gcs")
@patch("app.services.recommendation_service.RecommendationRepository.get_by_id")
@patch("app.services.recommendation_service.RecommendationRepository.update_recommendation")
def test_generate_should_return_updated_recommendation(
    mock_update, mock_get_by_id, mock_download, mock_extract, mock_ask_gpt
):
    mock_recommendation = MagicMock()
    mock_recommendation.video_url = "customer/video.mp4"
    mock_recommendation.id = "abc123"
    mock_get_by_id.return_value = mock_recommendation
    mock_update.return_value = "updated"

    os.environ["OPENAI_PROMPT"] = "Test prompt"
    os.environ["OPENAI_NRO_FRAMES"] = "1"
    os.makedirs("frames", exist_ok=True)
    with open("frames/test.jpg", "wb") as f:
        f.write(b"fake image")

    result = RecommendationService.generate("abc123")

    assert result == "updated"
    mock_download.assert_called_once()
    mock_extract.assert_called_once()
    mock_ask_gpt.assert_called_once()
    mock_update.assert_called_once()