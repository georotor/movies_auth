from config import Config


class TestSettings(Config):
    service_url: str = 'http://0.0.0.0:5000'


test_settings = TestSettings()
