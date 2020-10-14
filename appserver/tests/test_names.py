from starlette.testclient import TestClient

from app.main import app

def test_facu(test_app):
    response = test_app.get("/facu")
    assert response.status_code == 200
    assert response.json() == {"message":"hola soy facu"}

def test_nico(test_app):
    response = test_app.get("/nico")
    assert response.status_code == 200
    assert response.json() == {"message":"hola soy nico"}