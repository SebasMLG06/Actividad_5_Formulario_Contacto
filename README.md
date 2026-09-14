## 1. Requisitos

- Python 3.14 o superior.
- pip.

## 2. Instalación (una sola vez)

```bash
# 1. Clonar o descomprimir el proyecto y entrar a la carpeta
cd formulario_contacto_lasalle

# 2. Crear entorno virtual
python -m venv venv

# 3. Activar entorno virtual
source venv/bin/activate        # Linux / Mac
venv\Scripts\activate           # Windows

# 4. Instalar dependencias
pip install -r requisitos.txt

# 5. Copiar el archivo de ejemplo de variables de entorno
cp .env.example .env            # Linux / Mac
copy .env.example .env          # Windows
```

Editar `.env` y colocar una `SECRET_KEY` propia. 

## 3. Ambiente de Desarrollo

Características: `DEBUG=True`, mensajes de depuración en consola, base de
datos propia (`data/desarrollo.db`) con las filas marcadas con
`entorno = "DESARROLLO"`.

```bash
export APP_ENV=development      # Linux / Mac
set APP_ENV=development         # Windows

python app.py
```

Abrir en el navegador: `http://localhost:5000`

## 4. Ambiente de Pruebas

Características: configuración `testing`, base de datos separada
(`data/pruebas.db`), pensada para ejecutar pruebas automatizadas sin tocar
los datos de desarrollo.

### 4.1 Ejecutar la app en modo pruebas manualmente (opcional)

```bash
export APP_ENV=testing
python app.py
```

### 4.2 Ejecutar los 3 casos de prueba exigidos (automatizado)

```bash
python -m pytest tests/test_casos.py -v -s
```

Esto ejecuta y muestra en pantalla:

1. **Caso 1** — envío correcto del formulario → código `200`, mensaje de
   confirmación.
2. **Caso 2** — intento de envío con un campo obligatorio vacío → código
   `400`, mensaje de error "obligatorio".
3. **Caso 3** — intento de envío con correo inválido → código `400`,
   mensaje de error de formato.

## 5. Ambiente de Producción / Demostración

Características: `DEBUG=False`, sin mensajes de depuración, base de datos
propia (`data/produccion.db`).

### 5.1 Prueba local del modo producción (antes de desplegar)

```bash
export APP_ENV=production
gunicorn app:app          # Linux / Mac
# En Windows, Flask puro sirve igual: python app.py (con APP_ENV=production)
```

## 6. Estructura del proyecto

```
formulario_contacto_lasalle/
├── app.py                # Lógica de la aplicación (rutas, validación, DB)
├── config.py              # Configuración por ambiente (dev/test/prod)
├── requirements.txt
├── .env.example            # Variables de entorno de ejemplo (sin secretos)
├── .gitignore
├── templates/
│   └── index.html          # Formulario
├── static/
│   └── style.css
├── tests/
│   └── test_casos.py       # Los 3 casos de prueba exigidos
└── data/                   # Bases de datos SQLite (una por ambiente, no se sube)
```

