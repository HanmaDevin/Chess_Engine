from Chess.src.main.Move import Move


class GameState:
    def __init__(self):
        # the board has standard chess dimensions. 'b' or 'w' indicate the color of the piece.
        # the pieces are represented by 2 characters, one lowercase and one uppercase
        # the notation is oriented by the standard chess notation
        # 'K' = King, 'Q' = Queen, 'R' = Rook, 'B' = Bishop, 'N' = Knight, 'P' = Pawn
        # '--' represents an empty space
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]

        self.whiteToMove = True
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.inCheck = False
        self.pins = []
        self.checks = []
        self.moveLog = []
        self.moveFunctions = {'P': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves,
                              'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)  # for undoing the move
        self.whiteToMove = not self.whiteToMove  # swap player
        # update kings location
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRow, move.endCol)
        if move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow, move.endCol)

    def undoMove(self):
        if len(self.moveLog) != 0:  # make sure a move was made before
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove
            # update kings location
            if move.pieceMoved == 'wK':
                self.whiteKingLocation = (move.startRow, move.startCol)
            if move.pieceMoved == 'bK':
                self.blackKingLocation = (move.startRow, move.startCol)

    def getValidMoves(self):
        moves = []
        self.inCheck, self.pins, self.checks = self.checkForPinsAndChecks()
        if self.whiteToMove:
            kingRow = self.whiteKingLocation[0]
            kingCol = self.whiteKingLocation[1]
        else:
            kingRow = self.blackKingLocation[0]
            kingCol = self.blackKingLocation[1]
        if self.inCheck:
            if len(self.checks) == 1:  # only one check -> move king / block / capture
                moves = self.getAllPossibleMoves()
                check = self.checks[0]
                checkRow = check[0]
                checkCol = check[1]
                pieceChecking = self.board[checkRow][checkCol]  # piece causing check
                validSquares = []
                if pieceChecking[1] == 'N':
                    validSquares = [(checkRow, checkCol)]
                else:
                    for i in range(1, 8):
                        validSquare = (
                        kingRow + check[2] * i, kingCol + check[3] * i)  # check[2] and check[3] are directions
                        validSquares.append(validSquare)
                        if validSquare[0] == checkRow and validSquare[1] == checkCol:
                            break
                # get rid of any moves that do not block check or king move
                for i in range(len(moves) - 1, -1, -1):  # traverse backwards when removing elem
                    if moves[i].pieceMoved[1] != 'K':  # did not move king, must block
                        if not (moves[i].endRow, moves[i].endCol) in validSquares:  # move does not block or capture
                            moves.remove(moves[i])
            else:
                self.getKingMoves(kingRow, kingCol, moves)
        else:
            moves = self.getAllPossibleMoves()
        return moves

    def isInCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])

    def squareUnderAttack(self, row, col):
        self.whiteToMove = not self.whiteToMove
        opponentMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove
        for move in opponentMoves:
            if move.endRow == row and move.endCol == col:  # square under attack
                return True

        return False

    def getAllPossibleMoves(self):
        moves = []
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                turn = self.board[row][col][0]
                if (turn == "w" and self.whiteToMove) or (turn == "b" and not self.whiteToMove):
                    piece = self.board[row][col][1]
                    self.moveFunctions[piece](row, col, moves)  # calls piece function per type

        return moves

    def getPawnMoves(self, row, col, moves):
        if self.whiteToMove:
            if self.board[row - 1][col] == "--":
                moves.append(Move((row, col), (row - 1, col), self.board))

                if row == 6 and self.board[row - 2][col] == "--":  # 2. square in front of pawn is empty
                    moves.append(Move((row, col), (row - 2, col), self.board))
            if col - 1 >= 0:  # not capturing beyond edge

                if self.board[row - 1][col - 1][0] == 'b':  # there is a black piece to capture
                    moves.append(Move((row, col), (row - 1, col - 1), self.board))

            if col + 1 <= 7:  # not capturing beyond edge
                if self.board[row - 1][col + 1][0] == 'b':
                    moves.append(Move((row, col), (row - 1, col + 1), self.board))

        else:  # black pawn moves
            if self.board[row + 1][col] == "--":
                moves.append(Move((row, col), (row + 1, col), self.board))

                if row == 1 and self.board[row + 2][col] == "--":
                    moves.append(Move((row, col), (row + 2, col), self.board))

            if col + 1 <= 7:  # not capturing beyond edge
                if self.board[row + 1][col + 1][1] == 'w':  # there is a white piece to capture
                    moves.append(Move((row, col), (row + 1, col + 1), self.board))

            if col - 1 >= 0:  # not capturing beyond edge
                if self.board[row + 1][col - 1][0] == 'w':
                    moves.append(Move((row, col), (row + 1, col - 1), self.board))
        # adding pawn promotion later

    def getRookMoves(self, row, col, moves):
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        opposingColor = "b" if self.whiteToMove else "b"
        for direction in directions:
            for i in range(1, 8):
                endRow = row + direction[0] * i
                endCol = col + direction[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:  # on board
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":  # empty space
                        moves.append(Move((row, col), (endRow, endCol), self.board))
                    elif endPiece[0] == opposingColor:
                        moves.append(Move((row, col), (endRow, endCol), self.board))
                        break
                    else:  # reached own piece
                        break
                else:  # off board
                    break

    def getKnightMoves(self, row, col, moves):
        knightMoves = ((-2, -1), (-1, -2), (-2, 1), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        ownColor = "w" if self.whiteToMove else "b"
        for move in knightMoves:
            endRow = row + move[0]
            endCol = col + move[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != ownColor:
                    moves.append(Move((row, col), (endRow, endCol), self.board))

    def getBishopMoves(self, row, col, moves):
        directions = [(1, 1), (-1, 1), (1, -1), (-1, -1)]
        opposingColor = "b" if self.whiteToMove else "w"
        for direction in directions:
            for i in range(1, 8):
                endRow = row + direction[0] * i
                endCol = col + direction[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((row, col), (endRow, endCol), self.board))
                    elif endPiece[0] == opposingColor:
                        moves.append(Move((row, col), (endRow, endCol), self.board))
                        break
                    else:  # reached own piece
                        break
                else:  # off board
                    break

    def getQueenMoves(self, row, col, moves):
        self.getRookMoves(row, col, moves)
        self.getBishopMoves(row, col, moves)

    def getKingMoves(self, row, col, moves):
        kingMoves = [(-1, -1), (-1, 1), (1, -1), (1, 1), (0, -1), (0, 1), (-1, 0), (1, 0)]
        ownColor = "w" if self.whiteToMove else "b"
        for i in range(8):
            endRow = row + kingMoves[i][0]
            endCol = col + kingMoves[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece != ownColor:
                    moves.append(Move((row, col), (endRow, endCol), self.board))

    def checkForPinsAndChecks(self):
        pins = []
        checks = []
        inCheck = False
        if self.whiteToMove:
            opponentColor = "b"
            ownColor = "w"
            startRow = self.whiteKingLocation[0]
            startCol = self.whiteKingLocation[1]
        else:
            opponentColor = "w"
            ownColor = "b"
            startRow = self.blackKingLocation[0]
            startCol = self.blackKingLocation[1]

        # check for checks and pins in all directions from king
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (1, -1), (-1, 1), (1, 1))
        for i in range(len(directions)):
            direction = directions[i]
            possiblePin = ()
            for j in range(1, 8):
                endRow = startRow + direction[0] * j
                endCol = startCol + direction[1] * j
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] == ownColor:
                        if possiblePin == ():
                            possiblePin = (endRow, endCol, direction[0], direction[1])
                        else:
                            break
                    elif endPiece[0] == opponentColor:
                        type = endPiece[1]
                        # checking the piece type
                        if (0 <= i <= 3 and type == 'R') or \
                                (4 <= i <= 7 and type == 'B') or \
                                (j == 1 and type == 'P' and ((opponentColor == 'w' and 6 <= i <= 7) or
                                                             (opponentColor == 'b' and 4 <= i <= 5))) or \
                                (type == 'Q') or (j == 1 and type == 'K'):
                            if possiblePin == ():
                                inCheck = True
                                checks.append((endRow, endCol, direction[0], direction[1]))
                                break
                            else:  # piece blocking so pin
                                pins.append(possiblePin)
                                break
                        else:  # opponent piece not applying check
                            break
                else:
                    break  # off board
        # check for knight checks
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for move in knightMoves:
            endRow = startRow + move[0]
            endCol = startCol + move[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] == opponentColor and endPiece[1] == 'N':
                    inCheck = True
                    checks.append((endRow, endCol, move[0], move[1]))
        return inCheck, pins, checks
