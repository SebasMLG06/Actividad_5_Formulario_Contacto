"""
Pruebas del Ambiente de Pruebas (Testing).

Ejecuta los 3 casos exigidos por la actividad:
 1. Envío correcto del formulario.
 2. Intento de envío con un campo obligatorio vacío.
 3. Intento de envío con un correo electrónico inválido.

Cómo correrlo:
    APP_ENV=testing python -m pytest tests/test_casos.py -v -s

También imprime un resumen en texto plano, útil como evidencia para el informe.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from app import create_app


@pytest.fixture
def client():
    app = create_app("testing")
    app.testing = True
    with app.test_client() as client:
        yield client


def test_caso_1_envio_correcto(client):
    """Caso 1: envío correcto del formulario -> debe guardar y confirmar."""
    respuesta = client.post("/contacto", data={
        "nombre": "Estudiante Prueba",
        "correo": "prueba.testing@lasalle.edu.co",
        "asunto": "Caso de prueba 1",
        "mensaje": "Este es un envío correcto para el ambiente de pruebas.",
    }, follow_redirects=True)

    print("\n[CASO 1] Envío correcto -> código:", respuesta.status_code)
    assert respuesta.status_code == 200
    assert "enviado correctamente".encode("utf-8") in respuesta.data


def test_caso_2_campo_obligatorio_vacio(client):
    """Caso 2: campo obligatorio vacío (nombre) -> debe rechazar con error."""
    respuesta = client.post("/contacto", data={
        "nombre": "",
        "correo": "prueba.testing@lasalle.edu.co",
        "asunto": "Caso de prueba 2",
        "mensaje": "Falta el nombre.",
    })

    print("[CASO 2] Campo obligatorio vacío -> código:", respuesta.status_code)
    assert respuesta.status_code == 400
    assert "obligatorio".encode("utf-8") in respuesta.data


def test_caso_3_correo_invalido(client):
    """Caso 3: correo con formato inválido -> debe rechazar con error."""
    respuesta = client.post("/contacto", data={
        "nombre": "Estudiante Prueba",
        "correo": "esto-no-es-un-correo",
        "asunto": "Caso de prueba 3",
        "mensaje": "El correo no tiene formato válido.",
    })

    print("[CASO 3] Correo inválido -> código:", respuesta.status_code)
    assert respuesta.status_code == 400
    assert "válido".encode("utf-8") in respuesta.data
