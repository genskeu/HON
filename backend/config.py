#example of sqlite DB URI 'sqlite://////home/HON/instance/dev.db'
#example of mysql DB URI 'mysql://user:password@db_host_adress/db_name

class Config(object):
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ACCESS_TOKEN_EXPIRES = False
    
class DevelopmentConfig(Config):
    SECRET_KEY = "dev-key"
    JWT_SECRET_KEY = "dev-key"
    #IMAGE_PATH = "/home/HON/instance/images_dev"
    #SQLALCHEMY_DATABASE_URI = "sqlite://////home/HON/instance/dev.db"
    IMAGE_PATH = "/home/backend/instance/images_prod"
    SQLALCHEMY_DATABASE_URI = "mysql://genskeu:zxmdv21@host.docker.internal/phantomx"
    DEBUG = True

class ProductionConfig(Config):
    SECRET_KEY = "prod-key"
    IMAGE_PATH = "/home/backend/instance/images_test"
    SQLALCHEMY_DATABASE_URI = "sqlite://////home/backend/instance/dev.db"
    DEBUG = False

class TestingConfig(Config):
    SECRET_KEY = "test-key"
    IMAGE_PATH = "/home/backend/instance/images_test"
    SQLALCHEMY_DATABASE_URI = "sqlite://////home/HON/instance/test.db"
    TESTING = True

