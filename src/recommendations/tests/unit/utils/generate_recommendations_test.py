import os
import base64
import tempfile
import pytest
from unittest.mock import patch, MagicMock
from app.utils.generate_recommendations import ask_gpt_with_images

@patch("app.utils.generate_recommendations.client")
def test_ask_gpt_with_images_success(mock_openai_client):
    # Crear una imagen temporal
    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp_img:
        tmp_img.write(base64.b64decode(
            "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR4nGNgYAAAAAMAASsJTYQAAAAASUVORK5CYII="
        ))
        tmp_img_path = tmp_img.name

    # Mock de la respuesta de OpenAI
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content="Recomendación generada"))]
    mock_openai_client.chat.completions.create.return_value = mock_response

    os.environ["OPENAI_MODEL"] = "gpt-4o"
    result = ask_gpt_with_images([tmp_img_path], "¿Qué hay en esta imagen?")

    assert result == "Recomendación generada"
    mock_openai_client.chat.completions.create.assert_called_once()

@patch("app.utils.generate_recommendations.client")
def test_ask_gpt_with_images_invalid_path(mock_openai_client):
    with pytest.raises(FileNotFoundError):
        ask_gpt_with_images(["no_existe.jpg"], "prompt")
