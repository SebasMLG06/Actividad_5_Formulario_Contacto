import os
import re
import sqlite3
import logging
from datetime import datetime

from flask import Flask, render_template, request, flash, redirect, url_for

from config import config_by_name

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def create_app(env_name=None):
    """Application factory: crea la app configurada según el ambiente."""
    env_name = env_name or os.environ.get("APP_ENV", "development")
    app = Flask(__name__)
    app.config.from_object(config_by_name[env_name])
    app.config["ENV_NAME"] = env_name

    os.makedirs(os.path.dirname(app.config["DATABASE"]), exist_ok=True)

    logging.basicConfig(
        level=app.config["LOG_LEVEL"],
        format="%(asctime)s [%(levelname)s] %(message)s",
    )
    app.logger.setLevel(app.config["LOG_LEVEL"])
    app.logger.debug(f"Aplicación iniciada en ambiente: {app.config['ENTORNO']}")

    init_db(app.config["DATABASE"])

    @app.route("/", methods=["GET"])
    def index():
        return render_template("index.html", entorno=app.config["ENTORNO"])

    @app.route("/contacto", methods=["POST"])
    def contacto():
        nombre = request.form.get("nombre", "").strip()
        correo = request.form.get("correo", "").strip()
        asunto = request.form.get("asunto", "").strip()
        mensaje = request.form.get("mensaje", "").strip()

        errores = []
        if not nombre:
            errores.append("El nombre es obligatorio.")
        if not correo:
            errores.append("El correo es obligatorio.")
        elif not EMAIL_REGEX.match(correo):
            errores.append("El formato del correo electrónico no es válido.")
        if not asunto:
            errores.append("El asunto es obligatorio.")
        if not mensaje:
            errores.append("El mensaje es obligatorio.")

        if errores:
            app.logger.debug(f"Validación fallida: {errores} | datos recibidos={dict(request.form)}")
            for e in errores:
                flash(e, "error")
            return render_template(
                "index.html",
                entorno=app.config["ENTORNO"],
                nombre=nombre, correo=correo, asunto=asunto, mensaje=mensaje,
            ), 400

        guardar_contacto(app.config["DATABASE"], nombre, correo, asunto, mensaje, app.config["ENTORNO"])
        app.logger.debug(f"Contacto guardado correctamente: nombre={nombre}, correo={correo}")
        flash("¡Formulario enviado correctamente! Gracias por contactarnos.", "success")
        return redirect(url_for("index"))

    @app.route("/salud")
    def salud():
        """Endpoint simple para verificar que la app está viva (útil en despliegue)."""
        return {"estado": "ok", "entorno": app.config["ENTORNO"]}

    return app


def init_db(db_path):
    conn = sqlite3.connect(db_path)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS contactos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            correo TEXT NOT NULL,
            asunto TEXT NOT NULL,
            mensaje TEXT NOT NULL,
            entorno TEXT NOT NULL,
            fecha TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


def guardar_contacto(db_path, nombre, correo, asunto, mensaje, entorno):
    conn = sqlite3.connect(db_path)
    conn.execute(
        "INSERT INTO contactos (nombre, correo, asunto, mensaje, entorno, fecha) VALUES (?, ?, ?, ?, ?, ?)",
        (nombre, correo, asunto, mensaje, entorno, datetime.now().isoformat()),
    )
    conn.commit()
    conn.close()


# Instancia usada por 'flask run', gunicorn, etc. Usa APP_ENV del sistema.
app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=app.config["DEBUG"])
