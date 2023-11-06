"""
This  is our main driver file. It will be responsible for handling user input and displaying the current GameState object.
"""
import pygame as p
import ChessEngine

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
    # pieces = ["wR", "wN", "wB", "wQ", "wK", "wP", "bR", "bN", "bB", "bQ", "bK", "bP"]
    pieces = ["wR_Neo", "wN_Neo", "wB_Neo", "wQ_Neo", "wK_Neo", "wP_Neo", "bR_Neo", "bN_Neo", "bB_Neo", "bQ_Neo", "bK_Neo", "bP_Neo"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/"+piece+".png"), (SQ_SIZE, SQ_SIZE))


"""
The main drive of our code. This will handle user input and updating the graphics
"""
def main():
    p.init()
    p.display.set_caption("Chess")
    p.display.set_icon(p.image.load('images/bQ_Neo.png'))
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()

    # Only loads once before while loop
    loadImages()
    running=True

    # No square selected yet, keep track of player clicks
    sqSelected = ()

    # Keop track of player click
    playerClicks = []

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
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
                    gs.makeMove(move)
                    sqSelected = ()
                    playerClicks = []

        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()

'''
Responsible for all the graphic within a current game state
'''
def drawGameState(screen, gs):
    drawBoard(screen)
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

'''
Draw the pieces
'''
def drawPieces(screen, board):
    for r in range(DIMENTIONS):
        for c in range(DIMENTIONS):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
    

if __name__ == "__main__":
    main()    