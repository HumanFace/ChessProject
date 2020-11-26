from chessUI import UI
from Board import Board
import time

# initiate variables
UI = UI()
PlayingBoard = Board()
inGame = True

UI.init_board(PlayingBoard.getCoords())
while UI.get_state() and inGame:
    UI.user_input()

    # await selected source coord
    if UI.get_ready_state()[0]:
        coords = UI.get_selected_coords()[0]
        possibleMoves = PlayingBoard.getPossibleMoves(coords)
        UI.set_possible_moves(possibleMoves)

    # await selected target coord
    if UI.get_ready_state()[1]:
        PlayingBoard.move(*UI.get_selected_coords())
        UI.clear_selection()

    # check if a winner exists
    if PlayingBoard.getWinner():
        print(f"{PlayingBoard.getWinner().upper()} WON THE GAME")
        inGame = False
    
    UI.render(PlayingBoard.getCoords())
    # sleep for 1/60 of a second to prevent unnecesary CPU overload
    time.sleep(1/60)
