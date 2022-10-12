import sys
from selenium.webdriver.common.by import By
from stockfish import Stockfish


WHITE = 0
BLACK = 1

# side to move
side_to_move = 0

# read argv if available
try:
    if sys.argv[1] == 'black': side_to_move = BLACK
except:
    print('usage: "chessbot.py white" or "chessbot.py black"')
    sys.exit(0)

# square to coords
square_to_coords = [];

# array to convert board square indices to coordinates (black)
get_square = [
    'a8', 'b8', 'c8', 'd8', 'e8', 'f8', 'g8', 'h8',
    'a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7',
    'a6', 'b6', 'c6', 'd6', 'e6', 'f6', 'g6', 'h6',
    'a5', 'b5', 'c5', 'd5', 'e5', 'f5', 'g5', 'h5',
    'a4', 'b4', 'c4', 'd4', 'e4', 'f4', 'g4', 'h4',
    'a3', 'b3', 'c3', 'd3', 'e3', 'f3', 'g3', 'h3',
    'a2', 'b2', 'c2', 'd2', 'e2', 'f2', 'g2', 'h2',
    'a1', 'b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1'
];
  
# map piece names to FEN chars
piece_names = {
    'black_king': 'k',
    'black_queen': 'q',
    'black_rook': 'r',
    'black_bishop': 'b',
    'black_knight': 'n',
    'black_pawn': 'p',
    'white_knight': 'N',
    'white_pawn': 'P',
    'white_king': 'K',
    'white_queen': 'Q',
    'white_rook': 'R',
    'white_bishop': 'B'
}



def driver_locate_piece(driver):
    piece_locations = {
        'black_king': [],
        'black_queen': [],
        'black_rook': [],
        'black_bishop': [],
        'black_knight': [],
        'black_pawn': [],
        'white_knight': [],
        'white_pawn': [],
        'white_king': [],
        'white_queen': [],
        'white_rook': [],
        'white_bishop': []
    }
    for index in range(1,33):
        try:
            piece = driver.find_element(By.XPATH, f'/html/body/div[1]/div/div[1]/div[3]/div/div[2]/div/div[2]/div/div[{index}]')
            #get piece name in format 'white_pawn'
            piece_name = '_'.join(piece.get_attribute('class').split(' ')[2:4][::-1])
            #get piece_coords in format [0,0]
            piece_coords = [int(i)//100 for i in piece.get_attribute('style')[34:-2].replace('%','',2).split(',')]
            piece_locations[piece_name].append(piece_coords)
            print('detecting:', piece_name, piece_coords)
        except:
            pass

    return piece_locations


def driver_locations_to_fen(piece_locations, side_to_move):
    fen = ''
    matrix = []
    key_value_change = {}
    for k, v in piece_locations.items():
        for coord in v:
            key_value_change[tuple(coord)] = k

    for row in range(8):
        a = []
        for col in range(8):
            try:
                a.append(piece_names[key_value_change[(row, col)]])
            except:
                a.append(0)
        matrix.append(a)

    trans_matrix = [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]

    for row in trans_matrix:
        empty = 0
        for col in row:
            if isinstance(col, str):
                if empty: fen += str(empty)
                fen += col
                empty = 0
            elif isinstance(col, int):
                empty += 1
        if empty: fen += str(empty)
        if trans_matrix.index(row) < 7: fen += '/'

    if side_to_move == 'b':
        fen = fen[::-1]
    fen += ' ' + side_to_move

    # add placeholders (NO EN PASSANT AND CASTLING are static placeholders)
    fen += ' KQkq - 0 1'

    return fen

# search position for a best move
def search(fen, side_to_move):
    if side_to_move=='b':
        side_to_move = 0
    # create chess board instance and set position from FEN string
    print('Searching best move for this position:')
    print(fen)
    # board = chess.Board(fen=fen)
    # print(board)
    stockfish = Stockfish(fr'stockfish_15.exe', depth=20, parameters={"Threads": 6, "Minimum Thinking Time": 1})

    #
    stockfish.set_fen_position(fen_position=fen)

    board = stockfish.get_board_visual(perspective_white=bool(side_to_move))
    print(board)
    try:
        best_move = stockfish.get_best_move()
    except:
        print('Error, board inverting...')
        stockfish = Stockfish(fr'stockfish_15.exe', depth=20, parameters={"Threads": 6, "Minimum Thinking Time": 1})
        new_fen = fen[::-1][13:] + fen[43:]
        stockfish.set_fen_position(fen_position=new_fen)
        print(board)
        print('Wit reload')
        best_move = stockfish.get_best_move()

    return best_move




def best_move(driver, side_to_move):

        # locate pieces
        piece_locations = driver_locate_piece(driver)

        # convert piece image coordinates to FEN string
        fen = driver_locations_to_fen(piece_locations,side_to_move)

        best_move = search(fen,side_to_move)
        print('Best move:', best_move)






