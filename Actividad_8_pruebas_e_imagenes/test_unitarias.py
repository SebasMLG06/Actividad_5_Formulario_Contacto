"""
PRUEBAS UNITARIAS
Prueban una sola pieza aislada: la expresión regular que valida el correo.
No usan servidor, ni base de datos, ni navegador.
"""
from app import EMAIL_REGEX


def test_U01_correo_valido_es_aceptado():
    assert EMAIL_REGEX.match("estudiante@lasalle.edu.co") is not None


def test_U02_correo_sin_arroba_es_rechazado():
    assert EMAIL_REGEX.match("estudiante.lasalle.edu.co") is None
