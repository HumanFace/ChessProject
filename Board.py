class Board:
    def __init__(self):
        # initializes the default board
        self.__coords = [["rook", False, (8, "a")],
        ["knight", False, (8, "b")],
        ["bishop", False, (8, "c")],
        ["queen", False, (8, "d")],
        ["king", False, (8, "e")],
        ["bishop", False, (8, "f")],
        ["knight", False, (8, "g")],
        ["rook", False, (8, "h")],
        
        ["pawn", False, (7, "a")],
        ["pawn", False, (7, "b")],
        ["pawn", False, (7, "c")],
        ["pawn", False, (7, "d")],
        ["pawn", False, (7, "e")],
        ["pawn", False, (7, "f")],
        ["pawn", False, (7, "g")],
        ["pawn", False, (7, "h")],

        ["pawn", True, (2, "a")],
        ["pawn", True, (2, "b")],
        ["pawn", True, (2, "c")],
        ["pawn", True, (2, "d")],
        ["pawn", True, (2, "e")],
        ["pawn", True, (2, "f")],
        ["pawn", True, (2, "g")],
        ["pawn", True, (2, "h")],

        ["rook", True, (1, "a")],
        ["knight", True, (1, "b")],
        ["bishop", True, (1, "c")],
        ["queen", True, (1, "d")],
        ["king", True, (1, "e")],
        ["bishop", True, (1, "f")],
        ["knight", True, (1, "g")],
        ["rook", True, (1, "h")],
        ]


        self.__whiteIsCurrent = True
    
    def getCoords(self):
        returnList = []
        for i in self.__coords:
            if i[1]:
                color = "W"
            else:
                color = "B"

            if i[0] == "knight":
                firstLetter = "n"
            else:
                firstLetter = i[0][0]
            
            returnList.append((firstLetter + color, (i[2][0] - 1, ord(i[2][1]) - 97)))
        return returnList
    
    def getCurrentPlayer(self):
        return self.__boolToColor(self.__whiteIsCurrent)
    
    def move(self, fromCoords, toCoords):
        movingFigure = self.getFigureByCoords(fromCoords)

        targetFigure = self.getFigureByCoords(toCoords)
        targetFigureColor = targetFigure[1]

        #TODO: finish this bolck
        toCoordValid = False
        validMoves = __getValidMoves(*movingFigure)


        if not movingFigure[0]:
            print("This source coord is empty!")
            return
        
        elif toCoords not in __getValidMoves(*movingFigure):
            print("This does not seem to be a valid move")
            return
        
        elif targetFigureColor != None:
            if targetFigureColor == self.__whiteIsCurrent:
                print("The target position seems to be taken by a figure of the same color")
                return
            
            else:
                self.__coords.remove(targetFigure)
                self.__coords.remove(movingFigure)
                self.__coords.append([movingFigure[0], movingFigure[1], toCoords])
                print(f"There was one removed figure: {targetFigure[0]} of {self.__boolToColor(targetFigureColor)}")
        else:
            self.__coords.remove(movingFigure)
            self.__coords.append([movingFigure[0], movingFigure[1], toCoords])

        print("The figure was moved")
        self.__whiteIsCurrent = not self.__whiteIsCurrent
    
    def getFigureByCoords(self, coords):
        for i in self.__coords:
            if i[2] == coords:
                return i
        return (None, None, None)

    def __getValidMoves(self, figureType, isWhite, position):
        moves = []
        if figureType == "pawn":
            if isWhite:
                moves = [[(position[0] + 1, position[1]), (position[0] + 2, position[1])]]

            else:
                moves = [[(position[0] - 1, position[1]), (position[0] - 2, position[1])]]

        # TODO: fix rook and queen
        elif figureType == "rook":
            for i in ((0,1),(1,0),(1,1)):
                directionList = []
                for j in range(7):
                    x = position[0] + i[0]*(j + 1)*(-1)**i[1]
                    y = chr(ord(position[1]) + i[1]*(j + 1)*(-1)**i[0])
                    if not (0 < x < 9) or not (96 < ord(y) < 105):
                        break  
                    directionList.append((x, y))
                moves.append(directionList)
        
        elif figureType == "knight":
            for i in ((0,0),(0,1),(1,0),(1,1)):
                for j in (1, 2):
                    moves.append([(position[0] + (-1)**i[0]*j, chr(ord(position[1]) + (-1)**i[1]*(3 - j)))])

        elif figureType == "bishop":
            for i in ((0,0),(0,1),(1,0),(1,1)):
                directionList = []
                for j in range(7):
                    x = position[0] + (-1)**i[0]*(j + 1)
                    y = chr(ord(position[1]) + (-1)**i[1]*(j + 1))
                    if not (0 < x < 9) or not (96 < ord(y) < 105):
                        break  
                    directionList.append((x, y))
                moves.append(directionList)

        elif figureType == "queen":
            for i in ((0,0),(0,1),(1,0),(1,1)):
                directionList = []
                directionList2 = []
                for j in range(7):
                    x = position[0] + (-1)**i[0]*(j + 1)
                    y = chr(ord(position[1]) + (-1)**i[1]*(j + 1))
                    x2 = position[0] + i[0]*(j + 1)*(-1)**i[1]
                    y2 = chr(ord(position[1]) + i[1]*(j + 1)*(-1)**i[0])
                    if (not (0 < x < 9) or not (96 < ord(y) < 105)) or (not (0 < x2 < 9) or not (96 < ord(y2) < 105)):
                        break  
                    directionList.append((x, y))
                    if i != (0,0): 
                        directionList2.append((x2, y2))
                moves.append(directionList)
                moves.append(directionList2)
        
        elif figureType == "king":
            for i in (-1, 0, 1):
                for j in (-1, 0, 1):
                    if i != 0 or j != 0:
                        moves.append([(position[0] + i, chr(ord(position[1]) + j))])



        __cutInvalidIndexes(moves)
        return moves
    
    def __cutInvalidIndexes(self, moves):
        for direction in moves:
            toRemove = []
            for move in direction:
                if not (0 < move[0] < 9) or not (96 < ord(move[1]) < 105):
                    toRemove.append(move)
            for removal in toRemove:
                direction.remove(removal)



    def __boolToColor(self, boolValue):
        if boolValue:
            return "white"
        else:
            return "black"

class Figure:
   def __init__(self, figure):
       self.x = None
       self.y = None
       self.figure = figure
       self.count_of_moves = 0

   def possible_moves(self, x, y):
       move = ThisBoard.position(x, y)
       move = [1, 2, 3, 4, 5, 6, 7, 8]
       if self.figure == 'rook':
           move = [(x+move, y), (x, y+move)]
       if self.figure == 'pawn':
           first_move = (x+2, y)
           forward = (x+1, y)
           throw_away = (x+1, y+1)
           move = [first_move, forward, throw_away]
       if self.figure == 'bishop':
           forward = (x+move, y+move)
           move = [forward]
       if self.figure == 'knight':
           right_forward = (x+1, y+3)
           left_forward = (x-1, y+3)
           right_backward = (x+1, y-3)
           left_backward = (x-1, y-3)
           right_up = (x+3, y+1)
           left_up = (x-3, y+1)
           right_down = (x+3, y-1)
           left_down = (x-3, y-1)
           forward = [(right_forward, left_forward, right_backward, left_backward, right_up, right_down, left_up, left_down)]
       if self.figure == 'bishop':
           left_forward = (x-move, y+move)
           right_forward = (x+move, y+move)
           left_backward = (x-move, y-move)
           right_backward = (x+move, y-move)
           forward = [(left_backward, left_forward, right_backward, right_forward)]

class UI:
 
   def display(self, get_figs=''):
       board = [['.']*8]*8
 
       print([' ', '1', '2', '3', '4', '5', '6', '7', '8'])
       for row in board:
           print("    ", row)
 
   def message(self, message_content):
       print(message_content)
 
   def play(self, get_valid_moves, move_figure=""):
 
       figurehead = (input("Select column (D): "),
                     input("Select row (5): "))
 
       valid_moves = get_valid_moves(figurehead)
 
       for i, move in enumerate(valid_moves):
           self.message(f'{i + 1}. Column: {move[0]} Row: {move[1]}')
 
       move = valid_moves[int(input("Select move (number): ")) - 1]
 
       # move_figure(move)
 
       self.message(move)

ThisBoard = Board()
print(ThisBoard.getCoords())