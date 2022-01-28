#example of sqlite DB URI 'sqlite://////home/HON/instance/dev.db'
#example of mysql DB URI 'mysql://user:password@db_host_adress/db_name

class Config(object):
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    SECRET_KEY = "dev-key"
    IMAGE_PATH = "/home/HON/instance/images_dev"
    SQLALCHEMY_DATABASE_URI = "sqlite://////home/HON/instance/dev.db"
    DEBUG = True

class ProductionConfig(Config):
    SECRET_KEY = "prod-key"
    IMAGE_PATH = "/home/HON/instance/images_prod"
    SQLALCHEMY_DATABASE_URI = "sqlite://////home/HON/instance/prod.db"
    DEBUG = False

class TestingConfig(Config):
    IMAGE_PATH = "/home/HON/instance/images_test"
    SQLALCHEMY_DATABASE_URI = "sqlite://////home/HON/instance/test.db"
    TESTING = True

