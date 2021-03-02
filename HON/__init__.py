import os
from flask import Flask

# setup as application factory (recommended in flask tutorial)
def create_app(config=None,config_path="../config.py"):
    """
        creates instance of HON

        Args:
            config: dictionary to configure app 

        Returns:
            flask app object
    """
    app = Flask(__name__,instance_relative_config=True)
    
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    if config is None:
        # load the instance config, if it exists
        app.config.from_pyfile(config_path, silent=True)
    else:
        # load the config if passed in
        app.config.from_mapping(config)
    



    from . import DBmodel
    DBmodel.db.init_app(app)
    app.cli.add_command(DBmodel.init_db_command)
    app.cli.add_command(DBmodel.change_base_url_command)

    from . import auth
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
