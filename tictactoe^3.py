import pygame
from pygame.locals import *

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
bigWin = [[-1 for x in range(0, 3)] for x in range(0, 3)]
#print B2
pygame.init()
screen = pygame.display.set_mode([L, L])
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((WHITE))
screen.blit(background, (0, 0))
pygame.display.update()
'''test = (50, 75)
print test
test[0] = 25
print test'''
def win(lWin):
    while(True):
        pygame.draw.rect(screen, WHITE, Rect((0, 0), (L, L)))
        bigger = pygame.font.SysFont(fontName, 950)
        label3 = bigger.render(lWin, 1, DARKORCHID)
        screen.blit(label3, (-15, -55))
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
oldx = 100
oldy = 100
p = 0
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
#print posBoard
#board[level 1 row][level 1 column][level 2 row][level 2 column]
'''board[0][2][1][2] = 1
print board'''
rR = -1
rC = -1
r1 = 0
c1 = 0
r2 = 0
c2 = 0
full = True
letter = 0
#pygame.mouse.set_visible(False)
#print pygame.font.get_fonts()
while True:
    #pygame.draw.rect(screen, WHITE, Rect((0, 0), (L, L)))
    for x in range (0, 3):
        for y in range (0, 3):
            makeSmallGrid((B/2) + G + x * (B+T), (B/2) + G + y * (B+T))
    makeGrid(0, 0, 0, 0)
    pygame.event.get()
    myfont = pygame.font.SysFont(fontName, 50)
    big = pygame.font.SysFont(fontName, 270)
    #screen.blit(label2, (oldx, oldy))
    pygame.draw.rect(screen, WHITE, Rect((oldx, oldy), (300, 300)))
    #pygame.draw.rect(screen, WHITE, Rect((x - B2 / 2 + 1, y - B2 / 2 + 1), (B2 + 1, B2 + 1)))
    p = pygame.mouse.get_pos()
    for x in range(0, 3):
        for y in range(0, 3):
            #print bigWin
            if bigWin[x][y] == 0:
                label2 = big.render("O", 1, GREY)
                screen.blit(label2, (posBoard[x][y][1][1][0] - 97, posBoard[x][y][1][1][1] - 110))
            if bigWin[x][y] == 1:
                label2 = big.render("X", 1, GREY)
                screen.blit(label2, (posBoard[x][y][1][1][0] - 97, posBoard[x][y][1][1][1] - 110))
    for row1 in range(0, 3):
        for col1 in range(0, 3):
            for row2 in range(0, 3):
                for col2 in range(0, 3):
                    x = posBoard[row1][col1][row2][col2][0]
                    y = posBoard[row1][col1][row2][col2][1]
                    if abs(p[0] - x) < B2 / 2 and abs(p[1] - y) < B2 / 2:
                        r1 = row1
                        c1 = col1
                        r2 = row2
                        c2 = col2
                        full = True
                        for x2 in range(0, 3):
                            for y2 in range(0, 3):
                                if board[rC][rR][x2][y2] == -1:
                                    full = False
                        if (board[r1][c1][r2][c2] == -1 and (rR == -1 or (r1 == rR and c1 == rC))) or (full and not (rC == c1 and rR == r1)):
                            pygame.draw.rect(screen, HIGHLIGHT, Rect((x - B2 / 2 + 1, y - B2 / 2 + 1), (B2 + 1, B2 + 1)))
                        else:
                            pygame.draw.rect(screen, RED, Rect((x - B2 / 2 + 1, y - B2 / 2 + 1), (B2 + 1, B2 + 1)))
                    if board[row1][col1][row2][col2] == 0:
                        label = myfont.render("O", 1, BLACK)
                        screen.blit(label, (x - 17, y - 17))
                    if board[row1][col1][row2][col2] == 1:
                        label = myfont.render("X", 1, BLACK)
                        screen.blit(label, (x - 17, y - 17))
    if letter == 0:
        label = myfont.render("O", 1, BLACK)
    if letter == 1:
        label = myfont.render("X", 1, BLACK)
    screen.blit(label, (p[0] - 17, p[1] - 17))
    oldx = p[0]-200
    oldy = p[1]-200
    if pygame.mouse.get_pressed()[0] == 1 and board[r1][c1][r2][c2] == -1 and (rR == -1 or (r1 == rR and c1 == rC) or (full)):
        #print r1
        #print c1
        rC = c2
        rR = r2
        board[r1][c1][r2][c2] = letter
        letter = (letter + 1) % 2
        if bigWin[r1][c1] == -1: 
            for x in range(0, 3):
                count = 0
                for y in range(0, 3):
                    if board[r1][c1][x][y] == 0:
                        count += 1
                if count == 3:
                    bigWin[r1][c1] = 0
            for y in range(0, 3):
                count = 0
                for x in range(0, 3):
                    if board[r1][c1][x][y] == 0:
                        count += 1
                if count == 3:
                    bigWin[r1][c1] = 0
                    #print bigWin
            if (board[r1][c1][0][0] == 0 and board[r1][c1][1][1] == 0 and board[r1][c1][2][2] == 0) or (board[r1][c1][0][2] == 0 and board[r1][c1][1][1] == 0 and board[r1][c1][2][0] == 0):
                bigWin[r1][c1] = 0
            if (board[r1][c1][0][0] == 1 and board[r1][c1][1][1] == 1 and board[r1][c1][2][2] == 1) or (board[r1][c1][0][2] == 1 and board[r1][c1][1][1] == 1 and board[r1][c1][2][0] == 1):
                bigWin[r1][c1] = 1

            for x in range(0, 3):
                count = 0
                for y in range(0, 3):
                    if board[r1][c1][x][y] == 1:
                        count += 1
                if count == 3:
                    bigWin[r1][c1] = 1
            for y in range(0, 3):
                count = 0
                for x in range(0, 3):
                    if board[r1][c1][x][y] == 1:
                        count += 1
                if count == 3:
                    bigWin[r1][c1] = 1

            for x in range(0, 3):
                count = 0
                for y in range(0, 3):
                    if bigWin[x][y] == 0:
                        count += 1
                if count == 3:
                    win("O")
            for y in range(0, 3):
                count = 0
                for x in range(0, 3):
                    if bigWin[x][y] == 0:
                        count += 1
                if count == 3:
                    win("O")
            if (bigWin[0][0] == 0 and bigWin[1][1] == 0 and bigWin[2][2] == 0) or (bigWin[0][2] == 0 and bigWin[1][1] == 0 and bigWin[2][0] == 0):
                win("O")
            for x in range(0, 3):
                count = 0
                for y in range(0, 3):
                    if bigWin[x][y] == 1:
                        count += 1
                if count == 3:
                    win("X")
            for y in range(0, 3):
                count = 0
                for x in range(0, 3):
                    if bigWin[x][y] == 1:
                        count += 1
                if count == 3:
                    win("X")
            if (bigWin[0][0] == 1 and bigWin[1][1] == 1 and bigWin[2][2] == 1) or (bigWin[0][2] == 1 and bigWin[1][1] == 1 and bigWin[2][0] == 1):
                win("X")
    
    #print pygame.mouse.get_pos()
#makeSmallGrid()

