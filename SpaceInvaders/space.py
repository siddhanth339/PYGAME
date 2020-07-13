import pygame
import math
import random
from pygame import mixer

pygame.init()

# dimensions of window
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 800

win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders")

# load images
spaceShip = pygame.image.load('spaceship.png')
icon = pygame.image.load('ufo.png')
bg = pygame.image.load('background.png')
enemyImg = pygame.image.load('enemy.png')
bulletImg = pygame.image.load('bullet.png')

pygame.display.set_icon(icon)

# play background music
mixer.music.load('music.mp3')
mixer.music.play(-1)

# colors
WHITE = (255, 255, 255)

# font
font = pygame.font.SysFont('comicsanc', 60)

# player (the spaceship)
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity = 6
        self.fired = False
        self.score = 0
        self.bullet = Bullet(self.x + 64//2, self.y + 64//2)
        
    def fire(self):
        self.bullet = Bullet(self.x + 64//2, self.y + 64//2)
        self.fired = True

    def draw(self):
        win.blit(spaceShip, (self.x, self.y))
        
# enemy
class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity = 4
        self.right = True
        self.left = False
        
    def draw(self):
        
        if (self.x + 64 > SCREEN_WIDTH and self.right): # moving right
            self.y += 10
            self.right = False
            self.left = True
            
        elif (self.x - self.velocity < 0 and self.left):
            self.y += 10
            self.left = False
            self.right = True
            
        else:
            if (self.right):
                self.x += self.velocity
            else:
                self.x -= self.velocity
        
        win.blit(enemyImg, (self.x, self.y))
   
# bullet
class Bullet:
    def __init__(self, x, y):
        self.velocity = 10
        self.x = x
        self.y = y

    def draw(self):
        if (self.y - self.velocity < 0):
            player.fired = False
            return 
        else:
            self.y -= self.velocity
        win.blit(bulletImg, (self.x, self.y))
        
run = True
player = Player(370, 480)
num_enemies = 6
enemies = [Enemy(100, 100), Enemy(100, 200), Enemy(20, 10), Enemy(200, 10), Enemy(400, 100), Enemy(500, 100)]

def isCollision():
    for enemy in enemies:
        distance = math.sqrt(pow(player.bullet.x - enemy.x, 2) + pow(player.bullet.y - enemy.y, 2))
        if (distance < 27):
            collisionSound = mixer.Sound('explosion.wav')
            collisionSound.play()
            player.score += 1
            enemy.x = random.randint(0, SCREEN_WIDTH-64)
            enemy.y = random.randint(0, player.y-100)
            player.fired = False
        
def redrawGameWindow():
    win.blit(bg, (0, 0))
    player.draw()
    isCollision()
    for enemy in enemies: 
        enemy.draw()
    if (player.fired == True):
        player.bullet.draw()
    
    text = font.render("SCORE: " + str(player.score), 1, WHITE)
    win.blit(text, (5, 5))
    
    pygame.display.update()
    
while (run):
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            run = False
        
        if (event.type == pygame.KEYDOWN):
            if (event.key == pygame.K_SPACE and player.fired == False):
                bulletSound = mixer.Sound('laser.wav')
                bulletSound.play()
                player.fire()
    keys = pygame.key.get_pressed()
    
    if (keys[pygame.K_LEFT] and player.x - player.velocity > 0):
        player.x -= player.velocity
    
    elif(keys[pygame.K_RIGHT] and player.x + 64 < SCREEN_WIDTH): # 64 is width of the image
        player.x += player.velocity
    redrawGameWindow()
pygame.quit()
