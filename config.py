class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = "dev"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = "mysql://PhantomX:zxmdv21!@PhantomX.mysql.pythonanywhere-services.com/PhantomX$phantomX_04"
    SQLALCHEMY_POOL_RECYCLE = 299
    SQLALCHEMY_POOL_TIMEOUT = 20
    IMAGE_PATH = "/home/PhantomX/HON/instance/images"

class DevelopmentConfig(Config):
    pass

class TestingConfig(Config):
    pass

class DockerConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite://////HON_full/HON_SQLite.db'
    IMAGE_PATH = "/HON_full/instance/images"
    SESSION_COOKIE_SECURE = False
