import numpy as np
import pygame
import sys
import math

ANZAHL_REIHEN = 6
ANZAHL_SPALTEN = 7
PIXEL = 100

width = ANZAHL_SPALTEN * PIXEL
height = (ANZAHL_REIHEN + 1) * PIXEL

size = (width, height)

RADIUS = int(PIXEL / 2 - 5)

BLAU = (0, 0, 255)
SCHWARZ = (0, 0, 0)
WEISS = (255, 255, 255)
ROT = (255, 0, 0)
GELB = (255, 255, 0)


def erstelle_spiel():
    board = np.zeros((6, 7))
    return board


def finde_höhe(brett, spalte):
    for r in range(ANZAHL_REIHEN):
        if brett[r][spalte] == 0:
            return r


def setze_plättchen(brett, reihe, spalte, stein):
    brett[reihe][spalte] = stein


def ist_moeglich(brett, col):
    return brett[ANZAHL_REIHEN - 1][col] == 0


def ueberpruefe_sieg(board, piece):
    # Horizontal testen
    for x in range(ANZAHL_SPALTEN - 3):
        for y in range(ANZAHL_REIHEN):
            if board[y][x] == piece and board[y][x + 1] == piece and board[y][x + 2] == piece and board[y][x + 3] == piece:
                return True

    # Vertical testen
    for x in range(ANZAHL_SPALTEN - 3):
        for y in range(ANZAHL_REIHEN):
            if board[y][x] == piece and board[y + 1][x] == piece and board[y + 2][x] == piece and board[y + 3][x] == piece:
                return True

    # Positive Diagonale testen
    for x in range(ANZAHL_SPALTEN - 3):
        for y in range(ANZAHL_REIHEN):
            if board[y][x] == piece and board[y + 1][x + 1] == piece and board[y + 2][x + 2] == piece and board[y + 3][x + 3] == piece:
                return True

    # Negative Diagonale testen
    for x in range(ANZAHL_SPALTEN - 3):
        for y in range(ANZAHL_REIHEN):
            if board[y][x] == piece and board[y - 1][x + 1] == piece and board[y - 2][x + 2] == piece and board[y - 3][x + 3] == piece:
                return True


def zeichne_board(board):
    for x in range(ANZAHL_SPALTEN):
        for y in range(ANZAHL_REIHEN):
            pygame.draw.rect(screen, BLAU, (x * PIXEL, y * PIXEL + PIXEL, PIXEL, PIXEL))
            pygame.draw.circle(screen, WEISS, (int(x * PIXEL + PIXEL / 2), int(y * PIXEL + PIXEL + PIXEL / 2)), RADIUS)

    for x in range(ANZAHL_SPALTEN):
        for y in range(ANZAHL_REIHEN):
            if board[y][x] == 1:
                pygame.draw.circle(screen, ROT, (int(x * PIXEL + PIXEL / 2), height - int(y * PIXEL + PIXEL / 2)), RADIUS)
            elif board[y][x] == 2:
                pygame.draw.circle(screen, GELB, (int(x * PIXEL + PIXEL / 2), height - int(y * PIXEL + PIXEL / 2)), RADIUS)
    pygame.draw.rect(screen, SCHWARZ, (0, 0, width, PIXEL))


    pygame.display.update()


brett = erstelle_spiel()
spiel_ende = False
runde = 0

pygame.display.set_caption("Vier gewinnt !")
screen = pygame.display.set_mode(size)
pygame.init()

zeichne_board(brett)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)

while not spiel_ende:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLAU, (0, 0, width, PIXEL))
            posx = event.pos[0]
            if runde == 0:
                pygame.draw.circle(screen, ROT, (posx, int(PIXEL / 2)), RADIUS)
            else:
                pygame.draw.circle(screen, GELB, (posx, int(PIXEL / 2)), RADIUS)
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            # print(event.pos)
            # Ask for Player 1 Input
            if runde == 0:
                posx = event.pos[0]
                col = int(math.floor(posx / PIXEL))

                if ist_moeglich(brett, col):
                    row = finde_höhe(brett, col)
                    setze_plättchen(brett, row, col, 1)
                    if ueberpruefe_sieg(brett, 1):
                        label = myfont.render("Player 1 wins!!", 1, ROT)
                        screen.blit(label, (40, 10))
                        spiel_ende = True


            # # Ask for Player 2 Input
            else:
                posx = event.pos[0]
                col = int(math.floor(posx / PIXEL))

                if ist_moeglich(brett, col):
                    row = finde_höhe(brett, col)
                    setze_plättchen(brett, row, col, 2)
                    if ueberpruefe_sieg(brett, 2):
                        label = myfont.render("Player 2 wins!!", 2, GELB)
                        screen.blit(label, (40, 10))
                        spiel_ende = True

            #print_board(board)
            zeichne_board(brett)

            runde += 1
            runde = runde % 2

            if spiel_ende:
                pygame.time.wait(3000)
