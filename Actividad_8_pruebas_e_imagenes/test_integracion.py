"""
PRUEBAS DE INTEGRACIÓN
Prueban que la ruta /contacto y la base de datos SQLite trabajan juntas.
Se cuenta cuántas filas hay ANTES y DESPUÉS de enviar el formulario.
"""
import sqlite3


def contar_registros(ruta_db):
    conn = sqlite3.connect(ruta_db)
    total = conn.execute("SELECT COUNT(*) FROM contactos").fetchone()[0]
    conn.close()
    return total


def test_I01_envio_correcto_guarda_un_registro(app, client):
    db = app.config["DATABASE"]
    antes = contar_registros(db)

    client.post("/contacto", data={
        "nombre": "Prueba Integracion",
        "correo": "integracion@lasalle.edu.co",
        "asunto": "Caso I-01",
        "mensaje": "Debe guardarse en la base de datos.",
    })

    despues = contar_registros(db)
    assert despues == antes + 1


def test_I02_envio_invalido_no_guarda_registro(app, client):
    db = app.config["DATABASE"]
    antes = contar_registros(db)

    client.post("/contacto", data={
        "nombre": "Prueba Integracion",
        "correo": "correo-invalido",
        "asunto": "Caso I-02",
        "mensaje": "No debe guardarse.",
    })

    despues = contar_registros(db)
    assert despues == antes
