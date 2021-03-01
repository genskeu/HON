from TAFC import create_app

def test_config():
    """Test create_app without passing test config."""
    assert not create_app().testing
    assert not create_app(config_path="config.py").testing
    assert create_app(config={"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:","SQLALCHEMY_TRACK_MODIFICATIONS" : False}).testing
    assert create_app(config_path="test_config.py").testing