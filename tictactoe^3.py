#imports
import pygame
import sys
from pygame.locals import *

#constants
fontName = "timesnewroman"

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
HIGHLIGHT = (90, 255, 32)
RED = (255, 47, 47)
GREY = (138, 133, 133)
DARKORCHID = (153, 50, 204)

L = 650
G = 20
T = 8
T2 = 4
B = ((L - 2 * G) - 2 * T)/3
G2 = 15
B2 = ((B - 2 * G2) - 2 * T2)/3

letters = ("O", "X", "")

X = 0
Y = 1

#variables
subvictories = [[-1 for x in range(0, 3)] for x in range(0, 3)]
oldx = 100
oldy = 100
mousePosition = [0, 0]
board = [[[[-1 for x in range(3)] for x in range(3)] for x in range(3)] for x in range(3)]
posBoard = [[[[[0 for x in range(2)] for x in range(3)] for x in range(3)] for x in range(3)] for x in range(3)]
posBoard[0][0][0][0][0] = G + G2 + B2 / 2
posBoard[0][0][0][0][1] = G + G2 + B2 / 2
for row2 in range(0, 3):
    for col2 in range(0, 3):
        posBoard[0][0][row2][col2][0] = posBoard[0][0][0][0][0] + (B2 + T2) * col2
        posBoard[0][0][row2][col2][1] = posBoard[0][0][0][0][1] + (B2 + T2) * row2
for row1 in range(0, 3):
    for col1 in range(0, 3):
        for row2 in range(0, 3):
            for col2 in range(0, 3):
                posBoard[row1][col1][row2][col2][0] = posBoard[0][0][row2][col2][0] + (B + T) * col1
                posBoard[row1][col1][row2][col2][1] = posBoard[0][0][row2][col2][1] + (B + T) * row1
pygame.init()
screen = pygame.display.set_mode([L, L])
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((WHITE))
screen.blit(background, (0, 0))
myfont = pygame.font.SysFont(fontName, 50)
pygame.display.update()

rowRequired = -1
colRequired = -1
rowLevel1 = 0
colLevel1 = 0
rowLevel2 = 0
colLevel2 = 0
full = True
letter = 0

#functions
def maybeQuit(events):
    for event in events:
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

def win(lWin):
    while(True):
        pygame.draw.rect(screen, WHITE, Rect((0, 0), (L, L)))
        bigger = pygame.font.SysFont(fontName, 900)
        label3 = bigger.render(lWin, 1, DARKORCHID)
        screen.blit(label3, (-15, -180))
        pygame.display.update()
        
def makeGrid(x, y, thick, side):
    pygame.draw.rect(screen, BLACK, Rect(((G), (B + G)),(((3 * B) + (2 * T)), T)))
    pygame.draw.rect(screen, BLACK, Rect(((G), (2 * B + G + T)),(((3 * B) + (2 * T)), T)))
    pygame.draw.rect(screen, BLACK, Rect(((B + G), (G)),((T), 3 * B + 2 * T)))
    pygame.draw.rect(screen, BLACK, Rect(((2 * B + G + T), (G)),((T), 3 * B + 2 * T)))

    pygame.display.update()

def makeSmallGrid(x, y):
    a = x - ((3 * B2)/2) - T2
    b = y - ((1 * B2)/2) - T2
    c = B - 2 * G2
    d = T2

    pygame.draw.rect(screen, BLACK, Rect((a, b), (c, d)))
    pygame.draw.rect(screen, BLACK, Rect((a, b + B2 + T2), (c, d)))
    pygame.draw.rect(screen, BLACK, Rect((b, a), (d, c)))
    pygame.draw.rect(screen, BLACK, Rect((b + B2 + T2, a), (d, c)))

def drawBoard():
    for x in range (0, 3):
        for y in range (0, 3):
            makeSmallGrid((B/2) + G + x * (B+T), (B/2) + G + y * (B+T))

    makeGrid(0, 0, 0, 0)

    big = pygame.font.SysFont(fontName, 270)
    pygame.display.update()
    pygame.draw.rect(screen, WHITE, Rect((oldx, oldy), (300, 300)))
    for x in range(0, 3):
        for y in range(0, 3):
            label2 = big.render(letters[subvictories[x][y]], 1, GREY)
            screen.blit(label2, (posBoard[x][y][1][1][0] - 97, posBoard[x][y][1][1][1] - 150))

def getInput():
    events = pygame.event.get()
    maybeQuit(events)
    mousePosition = pygame.mouse.get_pos()
    return mousePosition

def drawUpdates():
    global letter, rowRequired, colRequired, mousePosition, oldx, oldy
    #print mousePosition
    rowLevel1 = -1
    colLevel1 = -1
    rowLevel2 = -1
    colLevel2 = -1
    allowPlace = False
    for row1 in range(0, 3):
        for col1 in range(0, 3):
            for row2 in range(0, 3):
                for col2 in range(0, 3):
                    x = posBoard[row1][col1][row2][col2][0]
                    y = posBoard[row1][col1][row2][col2][1]
                    if abs(mousePosition[X] - x) < B2 / 2 and abs(mousePosition[Y] - y) < B2 / 2:
                        rowLevel1 = row1
                        colLevel1 = col1
                        rowLevel2 = row2
                        colLevel2 = col2
                        full = True
                        for x2 in range(0, 3):
                            for y2 in range(0, 3):
                                if board[colRequired][rowRequired][x2][y2] == -1:
                                    full = False
                        allowPlace = ((board[rowLevel1][colLevel1][rowLevel2][colLevel2] == -1) and ((full) or ((rowLevel1 == rowRequired) and (colLevel1 == colRequired)))) or (rowRequired == -1)
                        if allowPlace:
                            pygame.draw.rect(screen, HIGHLIGHT, Rect((x - B2 / 2 + 1, y - B2 / 2 + 1), (B2 + 1, B2 + 1)))
                        else:
                            pygame.draw.rect(screen, RED, Rect((x - B2 / 2 + 1, y - B2 / 2 + 1), (B2 + 1, B2 + 1)))
                    label = myfont.render(letters[board[row1][col1][row2][col2]], 1, BLACK)
                    screen.blit(label, (x - 17, y - 26))
                        
    label = myfont.render(letters[letter], 1, BLACK)
    screen.blit(label, (mousePosition[X] - 17, mousePosition[Y] - 17))
    oldx = mousePosition[X]-200
    oldy = mousePosition[Y]-200
    if pygame.mouse.get_pressed()[0] == 1 and allowPlace:
        colRequired = colLevel2
        rowRequired = rowLevel2
        board[rowLevel1][colLevel1][rowLevel2][colLevel2] = letter
        letter = (letter + 1) % 2
        if subvictories[rowLevel1][colLevel1] == -1: 
            for x in range(0, 3):
                count = 0
                for y in range(0, 3):
                    if board[rowLevel1][colLevel1][x][y] == 0:
                        count += 1
                if count == 3:
                    subvictories[rowLevel1][colLevel1] = 0
            for y in range(0, 3):
                count = 0
                for x in range(0, 3):
                    if board[rowLevel1][colLevel1][x][y] == 0:
                        count += 1
                if count == 3:
                    subvictories[rowLevel1][colLevel1] = 0
            if (board[rowLevel1][colLevel1][0][0] == 0 and board[rowLevel1][colLevel1][1][1] == 0 and board[rowLevel1][colLevel1][2][2] == 0) or (board[rowLevel1][colLevel1][0][2] == 0 and board[rowLevel1][colLevel1][1][1] == 0 and board[rowLevel1][colLevel1][2][0] == 0):
                subvictories[rowLevel1][colLevel1] = 0
            if (board[rowLevel1][colLevel1][0][0] == 1 and board[rowLevel1][colLevel1][1][1] == 1 and board[rowLevel1][colLevel1][2][2] == 1) or (board[rowLevel1][colLevel1][0][2] == 1 and board[rowLevel1][colLevel1][1][1] == 1 and board[rowLevel1][colLevel1][2][0] == 1):
                subvictories[rowLevel1][colLevel1] = 1

            for x in range(0, 3):
                count = 0
                for y in range(0, 3):
                    if board[rowLevel1][colLevel1][x][y] == 1:
                        count += 1
                if count == 3:
                    subvictories[rowLevel1][colLevel1] = 1
            for y in range(0, 3):
                count = 0
                for x in range(0, 3):
                    if board[rowLevel1][colLevel1][x][y] == 1:
                        count += 1
                if count == 3:
                    subvictories[rowLevel1][colLevel1] = 1

            for x in range(0, 3):
                count = 0
                for y in range(0, 3):
                    if subvictories[x][y] == 0:
                        count += 1
                if count == 3:
                    win(letters[0])
            for y in range(0, 3):
                count = 0
                for x in range(0, 3):
                    if subvictories[x][y] == 0:
                        count += 1
                if count == 3:
                    win(letters[0])
            if (subvictories[0][0] == 0 and subvictories[1][1] == 0 and subvictories[2][2] == 0) or (subvictories[0][2] == 0 and subvictories[1][1] == 0 and subvictories[2][0] == 0):
                win(letters[0])
            for x in range(0, 3):
                count = 0
                for y in range(0, 3):
                    if subvictories[x][y] == 1:
                        count += 1
                if count == 3:
                    win(letters[1])
            for y in range(0, 3):
                count = 0
                for x in range(0, 3):
                    if subvictories[x][y] == 1:
                        count += 1
                if count == 3:
                    win(letters[1])
            if (subvictories[0][0] == 1 and subvictories[1][1] == 1 and subvictories[2][2] == 1) or (subvictories[0][2] == 1 and subvictories[1][1] == 1 and subvictories[2][0] == 1):
                win(letters[1])

#loop
while True:
    drawBoard()

    mousePosition = getInput()

    drawUpdates()
