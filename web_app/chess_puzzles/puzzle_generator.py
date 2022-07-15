from .puzzle_render import *
import io
import chess
import chess.pgn
import chess.engine
import asyncio


async def analise(game, depth=18):
    ''' 
    The engine analyses the game and saves data after each move (for white and for black).
    Returns the following list of dictionaries:
        [ 
            *after whites move:* {"score": ..., "fen": ..., "best_move": ...},
            *after blacks move:* {"score": ..., "fen": ..., "best_move": ...},
            *after whites move:* {"score": ..., "fen": ..., "best_move": ...},
            ...
        ]
    '''
    
    transport, engine = await chess.engine.popen_uci(r"stockfish\stockfish_win\stockfish_14.1_win_x64_avx2.exe")
    # transport, engine = await chess.engine.popen_uci(r"stockfish\stockfish_linux\stockfish_15_x64")
    board = game.board()
    score_data = []

    for move in game.mainline_moves():
        move_data = {}

        board.push(move)
        info = await engine.analyse(board, chess.engine.Limit(depth=depth))

        # fen is a notation to describe positions of a chess game
        move_data["fen"] = board.fen()

        score = info["score"].pov(chess.WHITE).__str__()
        if score[0] == '#':
            score_val = 100
        else:
            score_val = int(score) / 100

        move_data["score"] = score_val
        try:
            move_data["best_move"] = info["pv"][0].uci()
            score_data.append(move_data)
        except:
            print("The engine cannot analyse this move")

    await engine.quit()
    return score_data


def make_puzzles(pgn, color, depth=18, inaccuracy_level=1.0):
    """ 
    Generates puzzles from {pgn} for {color};
    
    Parameters:
    pgn:    all game data in pgn format            
    color:  the colour of the player for whom the puzzle will be generated ('whites','blacks')
    depth:  depth of engine analysis
    inaccuracy_level:   score change used to detect user mistakes in the game
    
    Returns:
    list of dictionaries with dict_keys(['pieces', 'legal_moves', 'answer']) 
    """
    
    game = chess.pgn.read_game(io.StringIO(pgn))
    asyncio.set_event_loop_policy(chess.engine.EventLoopPolicy())
    score_data = asyncio.run(analise(game, depth))

    puzzles = []
    move_cash = {'fen': '', 'score': 0.0, 'best_move': ''}


    for move_num, move in enumerate(score_data):
        score = move['score']
        score_change =  score - move_cash['score']
        
        if color == 'white' and not move_num % 2:
            if score_change < -1 * inaccuracy_level:
                puzzles.append({'fen': move_cash['fen'],
                                'legal_moves': get_legal_moves(move_cash['fen']),
                                'answer': change_move_notation(move_cash['best_move'])
                })
        elif color == 'black' and move_num % 2:
            if score_change > inaccuracy_level:
                puzzles.append({'fen': move_cash['fen'],
                                'legal_moves': get_legal_moves(move_cash['fen']),
                                'answer': change_move_notation(move_cash['best_move'])
                })
        
        move_cash = move

    return puzzles

    