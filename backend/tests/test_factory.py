from backend import create_app

def test_config():
    """Test create_app without passing test config."""
    assert not create_app().testing
    assert not create_app().testing
    assert create_app(config={"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:","SQLALCHEMY_TRACK_MODIFICATIONS" : False}).testing
