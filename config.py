import os
def get_SQLALCHEMY_DATABASE_URI():
    db_type = os.environ.get('DB_TYPE', None)
    db_path = os.environ.get('DB_HOST', None)
    db_name = os.environ.get('DB_NAME', None)
    db_user = os.environ.get('DB_USER', None)
    db_password = os.environ.get('DB_PASSWORD', None)

    if db_type == "mysql":
        database_uri = 'mysql://%s:%s@'%(db_user,db_password) + os.path.join(db_path, db_name)
    elif db_type == "sqlite":
        database_uri = 'sqlite://////' + os.path.join(db_path, db_name)
    else:
        print("Database type unkown. Please check config.py.")

    return database_uri

database_uri = get_SQLALCHEMY_DATABASE_URI()

class Config(object):
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = database_uri

class ProductionConfig(Config):
    SECRET_KEY = "prod-key"
    IMAGE_PATH = "/home/HON/instance/images_prod"
    DEBUG = False

class DevelopmentConfig(Config):
    SECRET_KEY = "dev-key"
    IMAGE_PATH = "/home/HON/instance/images_dev"
    DEBUG = True

class TestingConfig(Config):
    IMAGE_PATH = "/home/HON/instance/images_test"
    TESTING = True

