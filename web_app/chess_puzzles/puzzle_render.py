import chess


def detect_pieces_in_game(fen):
    """
    Receives the position in fen;
    Returns a list of pieces in game and their positions
    (which is used to generate html)
    """

    pieces = {
        "P": "wp", "N": "wn", "B": "wb", "Q": "wq", "K": "wk", "R": "wr",
        "p": "bp", "n": "bn", "b": "bb", "q": "bq", "k": "bk", "r": "br"
    }

    pieces_in_game = []
    file = 1    # vertical line in chess
    rank = 8    # horisontal line in chess

    for sym in fen:
        if sym == '/':
            rank -= 1
            file = 1
        elif sym in 'pnbqkrPNBQKR':
            pieces_in_game.append([pieces[sym], str(file) + str(rank)])
            file += 1
        elif sym in '12345678':
            file += int(sym)
            # note: there is always a "/" after the "8" so we don't care about the file=9
        elif sym == " ":
            break

    return pieces_in_game


def change_move_notation(move):
    """ Change letter-number notation to numbers notation ('a8b7' -> '1827') """

    row = 'abcdefgh'
    move_out = ''

    try:
        move_out += str(row.index(move[0]) + 1)
        move_out += move[1]
        move_out += str(row.index(move[2]) + 1)
        move_out += move[3]
    except:
        print(f'Error: move notation is wrong: {move}')

    return int(move_out)


def get_legal_moves(fen):
    """ generates a list of legal moves for the current position in fen """

    board = chess.Board(fen)
    legal_moves = [str(move) for move in board.legal_moves]
    legal_moves_out = []

    for move in legal_moves:
        move_out = change_move_notation(move)
        legal_moves_out.append(move_out)

    return legal_moves_out


def capital(string:str):
    """ changes the first symbol to a capital letter and keeps the rest of the string """
    return string[0].upper() + string[1:]



