import pygame as p


class UI():

    def __init__(self):
        self.__WIDTH = self.__HEIGHT = 512
        self.__DIMENSION = 8
        self.__SQ_SIZE = self.__HEIGHT // self.__DIMENSION
        self.__IMAGES = {}
        self.__screen = p.display.set_mode((self.__WIDTH, self.__HEIGHT))
        self.__selected_piece = ()
        self.__move_to = ()
        self.__possible_moves = []
        self.__running = True
        self.__from_coords_ready = False
        self.__to_coords_ready = False

    #################
    ### RENDERING ###
    #################

    def __load_images(self):
        """
        Loads images into memory.
        """
        pieces = ['bB', 'bW', 'kB', 'kW', 'nB', 'nW',
                  'pB', 'pW', 'qB', 'qW', 'rB', 'rW', ]
        for piece in pieces:
            self.__IMAGES[piece] = p.transform.scale(
                p.image.load("images/" + piece + '.png'), (self.__SQ_SIZE, self.__SQ_SIZE))

    def __render_board(self):
        """
        Handles rendering of chess board.
        """
        for row in range(self.__DIMENSION):
            for col in range(self.__DIMENSION):
                if (row + col) % 2 != 0:
                    p.draw.rect(self.__screen, p.Color('grey'), p.Rect(
                        col*self.__SQ_SIZE, row*self.__SQ_SIZE, self.__SQ_SIZE, self.__SQ_SIZE))
                else:
                    p.draw.rect(self.__screen, p.Color('white'), p.Rect(
                        col*self.__SQ_SIZE, row*self.__SQ_SIZE, self.__SQ_SIZE, self.__SQ_SIZE))

    def __render_pieces(self, pieces):
        """
        Handles rendering of pieces.
        """
        for piece in pieces:
            self.__screen.blit(self.__IMAGES[piece[0]], p.Rect(
                piece[1][0]*self.__SQ_SIZE, piece[1][1]*self.__SQ_SIZE, self.__SQ_SIZE, self.__SQ_SIZE))

    def __render_selected(self):
        """
        Handles rendering of selection and possible moves highlight.
        """
        if self.__selected_piece != ():
            p.draw.rect(self.__screen, p.Color(99, 245, 66), p.Rect(
                self.__selected_piece[0]*self.__SQ_SIZE, self.__selected_piece[1]*self.__SQ_SIZE, self.__SQ_SIZE, self.__SQ_SIZE))

        if self.__possible_moves != []:
            for move in self.__possible_moves:
                p.draw.rect(self.__screen, p.Color(99, 50, 66), p.Rect(
                    move[0]*self.__SQ_SIZE, move[1]*self.__SQ_SIZE, self.__SQ_SIZE, self.__SQ_SIZE))

    def render(self, board_state):
        """
        Renders the actual state of board.

        Parameters
        ----------
        board_state : list
            Boardsate (list of all pieces)
        """
        self.__render_board()
        self.__render_selected()
        self.__render_pieces(board_state)
        p.display.flip()

    def init_board(self, board_state):
        """
        Sets up the game window, loads images and renders the initial state of board.

        Parameters
        ----------
        board_state : list
            Boardsate (list of all pieces)
        """
        p.init()
        self.__load_images()
        p.display.set_caption('CHESS')
        self.render(board_state)

    ####################
    ### HANDLE INPUT ###
    ####################

    def __mouse_selection(self):
        """
        Handles user selection of piece and position to move to. User can deselect the piece by clicking on it again.
        """
        mouse_position = p.mouse.get_pos()
        calc_sq_coords = (
            mouse_position[0] // self.__SQ_SIZE, mouse_position[1] // self.__SQ_SIZE)
        if self.__selected_piece == ():
            self.__selected_piece = calc_sq_coords
            self.__from_coords_ready = True
        elif self.__selected_piece == calc_sq_coords:
            self.clear_selection()
        else:
            self.__move_to = calc_sq_coords
            self.__to_coords_ready = True
    def __quit(self):
        """
        Sets running to off state.
        """
        self.__running = False

    def user_input(self):
        """
        Handles user inputs.
        """
        for e in p.event.get():
            if e.type == p.QUIT:
                self.__quit()
            elif e.type == p.MOUSEBUTTONDOWN:
                self.__mouse_selection()

    ###########################
    ### SETTERS AND GETTERS ###
    ###########################

    def get_selected_coords(self):
        """
        Returns list of two tuples. First are coords of selected piece. Second are coords to move to.
        """
        selected, to = self.__selected_piece, self.__move_to
        self.clear_selection()
        return [selected, to]
    
    def get_ready_state(self):
        if self.__from_coords_ready and self.__to_coords_ready:
            return True
        else:
            return False

    def set_possible_moves(self, moves):
        """
        Takes a list of possible moves.

        Parameters
        ----------
        moves : list
            List of coords (tuples) of possible moves.
        """
        self.__possible_moves = moves

    def clear_selection(self):
        """
        Clears piece selection, possible moves and move to.
        """
        self.__selected_piece = ()
        self.__possible_moves = []
        self.__move_to = ()
        self.__from_coords_ready, self.__to_coords_ready = False, False

    def get_state(self):
        """
        Returns running state.
        """
        return self.__running
