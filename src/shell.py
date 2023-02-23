import click
from flask import Blueprint
from werkzeug.security import generate_password_hash

from models.user import User, db

shell = Blueprint('shell', __name__, cli_group=None)


@shell.cli.command('user', help='Создание/обновление пользователя.')
@click.argument('email')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='Пароль для пользователя.')
@click.option('--admin', is_flag=True, help='Сделать пользователя администратором.')
def create(email, password, admin):
    user = User.find_by_email(email)

    if not user:
        user = User(email=email)
        db.session.add(user)

    user.password = generate_password_hash(password)
    user.is_admin = admin

    db.session.commit()
    click.secho(f'Пользователь <{email}> создан/обновлен')
