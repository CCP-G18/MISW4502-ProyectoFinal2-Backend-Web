from unittest.mock import patch, MagicMock
from google.api_core.exceptions import NotFound

from app.utils.bucket_utils import (
    create_customer_folder,
    validate_folder_exists,
    connect_to_bucket,
    generate_name_file,
)

def test_create_customer_folder():
    customer_id = "123abc"
    result = create_customer_folder(customer_id)
    assert result == "123abc/"


def test_validate_folder_exists_true():
    mock_blob = MagicMock()
    mock_blob.reload.return_value = None

    mock_bucket = MagicMock()
    mock_bucket.blob.return_value = mock_blob

    assert validate_folder_exists(mock_bucket, "test_folder/") is True
    mock_bucket.blob.assert_called_once_with("test_folder/")
    mock_blob.reload.assert_called_once()

def test_validate_folder_exists_false():
    mock_blob = MagicMock()
    mock_blob.reload.side_effect = NotFound("not found")

    mock_bucket = MagicMock()
    mock_bucket.blob.return_value = mock_blob

    assert validate_folder_exists(mock_bucket, "nonexistent/") is False


# ---------- connect_to_bucket ----------
@patch("app.utils.bucket_utils.storage.Client")
def test_connect_to_bucket(mock_storage_client_class):
    mock_bucket = MagicMock()
    mock_storage_client = MagicMock()
    mock_storage_client.get_bucket.return_value = mock_bucket
    mock_storage_client_class.return_value = mock_storage_client

    bucket = connect_to_bucket("my-test-bucket")

    mock_storage_client.get_bucket.assert_called_once_with("my-test-bucket")
    assert bucket == mock_bucket


@patch("app.utils.bucket_utils.datetime")
def test_generate_name_file(mock_datetime):
    mock_datetime.now.return_value.strftime.return_value = "20250430_201020"

    result = generate_name_file("video.mp4")
    assert result == "20250430_201020.mp4"

    result = generate_name_file("otro_video.webm")
    assert result.endswith(".webm")
