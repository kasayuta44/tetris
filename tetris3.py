import pygame
import random
import copy

#basic instances
display_width = 400
display_height = 900
screen = (display_width,display_height)
gameDisplay = pygame.display.set_mode(screen)
window = pygame.Surface(screen)
clock = pygame.time.Clock()

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
yellow = (255,255,0)
purple = (127,0,255)
orange = (255,128,0)
lblue = (0,255,255)

spawn = [3,23]

class piece:
    def __init__(self, matrix, spin, loc):
        self.matrix = matrix        #list of the matrices of each spin
        self.spin = spin            #int number for which spin within the list of matrices it would be (index from 0)
        self.loc = loc              #[x,y] location of the top left 

    def create(self):
        self.loc = spawn
    
    def get(self):
        return [self.matrix[self.spin],self.loc]
    
    def moveleft(self):
        self.loc[0] -= 1
    
    def moveright(self):
        self.loc[0] += 1
    
    def movedown(self):
        self.loc[1] -= 1
    
    def moveup(self):
        self.loc[1] += 1
  
    def rotateclock(self):
        if self.spin != 3:
            self.spin += 1
        else:
            self.spin = 0

    def rotatecounterclock(self):
        if self.spin != 0:
            self.spin -= 1
        else:
            self.spin = 3

class bag:
    def __init__(self,current,pieces1,pieces2):
        self.current = current
        self.pieces1 = pieces1
        self.pieces2 = pieces2

    def newbag(self):
        self.pieces1 = copy.deepcopy(self.pieces2)
        random.shuffle(self.pieces2)

    def nextpiece(self):
        if self.current == 6:
            self.current = 0
            self.newbag()
        else:
            self.current += 1
    
    def currentpiece(self):
        return self.pieces1[self.current]

class Tetris:
    def __init__(self,width,height):
        self.height = height
        self.width = width
        self.board = []
        self.score = 0
        
        #creating board
        for i in range(width):
            newline = []
            for j in range(height):
                newline.append(0)
            self.board.append(newline)

#locking in piece onto the board, info will equal to bag.currentpiece.get(), m is matrix from get() method
    def paste(self,info):
        m = info[0]
        for i in range(4):
            for j in range(4):
                if m[i][j] != 0:
                    self.board[m[1][0] + i][m[1][1] + j] = m[i][j]

#checking if there are any lines to be cleared
    def checklines(self):
        for j in range(20):
            check = True
            for i in range(10):
                if self.board[i][j] == 0:
                    check = False
            if check:
                self.board.remove(i)
                self.board.append([0 for x in range(23)])
        self.show()
                    
#displaying the board onto the screen    
    def show(self):
        for v,i in enumerate(self.board()):
            for w,j in enumerate(i):
                if i == 0:
                    pass
                elif j == 1:
                    pygame.draw.rect(window,lblue,(v*32,w*32,32,32))
                elif j == 2:
                    pygame.draw.rect(window,yellow,(v*32,w*32,32,32))
                elif j == 3:
                    pygame.draw.rect(window,purple,(v*32,w*32,32,32))
                elif j == 4:
                    pygame.draw.rect(window,green,(v*32,w*32,32,32))
                elif j == 5:
                    pygame.draw.rect(window,red,(v*32,w*32,32,32))
                elif j == 6:
                    pygame.draw.rect(window,blue,(v*32,w*32,32,32))
                elif j == 7:
                    pygame.draw.rect(window,orange,(v*32,w*32,32,32))
        pygame.display.update()

#after spin/movement of piece checking if any pieces would collide with existing pieces/border
#info will equal to bag.currentpiece.get() (possibly better to make it bag.currentpiece()???)
#m is matrix, lx and ly are location x and y coords respectively
    def collide(self,info):
        m = info[0]
        lx = info[1][0]
        ly = info[1][1]
        for i in range(4):
            for j in range(4):
                if m[i][j] != 0:
                    if self.board[lx + i][ly - j] != 0 or lx + i < 0 or lx + i > 10 or ly - j < 0: #logic needs to be fixed here
                        return False
        return True

#might need a method to adjust values within the object
    def left(self,info):
        info.moveleft()
        if not self.collide(info):
            info.moveright()
    
    def right(self,info):
        info.moveright()
        if not self.collide(info):
            info.moveleft()
    
    def down(self,info):
        info.movedown()
        if not self.collide(info):
            info.moveup()
    
    def harddrop(self,info):
        l = info.get()
        while l[1] > -1:
            info.movedown()
            if not self.collide():
                info.moveup()
                break

#info will be bag.currentpiece()
#replace pass with corresponding test cases from 
#https://tetris.wiki/Super_Rotation_System#:~:text=four%20constituent%20minos.-,Wall%20Kicks,into%20an%20alternative%20position%20nearby.
    def clockwise(self,info):
        lx = info.get()[1][0]
        ly = info.get()[1][1]
        info.rotateclock()
        if not self.collide():
            pass
            if not self.collide():
                pass
                if not self.collide():
                    pass
                    if not self.collide():
                        pass
                        if not self.collide():
                            info.rotatecounterclock()
    
    def counterclockwise(self,info):
        lx = info.get()[1][0]
        ly = info.get()[1][1]
        info.rotatecounterclock()
        if not self.collide():
            pass
            if not self.collide():
                pass
                if not self.collide():
                    pass
                    if not self.collide():
                        pass
                        if not self.collide():
                            info.rotateclock()

#method for the game
def start():
    game = Tetris(10,23)

pygame.init()
start()
