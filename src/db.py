from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import config

db = SQLAlchemy()


def init_db(app: Flask):
    app.config[
        'SQLALCHEMY_DATABASE_URI'] = (f'postgresql://{config.postgres_user}:{config.postgres_password}@'
                                      f'{config.postgres_host}/{config.postgres_db}')
    db.init_app(app)
