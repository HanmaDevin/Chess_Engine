import pygame as pg
from Chess.src.main.GameState import GameState

pg.init()
WIDTH = HEIGHT = 512 # 400 good size as well
DIMENSIONS = 8 # based off of standard chess board 8x8
SQUARE_SIZE = HEIGHT//DIMENSIONS
MAX_FPS = 15
IMAGES = {}

def loadImages():
    pieces = ['wP', 'wB', 'wR', 'wN', 'wQ', 'wK', 'bP', 'bB', 'bR', 'bN', 'bQ', 'bK']
    for piece in pieces:
        IMAGES[piece] = pg.transform.scale(pg.image.load("../../../Chess/resources/img/" + piece + ".png"), (SQUARE_SIZE, SQUARE_SIZE))
    # image access = 'IMAGES['wp']'

def main():
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()
    running = True
    screen.fill((0,0,0)) # White Background
    gameState = GameState()
    loadImages()
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        clock.tick(MAX_FPS)
        pg.display.flip()
        drawBoard(screen)


def drawBoard(screen):
    colors = [pg.Color("white"), pg.Color("darkgreen")]
    for i in range(DIMENSIONS):
        for j in range(DIMENSIONS):
            color = colors[(i+j) % 2]
            pg.draw.rect(screen, color, pg.Rect(j*SQUARE_SIZE, i*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


def drawPieces(screen, board):
    pass


def drawGameState(screen, gameState):
    # order of function calls is important
    # with reversed order the pieces would be 'under' the board
    drawBoard(screen)
    drawPieces(screen, gameState.board)
    


if __name__ == '__main__':
    main()
