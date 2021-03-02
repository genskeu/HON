import pytest


def test_init_db_command(app,runner, monkeypatch):
    class Recorder:
        called = False

    def fake_init_db():
        Recorder.called = True
    # create the database 
    monkeypatch.setattr("TAFC.DBmodel.init_db", fake_init_db)
    result = runner.invoke(args=["init-db"])
    # assert "Initialized" in result.output
    assert Recorder.called





