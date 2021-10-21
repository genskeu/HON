class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = "dev"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    pass

class TestingConfig(Config):
    pass

class DockerConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite://////HON_full/HON_SQLite.db'
    IMAGE_PATH = "/HON_full/instance/images"
    SESSION_COOKIE_SECURE = False
