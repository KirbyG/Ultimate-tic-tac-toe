#imports
import pygame
import sys
from pygame.locals import *
from datetime import datetime as time

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

class Game:
    def __init__(self):
        self.continueGame = True
        self.subvictories = [[-1 for x in range(0, 3)] for x in range(0, 3)]
        self.oldx = 100
        self.oldy = 100
        self.mousePosition = [0, 0]
        self.board = [[[[-1 for x in range(3)] for x in range(3)] for x in range(3)] for x in range(3)]
        self.posBoard = [[[[[0 for x in range(2)] for x in range(3)] for x in range(3)] for x in range(3)] for x in range(3)]
        self.posBoard[0][0][0][0][0] = G + G2 + B2 / 2
        self.posBoard[0][0][0][0][1] = G + G2 + B2 / 2
        for row2 in range(0, 3):
            for col2 in range(0, 3):
                self.posBoard[0][0][row2][col2][0] = self.posBoard[0][0][0][0][0] + (B2 + T2) * col2
                self.posBoard[0][0][row2][col2][1] = self.posBoard[0][0][0][0][1] + (B2 + T2) * row2
        for row1 in range(0, 3):
            for col1 in range(0, 3):
                for row2 in range(0, 3):
                    for col2 in range(0, 3):
                        self.posBoard[row1][col1][row2][col2][0] = self.posBoard[0][0][row2][col2][0] + (B + T) * col1
                        self.posBoard[row1][col1][row2][col2][1] = self.posBoard[0][0][row2][col2][1] + (B + T) * row1
        pygame.init()
        self.screen = pygame.display.set_mode([L, L])
        background = pygame.Surface(self.screen.get_size())
        background = background.convert()
        background.fill((WHITE))
        self.screen.blit(background, (0, 0))
        self.myfont = pygame.font.SysFont(fontName, 50)
        pygame.display.update()

        self.rowRequired = -1
        self.colRequired = -1
        self.letter = 0

    #functions
    def maybeQuit(self, events):
        for event in events:
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

    def win(self, lWin):
        pygame.draw.rect(self.screen, WHITE, Rect((0, 0), (L, L)))
        
        bigger = pygame.font.SysFont(fontName, 900)
        label3 = bigger.render(lWin, 1, DARKORCHID)
        self.screen.blit(label3, (-15, -180))

        normal = pygame.font.SysFont(fontName, 20)
        label4 = normal.render("click anywhere to play again", 1, DARKORCHID)
        self.screen.blit(label4, (20, L - 20))

        pygame.display.update()

        startTime = time.now()
        while (time.now() - startTime).microseconds < 500000:
            self.getInput()
        
        while(pygame.mouse.get_pressed()[0] != 1):
            self.getInput()

        self.continueGame = False
            
    def makeGrid(self, x, y, thick, side):
        pygame.draw.rect(self.screen, BLACK, Rect(((G), (B + G)),(((3 * B) + (2 * T)), T)))
        pygame.draw.rect(self.screen, BLACK, Rect(((G), (2 * B + G + T)),(((3 * B) + (2 * T)), T)))
        pygame.draw.rect(self.screen, BLACK, Rect(((B + G), (G)),((T), 3 * B + 2 * T)))
        pygame.draw.rect(self.screen, BLACK, Rect(((2 * B + G + T), (G)),((T), 3 * B + 2 * T)))

        pygame.display.update()

    def makeSmallGrid(self, x, y):
        a = x - ((3 * B2)/2) - T2
        b = y - ((1 * B2)/2) - T2
        c = B - 2 * G2
        d = T2

        pygame.draw.rect(self.screen, BLACK, Rect((a, b), (c, d)))
        pygame.draw.rect(self.screen, BLACK, Rect((a, b + B2 + T2), (c, d)))
        pygame.draw.rect(self.screen, BLACK, Rect((b, a), (d, c)))
        pygame.draw.rect(self.screen, BLACK, Rect((b + B2 + T2, a), (d, c)))

    def drawBoard(self):
        for x in range (0, 3):
            for y in range (0, 3):
                self.makeSmallGrid((B/2) + G + x * (B+T), (B/2) + G + y * (B+T))

        self.makeGrid(0, 0, 0, 0)

        big = pygame.font.SysFont(fontName, 270)
        pygame.display.update()
        pygame.draw.rect(self.screen, WHITE, Rect((self.oldx, self.oldy), (300, 300)))
        for x in range(0, 3):
            for y in range(0, 3):
                label2 = big.render(letters[self.subvictories[x][y]], 1, GREY)
                self.screen.blit(label2, (self.posBoard[x][y][1][1][0] - 97, self.posBoard[x][y][1][1][1] - 150))

    def getInput(self):
        events = pygame.event.get()
        self.maybeQuit(events)
        self.mousePosition = pygame.mouse.get_pos()

    def drawUpdates(self):
        rowLevel1 = -1
        colLevel1 = -1
        rowLevel2 = -1
        colLevel2 = -1
        allowPlace = False
        for row1 in range(0, 3):
            for col1 in range(0, 3):
                for row2 in range(0, 3):
                    for col2 in range(0, 3):
                        x = self.posBoard[row1][col1][row2][col2][0]
                        y = self.posBoard[row1][col1][row2][col2][1]
                        if abs(self.mousePosition[X] - x) < B2 / 2 and abs(self.mousePosition[Y] - y) < B2 / 2:
                            rowLevel1 = row1
                            colLevel1 = col1
                            rowLevel2 = row2
                            colLevel2 = col2
                            full = True
                            for x2 in range(0, 3):
                                for y2 in range(0, 3):
                                    if self.board[self.colRequired][self.rowRequired][x2][y2] == -1:
                                        full = False
                            allowPlace = ((self.board[rowLevel1][colLevel1][rowLevel2][colLevel2] == -1) and ((full) or ((rowLevel1 == self.rowRequired) and (colLevel1 == self.colRequired)))) or (self.rowRequired == -1)
                            if allowPlace:
                                pygame.draw.rect(self.screen, HIGHLIGHT, Rect((x - B2 / 2 + 1, y - B2 / 2 + 1), (B2 + 1, B2 + 1)))
                            else:
                                pygame.draw.rect(self.screen, RED, Rect((x - B2 / 2 + 1, y - B2 / 2 + 1), (B2 + 1, B2 + 1)))
                        label = self.myfont.render(letters[self.board[row1][col1][row2][col2]], 1, BLACK)
                        self.screen.blit(label, (x - 17, y - 26))
                            
        label = self.myfont.render(letters[self.letter], 1, BLACK)
        self.screen.blit(label, (self.mousePosition[X] - 17, self.mousePosition[Y] - 17))
        self.oldx = self.mousePosition[X]-200
        self.oldy = self.mousePosition[Y]-200
        if pygame.mouse.get_pressed()[0] == 1 and allowPlace:
            self.colRequired = colLevel2
            self.rowRequired = rowLevel2
            self.board[rowLevel1][colLevel1][rowLevel2][colLevel2] = self.letter
            self.letter = (self.letter + 1) % 2
            if self.subvictories[rowLevel1][colLevel1] == -1: 
                for x in range(0, 3):
                    count = 0
                    for y in range(0, 3):
                        if self.board[rowLevel1][colLevel1][x][y] == 0:
                            count += 1
                    if count == 3:
                        self.subvictories[rowLevel1][colLevel1] = 0
                for y in range(0, 3):
                    count = 0
                    for x in range(0, 3):
                        if self.board[rowLevel1][colLevel1][x][y] == 0:
                            count += 1
                    if count == 3:
                        self.subvictories[rowLevel1][colLevel1] = 0
                if (self.board[rowLevel1][colLevel1][0][0] == 0 and self.board[rowLevel1][colLevel1][1][1] == 0 and self.board[rowLevel1][colLevel1][2][2] == 0) or (self.board[rowLevel1][colLevel1][0][2] == 0 and self.board[rowLevel1][colLevel1][1][1] == 0 and self.board[rowLevel1][colLevel1][2][0] == 0):
                    self.subvictories[rowLevel1][colLevel1] = 0
                if (self.board[rowLevel1][colLevel1][0][0] == 1 and self.board[rowLevel1][colLevel1][1][1] == 1 and self.board[rowLevel1][colLevel1][2][2] == 1) or (self.board[rowLevel1][colLevel1][0][2] == 1 and self.board[rowLevel1][colLevel1][1][1] == 1 and self.board[rowLevel1][colLevel1][2][0] == 1):
                    self.subvictories[rowLevel1][colLevel1] = 1

                for x in range(0, 3):
                    count = 0
                    for y in range(0, 3):
                        if self.board[rowLevel1][colLevel1][x][y] == 1:
                            count += 1
                    if count == 3:
                        self.subvictories[rowLevel1][colLevel1] = 1
                for y in range(0, 3):
                    count = 0
                    for x in range(0, 3):
                        if self.board[rowLevel1][colLevel1][x][y] == 1:
                            count += 1
                    if count == 3:
                        self.subvictories[rowLevel1][colLevel1] = 1

                for x in range(0, 3):
                    count = 0
                    for y in range(0, 3):
                        if self.subvictories[x][y] == 0:
                            count += 1
                    if count == 3:
                        self.win(letters[0])
                for y in range(0, 3):
                    count = 0
                    for x in range(0, 3):
                        if self.subvictories[x][y] == 0:
                            count += 1
                    if count == 3:
                        self.win(letters[0])
                if (self.subvictories[0][0] == 0 and self.subvictories[1][1] == 0 and self.subvictories[2][2] == 0) or (self.subvictories[0][2] == 0 and self.subvictories[1][1] == 0 and self.subvictories[2][0] == 0):
                    self.win(letters[0])
                for x in range(0, 3):
                    count = 0
                    for y in range(0, 3):
                        if self.subvictories[x][y] == 1:
                            count += 1
                    if count == 3:
                        self.win(letters[1])
                for y in range(0, 3):
                    count = 0
                    for x in range(0, 3):
                        if self.subvictories[x][y] == 1:
                            count += 1
                    if count == 3:
                        self.win(letters[1])
                if (self.subvictories[0][0] == 1 and self.subvictories[1][1] == 1 and self.subvictories[2][2] == 1) or (self.subvictories[0][2] == 1 and self.subvictories[1][1] == 1 and self.subvictories[2][0] == 1):
                    self.win(letters[1])

    #loop
    def run(self):
        while self.continueGame:
            self.drawBoard()

            self.getInput()

            self.drawUpdates()

#main code
while True:
    game = Game()
    game.run()
