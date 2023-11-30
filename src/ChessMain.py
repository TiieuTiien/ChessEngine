"""
This  is our main driver file. It will be responsible for handling user input and displaying the current GameState object.
"""
import sys
import os
import pygame
from gui.button import Button

from src import ChessEngine, ChessAI
from multiprocessing import Process, Queue

BOARD_WIDTH = BOARD_HEIGHT = 512
MOVE_LOG_PANEL_WIDTH = 250
MOVE_LOG_PANEL_HEIGHT = BOARD_HEIGHT
DIMENTIONS = 8
SQ_SIZE = BOARD_HEIGHT // DIMENTIONS
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
        IMAGES[piece] = pygame.transform.scale(pygame.image.load("images/"+theme+piece+".png"), (SQ_SIZE, SQ_SIZE))

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

'''
Responsible for all the graphic within a current game state
'''
def drawGameState(screen, gs, validMoves, sqSelected, moveLogFont, CHESS_BACK, CHESS_MOUSE_POS):
    drawBoard(screen)
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board)
    drawMoveLog(screen, gs, moveLogFont)
    drawBackButton(screen, CHESS_BACK, CHESS_MOUSE_POS)

def drawBackButton(screen, CHESS_BACK, CHESS_MOUSE_POS):        
    CHESS_BACK.changeColor(CHESS_MOUSE_POS)
    CHESS_BACK.update(screen)

'''
Draw the square
'''
def drawBoard(screen):
    WHITE = (237, 238, 209)
    GREEN = (119, 153, 82)
    colors = [pygame.Color(WHITE), pygame.Color(GREEN)]

    for r in range(DIMENTIONS):
        for c in range(DIMENTIONS):
            color = colors[((r+c)%2)]
            pygame.draw.rect(screen, color, pygame.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
    
    # Display Files and Ranks:
        # Display numbers only on the "a" file
        font = pygame.font.SysFont('comicsans', 14, bold=True)
        text = font.render(str(8 - r), True, colors[0] if r % 2 == 1 else colors[1])
        text_rect = text.get_rect(center=(SQ_SIZE // 8, r * SQ_SIZE + SQ_SIZE // 4))
        screen.blit(text, text_rect)
        
    # Display file letters on the top
    for c in range(DIMENTIONS):
        font = pygame.font.SysFont('comicsans', 18)
        text = font.render(chr(97 + c), True, colors[0] if c % 2 == 0 else colors[1])
        text_rect = text.get_rect(bottomright=(c * SQ_SIZE + SQ_SIZE - SQ_SIZE / 32, 8 * SQ_SIZE))
        screen.blit(text, text_rect)

'''
Hightlight square selected and moves for piece selected
'''
def highlightSquares(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'):
            # highlight selected square
            s = pygame.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100) # Transperent value 0 -> 255
            s.fill(pygame.Color('yellow'))
            screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
            # # highlight moves from that square
            # s.fill(pygame.Color('yellow'))
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
    pygame.draw.circle(screen, outer_color, center, outer_radius)

    # Draw the inner circle
    pygame.draw.circle(screen, inner_color, center, inner_radius)

'''
Draw the pieces
'''
def drawPieces(screen, board):
    for r in range(DIMENTIONS):
        for c in range(DIMENTIONS):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], pygame.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

'''
Draw move log
'''
def drawMoveLog(screen, gs, font):
    moveLogRect= pygame.Rect(BOARD_WIDTH, 0, MOVE_LOG_PANEL_WIDTH, MOVE_LOG_PANEL_HEIGHT)
    pygame.draw.rect(screen, pygame.Color(50, 50, 50), moveLogRect)
    moveLog = gs.moveLog
    moveTexts = []
    for i in range(0, len(moveLog), 2):
        moveString = str(i//2 + 1) + ". " + str(moveLog[i]) + "   "
        # Make sure black make a move
        if i+1 < len(moveLog):
            moveString += str(moveLog[i+1]) + "     "
        moveTexts.append(moveString)

    movePerRow = 1
    padding = 5
    lineSpacing = 2
    textY = padding
    for i in range(0, len(moveTexts), movePerRow):
        text = ""
        for j in range(movePerRow):
            if i+j < len(moveTexts):
                text += moveTexts[i+j]
        textObject = font.render(text, True, pygame.Color('white'))
        textLocation = moveLogRect.move(padding, textY)
        screen.blit(textObject, textLocation)
        textY += textObject.get_height() + lineSpacing
    
def drawEndGameText(screen, text):
    font = pygame.font.SysFont("Montserrat Black", 32, True, False)
    textObject = font.render(text, 0, pygame.Color('gray'))
    textLocation = pygame.Rect(0, 0, BOARD_WIDTH, BOARD_HEIGHT).move(BOARD_WIDTH/2 - textObject.get_width()/2, BOARD_HEIGHT/2 - textObject.get_height()/2)
    screen.blit(textObject, textLocation)