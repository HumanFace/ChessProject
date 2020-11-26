from chessUI import UI
from Board import Board

board_state = [('rB', (0, 0)), ('kB', (1, 0))]

UI = UI()
PlayingBoard = Board()

UI.init_board(PlayingBoard.getCoords())
while UI.get_state():
    UI.user_input()
    if UI.get_ready_state():
        coords = UI.get_selected_coords()
        print(coords)
    UI.render(PlayingBoard.getCoords())
