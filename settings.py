from pathlib import Path
from decouple import config

from uimodules.pluralize import Pluralize

BASE_DIR = Path(__file__).resolve().parent

SETTINGS = dict(
    template_path=BASE_DIR / "templates",
    cookie_secret=config("COOKIE_SECRET"),
    xsrf_cookie=config("XSRF_COOKIE"),
    db=config("DB"),
    login_url="/auth/login/",
    ui_modules=dict(
        str_plural=Pluralize,
    )
) 

