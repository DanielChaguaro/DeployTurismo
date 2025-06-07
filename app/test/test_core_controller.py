# tests/test_user_controller.py
import pytest
from flask import Flask
from app.controllers.user_controller import (
    es_email_valido,
    es_nombre_valido,
    es_contrasena_valida,
    es_email_unico,
    create_user
)
from app.models.db import db
from app.models.Usuario import Usuario

# Crear una app de Flask para testing
@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


def test_es_nombre_valido():
    assert es_nombre_valido('John Doe') == True
    assert es_nombre_valido('John123') == False

def test_es_contrasena_valida():
    assert es_contrasena_valida('password123') == True
    assert es_contrasena_valida('123') == False
