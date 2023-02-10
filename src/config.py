from pydantic import BaseSettings


class Config(BaseSettings):
    postgres_password: str = '123qwe'
    postgres_user: str = 'app'
    postgres_db: str = 'auth_database'
    postgres_host: str = 'localhost'
    postgres_port: int = 5432

    redis_host: str = 'localhost'
    redis_port: int = 6379

    class Config:
        env_nested_delimiter = '__'


config = Config()
