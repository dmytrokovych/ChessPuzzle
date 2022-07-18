from chessdotcom import get_player_game_archives
import requests
from datetime import datetime


def get_games_urls(username):
    '''Returns a list of URLs to the monthly archives for player {username}'''
    
    try:
        data = get_player_game_archives(username).json
        data = data['archives']
    except:
        print(f'User {username} not found.')
        data = []

    return data


def get_games(username, number_of_games=10):
    ''' Returns the last {number_of_games} games of {username}'''

    games = []
    urls = get_games_urls(username)

    if not urls:
        return []

    try:
        for url in urls[::-1]:
            if len(games) < number_of_games:
                res = requests.get(url).json()
                chess_games = [game for game in res['games'][::-1] if game['rules'] == 'chess']
                games.extend(chess_games)
                
        print(f'{number_of_games} games have been successfully loaded.')
    except:
        print(f'Failed to load {username} games.')
        return []

    return games[:number_of_games]


def get_game_result(game):
    '''Returns {game} result in the form "(white score)-(black score)" '''

    if game['white']['result'] == 'win':
        result = '1-0'
    elif game['white']['result'] == 'win':
        result = '0-1'
    else:
        result = '0.5-0.5'

    return result


def get_user_data(username, number_of_games=10):
    """ 
    Returns a list of dictionaries with {username} data for each game;
    dict_keys(['white', 'black', 'result', 'date', 'pgn'])
    """

    data = []
    games = get_games(username, number_of_games)

    for game in games:
        game_data = {}
        
        game_data["white"] = game['white']['username'] 
        game_data["black"] = game['black']['username']
        game_data["result"] = get_game_result(game)
        game_data["date"]  = datetime.fromtimestamp(game['end_time']).strftime("%m/%d/%Y, %H:%M:%S")
        game_data["pgn"] = game['pgn']

        data.append(game_data)

    return data