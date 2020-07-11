import pygame
import time
import random

pygame.init()
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("S N A K E")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
DARK_GREEN = (0, 100, 0)
font = pygame.font.SysFont('comicsans', 80)
        
class Snake:
    def __init__(self):
        self.vel = 1
        self.left = False
        self.right = True
        self.up = False
        self.down = False
        self.initialX = 2 # row
        self.initialY = 8 # col
        self.Length = 3
        self.body = [[self.initialX, self.initialY]]
        self.score = 0
        self.prevScore = 0 # to check whether the snake ate the food
    
    def update(self):
        if(self.left):
            self.initialY -= self.vel

            if(self.Length > 1): 
                if([self.initialX % 20, self.initialY % 20] in self.body): # if the snake bites its own body
                    return -1
            
            self.body.append([self.initialX % 20, self.initialY % 20])
            if(self.score != self.prevScore):
                self.prevScore = self.score
            else:
                del self.body[0]
            
        if(self.right):
            self.initialY += self.vel

            if(self.Length > 1): 
                if([self.initialX % 20, self.initialY % 20] in self.body): # if the snake bites its own body
                    return -1
            
            self.body.append([self.initialX % 20, self.initialY % 20])
            if(self.score != self.prevScore):
                self.prevScore = self.score
            else:
                del self.body[0]
            
        if(self.up):
            self.initialX -= self.vel

            if(self.Length > 1): 
                if([self.initialX % 20, self.initialY % 20] in self.body): # if the snake bites its own body
                    return -1
            
            self.body.append([self.initialX % 20, self.initialY % 20])
            if(self.score != self.prevScore):
                self.prevScore = self.score
            else:
                del self.body[0]
            
        if(self.down):
            self.initialX += self.vel

            if(self.Length > 1): 
                if([self.initialX % 20, self.initialY % 20] in self.body): # if the snake bites its own body
                    return -1
            
            self.body.append([self.initialX % 20, self.initialY % 20])
            if(self.score != self.prevScore):
                self.prevScore = self.score
            else:
                del self.body[0]
                
    def draw(self):            
        for i in range(len(self.body)):
            pygame.draw.rect(win, DARK_GREEN, (self.body[i][1] * 30, self.body[i][0] * 30, 30, 30))
            if (i == len(self.body) - 1): # draw eyes 
                radius = 5
                eye1 = (self.body[i][1] * 30 + 10, self.body[i][0] * 30 + 5)
                eye2 = (self.body[i][1] * 30 + 10, self.body[i][0] * 30 + 20)
                pygame.draw.circle(win, BLACK, eye1, radius)
                pygame.draw.circle(win, BLACK, eye2, radius)               

class Food:
    def __init__(self):
        self.row = random.randint(0, 19)
        self.col = random.randint(0, 19)
        self.foodPos = [self.row, self.col]
        
    def ate(self):
        self.row = random.randint(0, 19)
        self.col = random.randint(0, 19)
        self.foodPos = [self.row, self.col]
        
    def draw(self):
        pygame.draw.rect(win, RED, (self.col * 30, self.row * 30, 30, 30))
        
def EndGame(): # Game over
    win.fill(WHITE)
    text = font.render("GAME OVER", 1, BLACK)
    win.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HEIGHT//2 - text.get_height()//2))
    pygame.display.update()
    time.sleep(2)
    
    win.fill(WHITE)
    text = font.render("SCORE: " + str(snake.score), 1, BLACK)
    win.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HEIGHT//2 - text.get_height()//2))
    pygame.display.update()
    time.sleep(2)
    
def reDrawGameWindow():
    win.fill(WHITE)
    for i in range(600//30):
        pygame.draw.line(win, BLACK, (0, i * 30), (SCREEN_WIDTH, i * 30))
    
    for i in range(600//30):
        pygame.draw.line(win, BLACK, (i * 30, 0), (i * 30, SCREEN_HEIGHT))
    
    x = snake.update()
    if (x == -1):
        EndGame()
        return -1
    snake.draw()
    food.draw()

    pygame.display.update()


run = True
fps = 10
clock = pygame.time.Clock()
snake = Snake()
food = Food()

while (run):
    clock.tick(fps)
    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            EndGame()
            run = False
        
        if (event.type == pygame.KEYDOWN):     
            if (event.key == pygame.K_LEFT): # turn left
                if (snake.right != True): # If the snake was going right and then left key was pressed (going right we pressed the left key) then snake cannot go in  opposite direction (snake does not have reverse gear), 
                    # it must go right then left or left then right
                    # -> <- not possible
                    # -> Down <- possible
                    # -> Up <- left possible
                    
                    snake.left = True
                    snake.right = False
                    snake.up = False
                    snake.down = False
            
            if(event.key == pygame.K_RIGHT):
                if (snake.left != True):
                    snake.right = True
                    snake.left = False
                    snake.up = False
                    snake.down = False
                
            if(event.key == pygame.K_UP):
                if (snake.down != True):
                    snake.right = False
                    snake.left = False
                    snake.up = True
                    snake.down = False
             
            if(event.key == pygame.K_DOWN):
                if (snake.up != True):
                    snake.right = False
                    snake.left = False
                    snake.up = False
                    snake.down = True
    
    if (food.foodPos in snake.body):
        snake.score += 1
        snake.Length += 1
        food.ate()
        
    x = reDrawGameWindow()        
    if (x == -1):
        run = False
pygame.quit()
