"""
PRUEBAS FUNCIONALES
Simulan lo que hace el usuario y verifican lo que ve en pantalla.
"""


def test_F01_envio_correcto_muestra_confirmacion(client):
    respuesta = client.post("/contacto", data={
        "nombre": "Prueba Funcional",
        "correo": "funcional@lasalle.edu.co",
        "asunto": "Caso F-01",
        "mensaje": "Debe aparecer la confirmación.",
    }, follow_redirects=True)

    assert respuesta.status_code == 200
    assert "enviado correctamente".encode("utf-8") in respuesta.data


def test_F02_campo_vacio_muestra_error(client):
    respuesta = client.post("/contacto", data={
        "nombre": "",
        "correo": "funcional@lasalle.edu.co",
        "asunto": "Caso F-02",
        "mensaje": "Falta el nombre.",
    })

    assert respuesta.status_code == 400
    assert "El nombre es obligatorio".encode("utf-8") in respuesta.data
