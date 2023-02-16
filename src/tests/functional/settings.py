from config import Config
import os


class TestSettings(Config):
    service_url: str = os.getenv("SERVICE_URL", 'http://0.0.0.0:5000')


test_settings = TestSettings()
