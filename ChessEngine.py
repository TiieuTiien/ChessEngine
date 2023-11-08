"""
This class is responsible for storing all the information about the current state of o chess ga•e. It will also be
responsible for determining the valid moves at the current state. It will also keep a move log.
"""


class GameState:
    def __init__(self):
        # Normal board
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        # self.board = [
        #     ["bR_Neo","bN_Neo","bB_Neo","bQ_Neo","bK_Neo","bB_Neo","bN_Neo","bR_Neo"],
        #     ["bP_Neo","bP_Neo","bP_Neo","bP_Neo","bP_Neo","bP_Neo","bP_Neo","bP_Neo"],
        #     ["--", "--", "--", "--", "--", "--", "--", "--"],
        #     ["--", "--", "--", "--", "--", "--", "--", "--"],
        #     ["--", "--", "--", "--", "--", "--", "--", "--"],
        #     ["--", "--", "--", "--", "wR_Neo", "--", "--", "--"],
        #     ["wP_Neo","wP_Neo","wP_Neo","wP_Neo","wP_Neo","wP_Neo","wP_Neo","wP_Neo"],
        #     ["wR_Neo","wN_Neo","wB_Neo","wQ_Neo","wK_Neo","wB_Neo","wN_Neo","wR_Neo"],
        # ]

        self.moveFunctions = {
            'P': self.getPawnMoves,
            'R': self.getRockMoves,
            'N': self.getKnightMoves,
            'B': self.getBishopMoves,
            'Q': self.getQueenMoves,
            'K': self.getKingMoves,
        }

        self.whiteToMove = True
        self.moveLog = []

    """
    Take a move as a parameter and execute it (not special move like: en-passant, castling or promotion)
    """

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved

        # Display moves in the game
        self.moveLog.append(move)

        # Switch turn
        self.whiteToMove = not self.whiteToMove

    """
    Undo last move made
    """

    def undoMove(self):
        # Check if moveLog is empty
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured

            # Switch turn
            self.whiteToMove = not self.whiteToMove

    """
    All moves considering checks
    """

    def getValidMoves(self):
        return self.getAllPossibleMoves()

    """
    All move without considering checks
    """

    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == "w" and self.whiteToMove) or (turn == "b" and not self.whiteToMove):
                    piece = self.board[r][c][1]

                    # Calls the appropriate move function based on piece type
                    self.moveFunctions[piece](r, c, moves)
        return moves

    '''
    Get all the pawn moves for the pawn located at row, col and add these moves to the list
    '''
    def getPawnMoves(self, r, c, moves):
        # White's pawn moves
        if self.whiteToMove:
            if self.board[r-1][c] == "--":
                moves.append(Move((r, c), (r-1, c), self.board))
                if self.board[r-2][c] == "--" and r == 6:
                    moves.append(Move((r, c), (r-2, c), self.board))
            if c-1 >= 0:
                if self.board[r-1][c-1][0] == "b":
                    moves.append(Move((r, c), (r-1, c-1), self.board))
            if c+1 <= 7:
                if self.board[r-1][c+1][0] == "b":
                    moves.append(Move((r, c), (r-1, c+1), self.board))
        # Black's pawn moves
        else:
            if self.board[r+1][c] == "--":
                moves.append(Move((r, c), (r+1, c), self.board))
                if self.board[r+2][c] == "--" and r == 1:
                    moves.append(Move((r, c), (r+2, c), self.board))
            if c-1 >= 0:
                if self.board[r+1][c-1][0] == "w":
                    moves.append(Move((r, c), (r+1, c-1), self.board))
            if c+1 <= 7:
                if self.board[r+1][c+1][0] == "w":
                    moves.append(Move((r, c), (r+1, c+1), self.board))

    '''
    Get all the rock moves for the rock located at row, col and add these moves to the list
    '''
    def getRockMoves(self, r, c, moves):
        # # Check Up
        # for up in range (r-1, -1, -1):
        #     if self.board[up][c] == "--":
        #         moves.append(Move((r, c), (up, c), self.board))
        # # Check Down
        # for down in range (r+1, 8):
        #     if self.board[down][c] == "--":
        #         moves.append(Move((r, c), (down, c), self.board))
        # # Check Left
        # for left in range (c-1, -1, -1):
        #     if self.board[r][left] == "--":
        #         moves.append(Move((r, c), (r, left), self.board))
        # # Check Right
        # for right in range (r+1, 8):
        #     if self.board[r][right] == "--":
        #         moves.append(Move((r, c), (r, right), self.board))

        # Optimize way
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dr, dc in directions:
            new_r, new_c = r + dr, c + dc
            while 0 <= new_r < 8 and 0 <= new_c < 8:
                new_pos = self.board[new_r][new_c]
                if new_pos == "--" or new_pos[0] != self.board[r][c][0]:    
                    moves.append(Move((r, c), (new_r, new_c), self.board))
                    if new_pos != "--" and new_pos[0] != self.board[r][c][0]:
                        break   
                    new_r += dr
                    new_c += dc
                else:
                    break

    '''
    Get all the knight moves for the knight located at row, col and add these moves to the list
    '''
    def getKnightMoves(self, r, c, moves):
        directions = [(-1, -2), (-1, 2), (1, -2), (1, 2), (-2, -1), (-2, 1), (2, -1), (2, 1)]

        for dr, dc in directions:
            new_r, new_c = r + dr, c + dc
            if 0 <= new_r < 8 and 0 <= new_c < 8 and self.board[new_r][new_c][0] != self.board[r][c][0]:
                moves.append(Move((r, c), (new_r, new_c), self.board))

    '''
    Get all the bishop moves for the bishop located at row, col and add these moves to the list
    '''
    def getBishopMoves(self, r, c, moves):
        # Optimize way
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        for dr, dc in directions:
            new_r, new_c = r + dr, c + dc
            while 0 <= new_r < 8 and 0 <= new_c < 8:
                new_pos = self.board[new_r][new_c]
                if new_pos == "--" or new_pos[0] != self.board[r][c][0]:
                    moves.append(Move((r, c), (new_r, new_c), self.board))
                    if new_pos != "--" and new_pos[0] != self.board[r][c][0]:
                        break
                    new_r += dr
                    new_c += dc
                else:
                    break

    '''
    Get all the queen moves for the queen located at row, col and add these moves to the list
    '''
    def getQueenMoves(self, r, c, moves):
        self.getBishopMoves(r, c, moves)
        self.getRockMoves(r, c, moves)

    '''
    Get all the king moves for the king located at row, col and add these moves to the list
    '''
    def getKingMoves(self, r, c, moves):
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

        for dr, dc in directions:
            new_r, new_c = r + dr, c + dc
            if 0 <= new_r < 8 and 0 <= new_c < 8 and self.board[new_r][new_c][0] != self.board[r][c][0]:
                moves.append(Move((r, c), (new_r, new_c), self.board))
        

class Move:
    # Represent chess board Ranks and Files (Row and Column in programing context)
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}

    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow*1000+self.startCol*100+self.endRow*10+self.endCol
        # print(self.moveID)

    '''
    Overriding the equals method
    '''
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        # Can be modify to show real chess notation
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
