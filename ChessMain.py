"""
This  is our main driver file. It will be responsible for handling user input and displaying the current GameState object.
"""
import pygame as p
import ChessEngine, ChessAI

WIDTH = HEIGHT = 512
DIMENTIONS = 8
SQ_SIZE = HEIGHT // DIMENTIONS
MAX_FPS = 16
IMAGES = {}

'''
Initialize a global dictionary of images. This will be called exactly once in the main
'''
def loadImages():
    # Normal board
    pieces = ["wR", "wN", "wB", "wQ", "wK", "wP", "bR", "bN", "bB", "bQ", "bK", "bP"]
    theme = "neo/"
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/"+theme+piece+".png"), (SQ_SIZE, SQ_SIZE))


"""
The main drive of our code. This will handle user input and updating the graphics
"""
def main():
    p.init()
    p.display.set_caption("Chess")
    p.display.set_icon(p.image.load('images/neo/bQ.png'))
    screen = p.display.set_mode((WIDTH, HEIGHT), p.SRCALPHA)
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    
    # Generate validmoves
    validMoves = gs.getValidMoves()
    moveMade = False

    # Only loads once before while loop
    loadImages()
    running=True

    # No square selected yet, keep track of player clicks
    sqSelected = ()

    # Keop track of player click
    playerClicks = []

    gameOver = False
    playerOne = True # If human playing white then player one is true and vice versa
    playerTwo = False # Same as above

    while running:
        humanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver and humanTurn:
                    location = p.mouse.get_pos()
                    col = location[0]//SQ_SIZE
                    row = location[1]//SQ_SIZE
                    if sqSelected == (row, col):
                        sqSelected = ()
                        playerClicks = []
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)

                    if len(playerClicks) == 2:
                        move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                        print(move.getChessNotation())
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gs.makeMove(validMoves[i])
                                moveMade = True
                                sqSelected = ()
                                playerClicks = []
                        if not moveMade:
                            playerClicks = [sqSelected]

            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()
                    moveMade = True
                if e.key == p.K_r:
                    gs = ChessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
        
        # AI move finder
        if not gameOver and not humanTurn:
            AIMove = ChessAI.findBestMove(gs, validMoves)
            if AIMove is None:
                AIMove = ChessAI.findRandomMove(validMoves)
            gs.makeMove(AIMove)
            moveMade = True

        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False

        drawGameState(screen, gs, validMoves, sqSelected)

        if gs.checkMate:
            gameOver = True
            if gs.whiteToMove:
                drawText(screen, 'Black wins by checkmate')
            elif not gs.whiteToMove:
                drawText(screen, 'White wins by checkmate')
        elif gs.staleMate:
            gameOver = True
            drawText(screen, 'Stale mate!!!')

        clock.tick(MAX_FPS)
        p.display.flip()

'''
Hightlight square selected and moves for piece selected
'''
def highlightSquares(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'):
            # highlight selected square
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100) # Transperent value 0 -> 255
            s.fill(p.Color('yellow'))
            screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
            # # highlight moves from that square
            # s.fill(p.Color('yellow'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    drawDot(screen, (move.endCol*SQ_SIZE + SQ_SIZE//2, move.endRow*SQ_SIZE + SQ_SIZE//2), 10)

# Helper function to draw a dot
def drawDot(screen, center, alpha):
    inner_radius = 5  # Radius for the inner circle
    outer_radius = 10  # Radius for the outer circle
    inner_color = (20, 20, 20, alpha)
    outer_color = (60, 60, 60, alpha)

    # Draw the outer circle
    p.draw.circle(screen, outer_color, center, outer_radius)

    # Draw the inner circle
    p.draw.circle(screen, inner_color, center, inner_radius)

'''
Responsible for all the graphic within a current game state
'''
def drawGameState(screen, gs, validMoves, sqSelected):
    drawBoard(screen)
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board)

'''
Draw the square
'''
def drawBoard(screen):
    WHITE = (237, 238, 209)
    GREEN = (119, 153, 82)
    colors = [p.Color(WHITE), p.Color(GREEN)]

    for r in range(DIMENTIONS):
        for c in range(DIMENTIONS):
            color = colors[((r+c)%2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
    
    # Display Files and Ranks:
        # Display numbers only on the "a" file
        font = p.font.SysFont('comicsans', 14, bold=True)
        text = font.render(str(8 - r), True, colors[0] if r % 2 == 1 else colors[1])
        text_rect = text.get_rect(center=(SQ_SIZE // 8, r * SQ_SIZE + SQ_SIZE // 4))
        screen.blit(text, text_rect)
        
    # Display file letters on the top
    for c in range(DIMENTIONS):
        font = p.font.SysFont('comicsans', 18)
        text = font.render(chr(97 + c), True, colors[0] if c % 2 == 0 else colors[1])
        text_rect = text.get_rect(bottomright=(c * SQ_SIZE + SQ_SIZE - SQ_SIZE / 32, 8 * SQ_SIZE))
        screen.blit(text, text_rect)

'''
Draw the pieces
'''
def drawPieces(screen, board):
    for r in range(DIMENTIONS):
        for c in range(DIMENTIONS):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
    
def drawText(screen, text):
    font = p.font.SysFont("Gotham", 32, True, False)
    textObject = font.render(text, 0, p.Color('black'))
    textLocation = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH/2 - textObject.get_width()/2, HEIGHT/2 - textObject.get_height()/2)
    screen.blit(textObject, textLocation)

if __name__ == "__main__":
    main()    