import pygame as pg
from Chess.src.main.GameState import GameState
from Chess.src.main.Move import Move

pg.init()
WIDTH = HEIGHT = 512  # 400 good size as well
DIMENSIONS = 8  # based off of standard chess board 8x8
SQUARE_SIZE = HEIGHT // DIMENSIONS
MAX_FPS = 15
IMAGES = {}


def loadImages():
    pieces = ['wP', 'wB', 'wR', 'wN', 'wQ', 'wK', 'bP', 'bB', 'bR', 'bN', 'bQ', 'bK']
    for piece in pieces:
        IMAGES[piece] = pg.transform.scale(pg.image.load("../../../Chess/resources/img/" + piece + ".png"),
                                           (SQUARE_SIZE, SQUARE_SIZE))
    # image access = 'IMAGES['wp']'


def main():
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()
    running = True
    screen.fill((0, 0, 0))  # White Background
    gameState = GameState()
    validMoves = gameState.getValidMoves()
    moveMade = False
    loadImages()
    squareSelected = ()  # no square selected initially
    playerClicks = []

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.MOUSEBUTTONDOWN:  # get mouse input
                location = pg.mouse.get_pos()  # x & y location of the mouse
                col = location[0] // SQUARE_SIZE
                row = location[1] // SQUARE_SIZE
                if squareSelected == (row, col):
                    squareSelected = ()  # deselect
                    playerClicks = []  # clear player clicks
                squareSelected = (row, col)
                playerClicks.append(squareSelected)
                if len(playerClicks) == 2:  # after second click
                    move = Move(playerClicks[0], playerClicks[1], gameState.board)
                    print(move.getChessNotation())
                    if move in validMoves:
                        gameState.makeMove(move)
                        moveMade = True
                    squareSelected = ()
                    playerClicks = []
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_z:
                    gameState.undoMove()
                    moveMade = True

        if moveMade:
            validMoves = gameState.getValidMoves()
            moveMade = False
        drawGameState(screen, gameState)
        clock.tick(MAX_FPS)
        pg.display.flip()


def drawBoard(screen):
    colors = [pg.Color("white"), pg.Color("darkgreen")]
    for row in range(DIMENSIONS):
        for col in range(DIMENSIONS):
            color = colors[(row + col) % 2]
            pg.draw.rect(screen, color, pg.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


def drawPieces(screen, board):
    for row in range(DIMENSIONS):
        for col in range(DIMENSIONS):
            piece = board[row][col]
            if piece != "--":  # not empty square
                screen.blit(IMAGES[piece], pg.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


def drawGameState(screen, gameState):
    # order of function calls is important
    # with reversed order the pieces would be 'under' the board
    drawBoard(screen)
    drawPieces(screen, gameState.board)


if __name__ == '__main__':
    main()
