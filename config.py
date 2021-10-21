class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = "dev"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///////home/uli/Insync/uligenske@gmail.com/Google Drive/Projekte_Uli/HON/Code/instance/dev_SQLite.db'
    IMAGE_PATH = "/home/uli/Insync/uligenske@gmail.com/Google Drive/Projekte_Uli/HON/Code/instance/dev_images"

class TestingConfig(Config):
    pass

class DockerConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite://////HON_full/HON_SQLite.db'
    IMAGE_PATH = "/HON_full/instance/images"
    SESSION_COOKIE_SECURE = False
