import sqlite3

from .chess_puzzles.chessdotcom_data import get_user_data
from .chess_puzzles.puzzle_generator import make_puzzles
from .chess_puzzles.puzzle_render import capital, detect_pieces_in_game

from random import randint


def get_db():
    db = sqlite3.connect('database.db')
    db.row_factory = sqlite3.Row
    return db


def create_games_table(db, username):
    tablename = username + "_games"
    db.execute(f"""CREATE TABLE IF NOT EXISTS {tablename}(
        white TEXT NOT NULL,
        black TEXT NOT NULL,
        result TEXT NOT NULL,
        date TEXT PRIMARY KEY NOT NULL,
        pgn TEXT NOT NULL);"""
    )
    db.commit()


def create_puzzles_table(db, username):
    tablename = username + "_puzzles"
    db.execute(f"""CREATE TABLE IF NOT EXISTS {tablename}(
        fen TEXT PRIMARY KEY NOT NULL,
        answer TEXT NOT NULL,
        legal_moves TEXT NOT NULL,
        gamename TEXT NOT NULL,
        color TEXT NOT NULL,
        status TEXT NOT NULL);"""
    )
    db.commit()


def insert_puzzles(db, username, game):
    tablename = username + "_puzzles"

    color = ['black', 'white'][capital(username) in game["white"]]
    puzzles = make_puzzles(game["pgn"], color, depth=12, inaccuracy_level=1.0)

    for puzzle in puzzles:
        db.execute(f"""INSERT OR IGNORE INTO {tablename} VALUES 
            ("{puzzle['fen']}", 
            "{puzzle['answer']}", 
            "{puzzle['legal_moves']}", 
            "{game["white"] + " - " + game["black"] + "  ||  " + game["date"]}", 
            "{color}", 
            "unsolved");"""
        )


def insert_games(db, username, number_of_games=1):
    tablename = username + "_games"
    games = get_user_data(username, number_of_games=number_of_games)

    for game in games:
        res = db.execute(f"""INSERT OR IGNORE INTO {tablename} VALUES 
            ("{game["white"]}", 
            "{game["black"]}", 
            "{game['result']}", 
            "{game["date"]}", 
            '{game["pgn"]}');"""
        )
        if bool(res.lastrowid):
            insert_puzzles(db, username, game)
            db.commit()
            print('Game is saved to database')
        else:
            print('Game already in database')


def select_puzzles_from_db(username):
    db = get_db()

    tablename = username + "_puzzles"
    puzzle_data = db.execute(f"""
        SELECT fen, answer, legal_moves, gamename, color 
        FROM {tablename} 
        WHERE status="unsolved";"""
    ).fetchall()
    db.close()
    
    return puzzle_data


def update_puzzle_status_in_db(fen, username):
    db = get_db()

    tablename = username + "_puzzles"
    db.execute(f"""
        UPDATE {tablename} 
        SET status="solved" 
        WHERE fen="{fen}";"""
    )
    print('Puzzle status changed to "solved"')
    db.commit()
    db.close()


def get_random_puzzle(username):
    puzzles = select_puzzles_from_db(username)
    if bool(len(puzzles)):
        puzzle = puzzles[randint(0, len(puzzles)-1)]
        data = {
            'answer':       puzzle['answer'],
            'legal_moves':  puzzle['legal_moves'][1:-1].split(', '),
            'pieces':       detect_pieces_in_game(puzzle['fen']),
            'fen':          puzzle['fen'],
            'gamename':     puzzle['gamename'],
            'color':        puzzle['color']
        }
        return data
    
    return []