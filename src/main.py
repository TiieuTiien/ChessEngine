import pygame, sys, os

# Get the absolute path of the current script
current_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
# Construct the relative path and add it to sys.path
sys.path.append(current_path)

from gui.button import Button
from src.ChessMain import *

pygame.init()

SCREEN = pygame.display.set_mode((762, 512))
pygame.display.set_caption("Chess")
pygame.display.set_icon(pygame.image.load('images/neo/bQ.png'))

BG = pygame.image.load("assets/Background.png")

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)
    
def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")

        OPTIONS_TEXT = get_font(45).render("This is the OPTIONS screen.", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None, pos=(640, 460), 
                            text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()


"""
The main drive of our code. This will handle user input and updating the graphics
"""
def main():
    pygame.init()
    pygame.display.set_caption("Chess")
    pygame.display.set_icon(pygame.image.load('images/neo/bQ.png'))
    screen = pygame.display.set_mode((BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, BOARD_HEIGHT), pygame.SRCALPHA)
    clock = pygame.time.Clock()
    screen.fill(pygame.Color("white"))
    gs = ChessEngine.GameState()

    # Move log font
    moveLogFont = pygame.font.SysFont("Arial", 14, False, False)
    
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
    playerTwo = True # Same as above

    AIThinking = False
    moveFinderProcess = None
    moveUndone = False
    CHESS_BACK = Button(image=None, pos=(690, 490), text_input="BACK", font=get_font(20), base_color=(100, 100, 100), hovering_color="White")

    while running:
        humanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)# Check if the user has clicked the close button (QUIT event)
        CHESS_MOUSE_POS = pygame.mouse.get_pos()
        
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
        
            elif e.type == pygame.MOUSEBUTTONDOWN:
                if not gameOver and humanTurn:
                    col = CHESS_MOUSE_POS[0]//SQ_SIZE
                    row = CHESS_MOUSE_POS[1]//SQ_SIZE
                    # The user clicked the mouse twice or user clicked mouse log
                    if sqSelected == (row, col) or col >= 8:
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

                if CHESS_BACK.checkForInput(CHESS_MOUSE_POS):
                    main_menu()

            # Key handler
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_z:
                    gs.undoMove()
                    moveMade = True
                    gameOver = False
                    if AIThinking:
                        moveFinderProcess.terminate()
                        AIThinking = False
                    moveUndone = True

                if e.key == pygame.K_r:
                    gs = ChessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    gameOver = False
                    if AIThinking:
                        moveFinderProcess.terminate()
                        AIThinking = False
                    moveUndone = True
        
        # AI move finder
        if not gameOver and not humanTurn and not moveUndone:
            if not AIThinking:
                AIThinking = True
                print("Thinking...")

                # Use this to pass data between threads
                returnQueue = Queue()
                moveFinderProcess = Process(target=ChessAI.findBestMove, args=(gs, validMoves, returnQueue))
                moveFinderProcess.start()

            if not moveFinderProcess.is_alive():
                print("Done thinking!")
                AIMove = returnQueue.get()
                if AIMove is None:
                    AIMove = ChessAI.findRandomMove(validMoves)
                gs.makeMove(AIMove)
                moveMade = True
                AIThinking = False

        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False
            moveUndone = False

        drawGameState(screen, gs, validMoves, sqSelected, moveLogFont, CHESS_BACK, CHESS_MOUSE_POS)

        if gs.checkMate or gs.draw or gs.staleMate:
            gameOver = True
            text = 'Stale mate!!!' if gs.staleMate else 'Draw!!!' if gs.draw else 'Black wins by checkmate' if gs.whiteToMove else 'White wins by checkmate'
            drawEndGameText(screen, text)

        clock.tick(MAX_FPS)
        pygame.display.flip()

def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(40).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(381, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect_fixed.png"), pos=(381, 200), text_input="PLAY", font=get_font(35), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect_fixed.png"), pos=(381, 300), text_input="OPTIONS", font=get_font(35), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect_fixed.png"), pos=(381, 400), text_input="QUIT", font=get_font(35), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    main()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

if __name__ == "__main__":
    main_menu()