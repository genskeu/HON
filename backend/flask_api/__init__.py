import os
from flask import Flask
from flask_cors import CORS

# setup as application factory (recommended in flask tutorial)
def create_app(config=None):
    """
        creates instance of HON

        Args:
            config: dictionary to configure app 

        Returns:
            flask app object
    """
    app = Flask(__name__,instance_relative_config=True)
    
    # enable cors requests
    CORS(app, resources={r"/*": {"origins": "*"}})
    
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    if config is None:
        if app.config["ENV"] == "production":
            app.config.from_object("config.ProductionConfig")
        elif app.config["ENV"] == "development":
            app.config.from_object("config.DevelopmentConfig")
        elif app.config["ENV"] == "testing":
            app.config.from_object("config.TestingConfig")
        elif app.config["ENV"] == "docker":
            app.config.from_object("config.DockerConfig")
    else:
        # load the config if passed in
        app.config.from_mapping(config)
    
    from . import DBmodel
    DBmodel.db.init_app(app)
    app.cli.add_command(DBmodel.init_db_command)
    app.cli.add_command(DBmodel.init_imgdir_command)
    app.cli.add_command(DBmodel.init_all_command)
    app.cli.add_command(DBmodel.add_default_users_command)

    from . import auth
    auth.jwt.init_app(app)
    app.register_blueprint(auth.bp)

    from . import studies
    app.register_blueprint(studies.bp)

    from . import results
    app.register_blueprint(results.bp)

    from . import file_handeling
    app.register_blueprint(file_handeling.bp)

    from . import users
    app.register_blueprint(users.bp)

    from . import misc
    app.register_blueprint(misc.bp)

    return app
