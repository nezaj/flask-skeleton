from src.app import create_app
from src.settings import DevelopmentConfig, ProductionConfig, TestConfig

def test_dev_config():
    app = create_app(DevelopmentConfig)
    assert app.config['ENV'] == 'dev'
    assert app.config['DEBUG'] is True
    assert app.config['ASSETS_DEBUG'] is True

def test_production_config():
    app = create_app(ProductionConfig)
    assert app.config['ENV'] == 'prod'
    assert app.config['DEBUG'] is False
    assert app.config['ASSETS_DEBUG'] is False

def test_test_config():
    app = create_app(TestConfig)
    assert app.config['ENV'] == 'test'
    assert app.config['TESTING'] is True
