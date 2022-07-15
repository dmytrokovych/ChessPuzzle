from flask import Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
from .background_tasks import update_db
from .db import select_puzzles_from_db, update_puzzle_status_in_db, get_random_puzzle
from .chess_puzzles.chessdotcom_data import get_user_data


bp = Blueprint('views', __name__)


@bp.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        username = request.form['username']
        update_db.delay(username, number_of_games=1)
        return redirect(url_for('views.profile', username=username))
    
    return render_template('home.html')


@bp.route('/<username>', methods=['POST', 'GET'])
def profile(username):
    if request.method == 'POST':
        number_of_games = int(request.form['games_number'])
        update_db.delay(username, number_of_games)
        return redirect(url_for('views.puzzle', username=username))
    
    games = get_user_data(username, number_of_games=10)
    return render_template('profile.html', username=username, games=games)


@bp.route('/<username>/puzzle', methods=['POST', 'GET'])
def puzzle(username):
    if request.method == 'POST':
        fen = request.form['fen']
        update_puzzle_status_in_db(fen, username)

    data = get_random_puzzle(username)
    if bool(len(data)):
        return render_template('puzzle.html', data=data)
    
    return redirect(url_for('views.no_data_message', username=username))


@bp.route('/<username>/no_data', methods=['POST', 'GET'])
def no_data_message(username):
    if request.method == "POST":
        return redirect(url_for('views.profile', username=username))

    return render_template('no_data_message.html')
