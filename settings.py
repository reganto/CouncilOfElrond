from pathlib import Path
import secrets

from uimodules.pluralize import Pluralize


BASE_DIR = Path(__file__).resolve().parent


class BaseSettings:
    pass


class DevelopmentSettings(BaseSettings):
    development = True
    debug = True
    template_path = BASE_DIR / "templates"
    cookie_secret = secrets.token_hex()
    xsrf_cookie = True
    db = "database.db"
    login_url = "/auth/login/"
    ui_modules = {
        "str_plural": Pluralize,
    }


class TestingSettings(BaseSettings):
    testing = True
    db = ":memory:"
    debug = True
    template_path = BASE_DIR / "templates"
    cookie_secret = secrets.token_hex()
    xsrf_cookie = True


class ProductionSettings(BaseSettings):
    production = True


settings = {
    "development": DevelopmentSettings,
    "testing": TestingSettings,
    "production": ProductionSettings,
}
