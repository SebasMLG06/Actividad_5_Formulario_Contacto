import os
import sys

# Permite importar app.py y config.py desde la carpeta tests/
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from app import create_app


@pytest.fixture
def app():
    """Aplicación en ambiente de pruebas (usa data/pruebas.db)."""
    app = create_app("testing")
    app.testing = True
    return app


@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client
