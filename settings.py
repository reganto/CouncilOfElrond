import os

root = os.path.dirname(os.path.abspath(__file__))


def add_path(*args):
    return os.path.join(root, *args)


class BaseSettings:
    pass


class DevelopmentSettings(BaseSettings):
    development = True
    debug = True
    template_path = add_path('templates')
    cookie_secret = os.urandom(16)
    xsrf_cookie = True
    db = 'database.db'
    login_url = '/auth/login/'


class TestingSettings(BaseSettings):
    testing = True
    db = ':memory:'
    debug = True
    template_path = add_path('templates')
    cookie_secret = os.urandom(16)
    xsrf_cookie = True


class ProductionSettings(BaseSettings):
    production = True


settings = {
    'development': DevelopmentSettings,
    'testing': TestingSettings,
    'production': ProductionSettings,
}
