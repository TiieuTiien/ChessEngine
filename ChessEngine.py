"""
This class is responsible for storing all the information about the current state of o chess ga•e. It will also be
responsible for determining the valid moves at the current state. It will also keep a move log.
"""
class GameState():
    def __init__(self):
        # Normal board
        # self.board = [
        #     ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
        #     ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
        #     ["--", "--", "--", "--", "--", "--", "--", "--"],
        #     ["--", "--", "--", "--", "--", "--", "--", "--"],
        #     ["--", "--", "--", "--", "--", "--", "--", "--"],
        #     ["--", "--", "--", "--", "--", "--", "--", "--"],
        #     ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
        #     ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        # ]
        self.board = [
            ["bR_Neo", "bN_Neo", "bB_Neo", "bQ_Neo", "bK_Neo", "bB_Neo", "bN_Neo", "bR_Neo"],
            ["bP_Neo", "bP_Neo", "bP_Neo", "bP_Neo", "bP_Neo", "bP_Neo", "bP_Neo", "bP_Neo"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP_Neo", "wP_Neo", "wP_Neo", "wP_Neo", "wP_Neo", "wP_Neo", "wP_Neo", "wP_Neo"],
            ["wR_Neo", "wN_Neo", "wB_Neo", "wQ_Neo", "wK_Neo", "wB_Neo", "wN_Neo", "wR_Neo"]
        ]
        self.whiteToMove = True
        self.moveLog = []

    '''
    Take a move as a parameter and execute it (not special move like: en-passant, castling or promotion)
    '''
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved

        # Display moves in the game
        self.moveLog.append(move)

        # Switch turn
        self.whiteToMove = not self.whiteToMove

    '''
    Undo last move made
    '''
    def undoMove(self):
        # Check if moveLog is empty
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured

            # Switch turn
            self.whiteToMove = not self.whiteToMove

class Move():

    # Represent chess board Ranks and Files (Row and Column in programing context)
    ranksToRows = {"1":7, "2":6, "3":5, "4":4, "5":3, "6":2, "7":1," 8":0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}

    filesToCols = {"a":0, "b":1, "c":2, "d":3, "e":4, "f":5, "g":6, "h":7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]

    def getChessNotation(self):
        # Can be modify to show real chess notation
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c]+self.rowsToRanks[r]
        