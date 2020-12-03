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
        self.__winner = None
    
    def getCoords(self):
        """
        Returns all the figures on the chessboard and their locations in '('pW', (0, 0))' notation
        """
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
            
            returnList.append((firstLetter + color, (ord(i[2][1]) - 97, i[2][0] - 1)))
        return returnList
    
    def getPossibleMoves(self, sourceCoords):
        """
        Returns a list of all possible moves in [(x, y)] notation, given source coords in (x, y) notation
        """
        newCoords = (sourceCoords[1] + 1, chr(sourceCoords[0] + 97))
        figure = self.__getFigureByCoords(newCoords)

        if figure[1] != self.__whiteIsCurrent:
            return []
        
        possibleMoves = self.__getValidMoves(*figure)
        returnList = []
        for moves in possibleMoves:
            for move in moves:
                returnList.append((ord(move[1]) - 97, move[0] - 1))
        return returnList
    
    def getCurrentPlayer(self):
        """
        Returns color of the current player
        """
        return self.__boolToColor(self.__whiteIsCurrent)
    
    def move(self, fromCoords, toCoords):
        """
        Handles movement and capturing of the pieces given source and target coords in (x, y) notation
        """

        # convert to (1, 'a') notation
        fromCoords = (fromCoords[1] + 1, chr(fromCoords[0] + 97))
        toCoords = (toCoords[1] + 1, chr(toCoords[0] + 97))

        # get info about the pieces
        movingFigure = self.__getFigureByCoords(fromCoords)

        targetFigure = self.__getFigureByCoords(toCoords)
        targetFigureColor = targetFigure[1]

        if not movingFigure[0]:
            print("This source coord is empty!")
            return
        
        elif movingFigure[1] != self.__whiteIsCurrent:
            print("This doesn't seem to be your piece!")
            return
        
        elif not self.__validateMove(toCoords, self.__getValidMoves(*movingFigure)):
            print("This does not seem to be a valid move!")
            return
        
        elif targetFigureColor != None:
            if targetFigureColor == self.__whiteIsCurrent:
                print("The target position seems to be taken by a piece of the same color!")
                return
            
            else:
                self.__coords.remove(targetFigure)
                self.__coords.remove(movingFigure)
                self.__coords.append([movingFigure[0], movingFigure[1], toCoords])
                print(f"There was one captured figure: {targetFigure[0]} of {self.__boolToColor(targetFigureColor)} color")

                # handle the capture of a king
                if targetFigure[0] == "king":
                    self.__winner = self.__whiteIsCurrent
        else:
            self.__coords.remove(movingFigure)
            self.__coords.append([movingFigure[0], movingFigure[1], toCoords])

        print("The figure was moved")
        self.__whiteIsCurrent = not self.__whiteIsCurrent
    
    def getWinner(self):
        """
        Returns the color of the winner if exists, else returns None
        """
        if self.__winner == None:
            return self.__winner

        else:
            return self.__boolToColor(self.__winner)

    def __getFigureByCoords(self, coords):
        """
        Returns piece info in ('pawn', True, (1, 'a')) notation by coords in (1, 'a') notation
        """
        for i in self.__coords:
            if i[2] == coords:
                return i
        return (None, None, None)

    def __getValidMoves(self, figureType, isWhite, position):
        """
        Returns a list of directions of moves given the parameters,
        """
        moves = []
        if figureType == "pawn":
            if isWhite:
                if position[0] == 2 and self.__getFigureByCoords((position[0] + 2, position[1]))[0] == None:
                    moves = [[(position[0] + 1, position[1]), (position[0] + 2, position[1])]]
                elif self.__getFigureByCoords((position[0] + 1, position[1]))[0] == None:
                    moves = [[(position[0] + 1, position[1])]]
                
                # capturing a piece diagonally
                if self.__getFigureByCoords((position[0] + 1, chr(ord(position[1]) + 1)))[1] == False:
                    moves.append([(position[0] + 1, chr(ord(position[1]) + 1))])
                if self.__getFigureByCoords((position[0] + 1, chr(ord(position[1]) - 1)))[1] == False:
                    moves.append([(position[0] + 1, chr(ord(position[1]) - 1))])

            else:
                if position[0] == 7 and self.__getFigureByCoords((position[0] - 2, position[1]))[0] == None:
                    moves = [[(position[0] - 1, position[1]), (position[0] - 2, position[1])]]
                elif self.__getFigureByCoords((position[0] - 1, position[1]))[0] == None:
                    moves = [[(position[0] - 1, position[1])]]
                
                # capturing a piece diagonally
                if self.__getFigureByCoords((position[0] - 1, chr(ord(position[1]) + 1)))[1]:
                    moves.append([(position[0] - 1, chr(ord(position[1]) + 1))])
                if self.__getFigureByCoords((position[0] - 1, chr(ord(position[1]) - 1)))[1]:
                    moves.append([(position[0] - 1, chr(ord(position[1]) - 1))])

        elif figureType == "rook" or figureType == "queen":
            for i in ((0,1,0),(0,1,1),(1,0,0),(1,0,1)):
                directionList = []
                for j in range(7):
                    x = position[0] + i[0]*(j + 1)*(-1)**i[2]
                    y = chr(ord(position[1]) + i[1]*(j + 1)*(-1)**i[2])
                    if not (0 < x < 9) or not (96 < ord(y) < 105) or (self.__getFigureByCoords((x,y))[1] == self.__whiteIsCurrent):
                        break  
                    directionList.append((x, y))
                    if self.__getFigureByCoords((x,y))[0]:
                        break
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
                    if not (0 < x < 9) or not (96 < ord(y) < 105) or (self.__getFigureByCoords((x,y))[1] == self.__whiteIsCurrent):
                        break  
                    directionList.append((x, y))
                    if self.__getFigureByCoords((x,y))[0]:
                        break
                moves.append(directionList)
        
        elif figureType == "king":
            for i in (-1, 0, 1):
                for j in (-1, 0, 1):
                    if i != 0 or j != 0:
                        moves.append([(position[0] + i, chr(ord(position[1]) + j))])

        if figureType == "queen":
            for i in ((0,0),(0,1),(1,0),(1,1)):
                directionList = []
                for j in range(7):
                    x = position[0] + (-1)**i[0]*(j + 1)
                    y = chr(ord(position[1]) + (-1)**i[1]*(j + 1))
                    if (not (0 < x < 9) or not (96 < ord(y) < 105)) or (self.__getFigureByCoords((x,y))[1] == self.__whiteIsCurrent):
                        break  
                    directionList.append((x, y))
                    if self.__getFigureByCoords((x,y))[0]:
                        break
                moves.append(directionList)


        self.__cutInvalidIndexes(moves)
        return moves

    def __cutInvalidIndexes(self, moves):
        """
        Cuts indexes that are outside the chessboard or target a piece of the same color from a list of directions of moves.
        """
        for direction in moves:
            toRemove = []
            for move in direction:
                if not (0 < move[0] < 9) or not (96 < ord(move[1]) < 105) or (self.__getFigureByCoords((move[0], move[1]))[1] == self.__whiteIsCurrent):
                    toRemove.append(move)
            for removal in toRemove:
                direction.remove(removal)
    
    def __validateMove(self, move, validMoves):
        """
        Returns True if a move is in a given list of direcions of moves, else returns False
        """
        for moves in validMoves:
            if move in moves:
                return True
        
        return False


    def __boolToColor(self, boolValue):
        """
        Converts booleans to string by the rules:
        True -> 'white'
        False -> 'black'
        """
        if boolValue:
            return "white"
        else:
            return "black"
