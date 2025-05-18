import pytest
from unittest.mock import MagicMock, patch
from app.services.visit_route_service import VisitRouteService
from app.exceptions.http_exceptions import BadRequestError, NotFoundError

@patch("app.repositories.visit_route_repository.VisitRouteRepository.get_all")
def test_get_all_visit_routes_success(mock_get_all):
    mock_get_all.return_value = [
        {"id": "route-id-1", "route_name": "Ruta Norte"},
        {"id": "route-id-2", "route_name": "Ruta Sur"}
    ]

    result = VisitRouteService.get_all()

    assert len(result) == 2
    assert result[0]["route_name"] == "Ruta Norte"
    assert result[1]["route_name"] == "Ruta Sur"

@patch("app.repositories.visit_route_repository.VisitRouteRepository.get_by_id")
def test_get_visit_route_by_id_success(mock_get_by_id):
    mock_get_by_id.return_value = {"id": "b97a03f2-f4a9-44fa-ba8c-364d6ccdbef1", "route_name": "Ruta Norte"}

    result = VisitRouteService.get_by_id("b97a03f2-f4a9-44fa-ba8c-364d6ccdbef1")

    assert result["id"] == "b97a03f2-f4a9-44fa-ba8c-364d6ccdbef1"
    assert result["route_name"] == "Ruta Norte"

@patch("app.repositories.visit_route_repository.VisitRouteRepository.get_by_id")
def test_get_visit_route_by_id_not_found(mock_get_by_id):
    mock_get_by_id.return_value = None

    with pytest.raises(NotFoundError, match="Ruta de visita no encontrada"):
        VisitRouteService.get_by_id("b97a03f2-f4a9-44fa-ba8c-364d6ccdbef1")

@patch("app.repositories.visit_route_repository.VisitRouteRepository.get_by_seller_id")
def test_get_visit_routes_by_seller_success(mock_get_by_seller):
    mock_get_by_seller.return_value = [{"id": "b97a03f2-f4a9-44fa-ba8c-364d6ccdbef1"}]

    result = VisitRouteService.get_by_seller_id("a68e9bdd-f86a-45b1-a466-89034d8d42ad")

    assert len(result) == 1
    assert result[0]["id"] == "b97a03f2-f4a9-44fa-ba8c-364d6ccdbef1"

@patch("app.repositories.visit_route_repository.VisitRouteRepository.get_by_id")
def test_get_visit_route_by_id_invalid(mock_get_by_id):
    with pytest.raises(BadRequestError, match="El formato del id de la ruta no es correcto"):
        VisitRouteService.get_by_id("2289567938784")

@patch("app.repositories.visit_route_repository.VisitRouteRepository.get_by_seller_and_date")
def test_get_by_seller_and_date_success(mock_get_by_seller_date):
    mock_route = MagicMock()
    mock_route.estimated_time = "45 minutos"
    mock_route.visit_date = "2025-05-18"
    mock_get_by_seller_date.return_value = [mock_route]

    result = VisitRouteService.get_by_seller_and_date("b97a03f2-f4a9-44fa-ba8c-364d6ccdbef1", "2025-05-18")

    assert result[0].visit_date == "2025-05-18"

@patch("app.repositories.visit_route_repository.VisitRouteRepository.create")
def test_create_visit_route_missing_field(mock_create):
    invalid_data = {
        "route_name": "Ruta Centro"
    }

    with pytest.raises(BadRequestError, match="El campo visit_date es requerido"):
        VisitRouteService.create(invalid_data)

@patch("app.repositories.visit_route_repository.VisitRouteRepository.create")
def test_create_visit_route_invalid_date(mock_create):
    data = {
        "route_name": "Ruta Este",
        "visit_date": "fecha-inválida",
        "origin_address": "Origen X",
        "origin_lat": 10.0,
        "origin_lng": -74.0,
        "destination_address": "Destino X",
        "destination_lat": 11.0,
        "destination_lng": -75.0,
        "estimated_time": "1h",
        "seller_id": "123e4567-e89b-12d3-a456-426614174000"
    }

    with pytest.raises(BadRequestError, match="La fecha de visita no tiene un formato válido"):
        VisitRouteService.create(data)