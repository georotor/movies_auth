import click
from flask import Blueprint
from werkzeug.security import generate_password_hash

from models.user import User, db
from utils.sql import USER_HISTORY_PARTITION_SQL
from sqlalchemy.sql import text

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


@shell.cli.command(
    'init_db',
    help='Создание секций (partitions) для таблицы UserHistory '
         'на 5 лет вперед начиная с указанного года.'
)
@click.argument('year')
def create_partitions(year):
    for current_year in range(int(year), int(year)+6):
        db.session.execute(text(
            USER_HISTORY_PARTITION_SQL.format(
                current_year, current_year, current_year+1
            ))
        )
        click.secho('Создана таблица для {} года'.format(current_year))
    db.session.commit()