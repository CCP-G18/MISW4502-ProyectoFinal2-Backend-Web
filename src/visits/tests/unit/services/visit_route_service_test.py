import uuid
import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime

from app.services.visit_route_service import VisitRouteService
from app.exceptions.http_exceptions import BadRequestError, NotFoundError


@patch("app.repositories.visit_route_repository.VisitRouteRepository.get_all")
def test_get_all_routes_success(mock_get_all):
    mock_get_all.return_value = [MagicMock(id=uuid.uuid4()), MagicMock(id=uuid.uuid4())]

    result = VisitRouteService.get_all()

    assert len(result) == 2
    mock_get_all.assert_called_once()

@patch("app.repositories.visit_route_repository.VisitRouteRepository.get_by_id")
def test_get_route_by_id_success(mock_get_by_id):
    route_id = str(uuid.uuid4())
    mock_route = MagicMock(id=route_id)
    mock_get_by_id.return_value = mock_route

    result = VisitRouteService.get_by_id(route_id)

    assert result == mock_route
    mock_get_by_id.assert_called_once_with(route_id)

@patch("app.repositories.visit_route_repository.VisitRouteRepository.get_by_id")
def test_get_route_by_id_invalid_uuid(mock_get_by_id):
    with pytest.raises(BadRequestError):
        VisitRouteService.get_by_id("invalid-uuid")

    mock_get_by_id.assert_not_called()

@patch("app.repositories.visit_route_repository.VisitRouteRepository.get_by_id")
def test_get_route_by_id_not_found(mock_get_by_id):
    route_id = str(uuid.uuid4())
    mock_get_by_id.return_value = None

    with pytest.raises(NotFoundError):
        VisitRouteService.get_by_id(route_id)

@patch("app.repositories.visit_route_repository.VisitRouteRepository.get_by_seller_id")
def test_get_routes_by_seller_id_success(mock_get_by_seller):
    seller_id = str(uuid.uuid4())
    mock_routes = [MagicMock(id=uuid.uuid4())]
    mock_get_by_seller.return_value = mock_routes

    result = VisitRouteService.get_by_seller_id(seller_id)

    assert result == mock_routes
    mock_get_by_seller.assert_called_once_with(seller_id)

@patch("app.repositories.visit_route_repository.VisitRouteRepository.create")
def test_create_route_missing_field(mock_create):
    route_data = {
        "visit_date": "2025-05-18",
        "seller_id": str(uuid.uuid4())
    }
    with pytest.raises(BadRequestError):
        VisitRouteService.create(route_data)

    mock_create.assert_not_called()

@patch("app.repositories.visit_route_repository.VisitRouteRepository.create")
def test_create_route_invalid_uuid(mock_create):
    route_data = {
        "visit_date": "2025-05-18",
        "seller_id": "invalid",
        "customer_id": str(uuid.uuid4())
    }
    with pytest.raises(BadRequestError):
        VisitRouteService.create(route_data)

    mock_create.assert_not_called()

@patch("app.repositories.visit_route_repository.VisitRouteRepository.get_by_seller_and_date")
def test_get_routes_by_seller_and_date_success(mock_get):
    seller_id = str(uuid.uuid4())
    visit_date_str = datetime.now().strftime("%Y-%m-%d")
    visit_date_obj = datetime.strptime(visit_date_str, "%Y-%m-%d").date()

    mock_routes = [MagicMock(id=uuid.uuid4())]
    mock_get.return_value = mock_routes

    result = VisitRouteService.get_by_seller_and_date(seller_id, visit_date_str)

    assert result == mock_routes
    mock_get.assert_called_once_with(seller_id, visit_date_obj)

@patch("app.repositories.visit_route_repository.VisitRouteRepository.create")
def test_create_route_success(mock_create):
    route_data = {
        "route_name": "Ruta Visita 1",
        "visit_date": datetime.now().strftime("%Y-%m-%d"),
        "origin_address": "Avenida Calle 100 #15-30, Bogotá, Colombia",
        "origin_lat": 4.676707,
        "origin_lng": -74.048489,
        "destination_address": "Calle 100 #8a-55, Bogotá, Colombia",
        "destination_lat": 4.676123,
        "destination_lng": -74.048739,
        "estimated_time": "10 minutos",
        "seller_id": "a68e9bdd-f86a-45b1-a466-89034d8d42ad"
    }
    mock_route = MagicMock()
    mock_create.return_value = mock_route

    result = VisitRouteService.create(route_data)

    assert result == mock_route
    mock_create.assert_called_once()