import pytest
from flask import session
from app import create_app
from app.models.db import db
from app.models.Usuario import Usuario

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SECRET_KEY": "testkey",
        "WTF_CSRF_ENABLED": False,
    })

    with app.app_context():
        db.create_all()
        # Crear un usuario de prueba
        usuario = Usuario(nombre="Test", preferencias="aventura", correo="test@demo.com")
        db.session.add(usuario)
        db.session.commit()
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

def test_recomendaciones_basicas_no_auth(client):
    response = client.post('/recomendaciones_basicas', data={
        'fecha_inicial': '2024-01-01',
        'fecha_final': '2024-12-31'
    })
    assert b"Usuario no autenticado" in response.data

def test_reportes_status(client):
    response = client.get('/reportes')
    assert response.status_code == 200