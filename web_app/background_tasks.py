import os
from celery import Celery

from .db import get_db, create_games_table, create_puzzles_table, insert_games


celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", 'redis://127.0.0.1:6379')
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", 'redis://127.0.0.1:6379')


@celery.task()
def update_db(username, number_of_games=1):
    db = get_db()

    create_games_table(db, username)
    create_puzzles_table(db, username)
    insert_games(db, username, number_of_games)

    db.close()