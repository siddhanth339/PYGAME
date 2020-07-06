import pygame
import time
from logic import solve
pygame.init()

SCREEN_WIDTH = 540
SCREEN_HEIGHT = 540
win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT + 60)) # + 60 to show the timer
pygame.display.set_caption("SUDOKU")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
font = pygame.font.SysFont('comicsans', 50)

class Cube:
    rows = 9
    cols = 9

    def __init__(self, value, row, col, width ,height):
        self.value = value
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False
        self.fixed = False # can we change this box's value
        if(self.value != 0):
            self.fixed = True
        
            
    def draw(self):
        if (self.selected == True):
            pygame.draw.rect(win, RED, (self.col * self.height, self.row * self.width, self.width, self.height), 4)
        if(self.value != 0):    
            text = font.render(str(self.value), 1, BLACK)
            win.blit(text, ((self.col * 60) + self.width//2 - text.get_width()//2, (self.row * 60) + self.height//2 - text.get_height()//2))
        
class Grid:
    board = [
        [7, 8, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7]
    ]
    
    answer = [[7, 8, 5, 4, 3, 9, 1, 2, 6],
            [6, 1, 2, 8, 7, 5, 3, 4, 9],
            [4, 9, 3, 6, 2, 1, 5, 7, 8],
            [8, 5, 7, 9, 4, 3, 2, 6, 1],
            [2, 6, 1, 7, 5, 8, 9, 3, 4],
            [9, 3, 4, 1, 6, 2, 7, 8, 5],
            [5, 7, 8, 3, 9, 4, 6, 1, 2], 
            [1, 2, 6, 5, 8, 7, 4, 9, 3],
            [3, 4, 9, 2, 1, 6, 8, 5, 7]]
    
    def __init__(self, rows, cols, width, height):
        self.rows = rows
        self.cols = cols
        self.cubes = []
        
        for i in range(rows):
            l = []
            for j in range(cols):
                l.append(Cube(self.board[i][j], i, j, 60, 60))
            self.cubes.append(l)
            
        self.width = width
        self.height = height
        self.prev_y = -1 # previously selected box's y . This is used to remove the red box from prev coordinates
        self.prev_x = -1 # previously selected box's x
        self.selectedBox_X = -1
        self.selectedBox_Y = -1
        
    def select(self, pos):
        pygame.event.pump() # This function is used to keep pygame active. Read the documentation of pygame.event.pump()
        self.selectedBox_X = pos[1] 
        self.selectedBox_Y = pos[0] 
        self.cubes[self.selectedBox_X][self.selectedBox_Y].selected = True
        
        if (self.prev_y != -1 and self.prev_x != -1):
            if (self.prev_y != self.selectedBox_Y or self.prev_x != self.selectedBox_X):
                self.cubes[self.prev_x][self.prev_y].selected = False
                self.prev_y = self.selectedBox_Y 
                self.prev_x = self.selectedBox_X
            
        elif(self.prev_y == -1 and self.prev_x == -1): # for the first time
            self.prev_y = self.selectedBox_Y 
            self.prev_x = self.selectedBox_X
    
    def ReDraw(self, time):
        redrawWindow(time)
        
    # check if the user has solved the puzzle
    def check(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if(self.answer[i][j] != self.cubes[i][j].value):
                    return False
        return True
    
    def set(self, key):
        self.cubes[self.selectedBox_X][self.selectedBox_Y].value = key
    
    def resetBoard(self):
        self.cubes = [] # reset all the cubes
        for i in range(self.rows):
            l = []
            for j in range(self.cols):
                l.append(Cube(self.board[i][j], i, j, 60, 60))
            self.cubes.append(l)
        self.ReDraw(0)
    
    def draw(self):
        # Draw grid
        gap = self.width / 9
        
        # Draw Horizontal lines
        for i in range(self.rows + 1):
            if (i % 3 == 0 and i != 0):
                thickness = 4
            else:
                thickness = 1
            pygame.draw.line(win, BLACK, (0, i * gap), (SCREEN_WIDTH, i * gap), thickness)
            
        # Draw vertical lines
        for j in range(self.cols + 1):
            if(j % 3 == 0 and j != 0):
                thickness = 4
            else: 
                thickness = 1
            pygame.draw.line(win, BLACK, (j * gap, 0), (j * gap, SCREEN_HEIGHT), thickness)    
            
        # Draw Cubes
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw()

def formatTime(seconds):
    
    sec = seconds % 60
    minutes = seconds // 60
    return str(minutes) + ":" + str(sec)

def redrawWindow(time):
    win.fill(WHITE)
    
    # draw board (the puzzle)
    board.draw()
    
    # draw timer at the bottom right corner
    timer = font.render("Time: " + formatTime(time), 1, BLACK)
    win.blit(timer, (360, 560))
    
    # draw the submit button to verify
    pygame.draw.rect(win, BLACK, (submitButton_X, submitButton_Y, submitButton_Width, submitButton_Height), 2)
    text = font.render("SUBMIT", 1, BLACK)
    win.blit(text, (submitButton_X + submitButton_Width//2 - text.get_width()//2, submitButton_Y + submitButton_Height//2 - text.get_height()//2))
    pygame.display.update()

def autoComplete():
    board.resetBoard() 
    solve(board)
    redrawWindow(0)
    
def displayResult(message):
    win.fill(WHITE)
    message = font.render(message, 1, BLACK)
    win.blit(message, (SCREEN_WIDTH//2 - message.get_width()//2, (SCREEN_HEIGHT + 60)//2 - message.get_height()//2))
    pygame.display.update()
    time.sleep(3)

    
board = Grid(9, 9, 540, 540)
submitButton_X = 30
submitButton_Y = 550
submitButton_Width = 150
submitButton_Height = 40
run = True
startTime = time.time()


while (run):
    
    currentTime = round(time.time() - startTime)
    key = 0
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            run = False
            break
        
        if (event.type == pygame.MOUSEBUTTONDOWN):
            pos = list(pygame.mouse.get_pos())
            
            if(pos[1] < 540):
                pos[0] = pos[0] // 60
                pos[1] = pos[1] // 60
                board.select(pos)

            # check if submit button is clicked
            elif(submitButton_X < pos[0] < submitButton_X + submitButton_Width and submitButton_Y < pos[1] < submitButton_Y + submitButton_Height): 
                if (board.check() == True):
                    displayResult("Great Job!!!")
                    run = False
                    break
                else:
                    displayResult("Try Again")
                    run = False
                    break
                    
        if (event.type == pygame.KEYDOWN):
            if (event.key == pygame.K_RETURN):
                autoComplete()
                time.sleep(2)
                run = False
                break
            if event.key == pygame.K_1:
                key = 1
            if event.key == pygame.K_2:
                key = 2
            if event.key == pygame.K_3:
                key = 3
            if event.key == pygame.K_4:
                key = 4
            if event.key == pygame.K_5:
                key = 5
            if event.key == pygame.K_6:
                key = 6
            if event.key == pygame.K_7:
                key = 7
            if event.key == pygame.K_8:
                key = 8
            if event.key == pygame.K_9:
                key = 9
            
            if(board.selectedBox_X != -1 and board.selectedBox_Y != -1): # check if any cube is selected or not
                # if a cube is selected check if we can change its value => check if fixed variable is False
                if (board.cubes[board.selectedBox_X][board.selectedBox_Y].fixed == False):
                    board.set(key)
                    
    if (run == False):
        break            
    redrawWindow(currentTime) # currentTime is in seconds      
pygame.quit()
