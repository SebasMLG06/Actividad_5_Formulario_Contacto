import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class BaseConfig:
    """Configuración común a todos los ambientes."""
    SECRET_KEY = os.environ.get("SECRET_KEY", "clave-no-secreta-cambiar")
    DEBUG = False
    TESTING = False
    LOG_LEVEL = "WARNING"
    ENTORNO = "BASE"


class DevelopmentConfig(BaseConfig):
    """Ambiente de desarrollo: mensajes de depuración activos, datos identificables."""
    DEBUG = True
    TESTING = False
    DATABASE = os.path.join(BASE_DIR, "data", "desarrollo.db")
    LOG_LEVEL = "DEBUG"
    ENTORNO = "DESARROLLO"


class TestingConfig(BaseConfig):
    """Ambiente de pruebas: separado de desarrollo, con su propia base de datos."""
    DEBUG = True
    TESTING = True
    DATABASE = os.path.join(BASE_DIR, "data", "pruebas.db")
    LOG_LEVEL = "DEBUG"
    ENTORNO = "PRUEBAS"


class ProductionConfig(BaseConfig):
    """Ambiente de producción/demostración: sin mensajes de depuración."""
    DEBUG = False
    TESTING = False
    DATABASE = os.path.join(BASE_DIR, "data", "produccion.db")
    LOG_LEVEL = "ERROR"
    ENTORNO = "PRODUCCION"


config_by_name = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}
