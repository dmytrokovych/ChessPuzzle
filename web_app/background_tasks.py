import os
from celery import Celery

from .db import get_db, create_games_table, create_puzzles_table, insert_games


celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", 'redis://127.0.0.1:6379')
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", 'redis://127.0.0.1:6379')


@celery.task()
def update_db(username, number_of_games=1):
    create_games_table(username)
    create_puzzles_table(username)
    insert_games(username, number_of_games=number_of_games)
