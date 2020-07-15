import pygame
import random 

pygame.init()

clock = pygame.time.Clock()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 700

win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("P O N G")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GREY = (200, 200, 200)

# Yes!! ball is a rectangle (it is done this way because the ellipse is drawn inside this rectangle)
ball = pygame.Rect(SCREEN_WIDTH //  2 - 15, SCREEN_HEIGHT // 2 - 15, 30, 30)
player = pygame.Rect(SCREEN_WIDTH - 20, SCREEN_HEIGHT // 2 - 70, 10, 140)
opponent = pygame.Rect(10, SCREEN_HEIGHT // 2 - 70, 10, 140)

ball_speed_x = 7
ball_speed_y = 7

font = pygame.font.SysFont('comicsans', 40)

def ball_restart():
    global ball_speed_x, ball_speed_y
    
    ball.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2) # reset the ball to the center of the window
    ball_speed_y *= random.choice((1, -1))
    ball_speed_x *= random.choice((1, -1))
    
def ball_animation():
    
    global ball_speed_x, ball_speed_y, score1, score2
    ball.x += ball_speed_x
    ball.y += ball_speed_y
    
    # collision of ball with the sides of the window
    if (ball.top <= 0 or ball.bottom >= SCREEN_HEIGHT):
        ball_speed_y *= -1

    if (ball.left <= 0 or ball.right >= SCREEN_WIDTH):
        if (ball.left <= 0):
            score2 += 1
        else:
            score1 += 1
        ball_restart()
       
    # collision of ball with the player or opponent
    if (ball.colliderect(player) or ball.colliderect(opponent)):
        ball_speed_x *= -1
        
def redrawGameWindow():
    win.fill(BLACK)       
    pygame.draw.rect(win, LIGHT_GREY, player)
    pygame.draw.rect(win, LIGHT_GREY, opponent)
    pygame.draw.ellipse(win, LIGHT_GREY, ball)
    # draw a SMOOTH LINE using aaline (antialiasing)
    pygame.draw.aaline(win, LIGHT_GREY, (SCREEN_WIDTH//2, 0), (SCREEN_WIDTH//2, SCREEN_HEIGHT))
    
    score = font.render(str(score1), 1, WHITE)
    win.blit(score, (SCREEN_WIDTH//2 - 50, 5))
    score = font.render(str(score2), 1, WHITE)
    win.blit(score, (SCREEN_WIDTH//2 + 35, 5))
    pygame.display.update()
    
run = True
score1 = 0
score2 = 0

while (run):
    
    clock.tick(60)
    
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            run = False
        
    keys = pygame.key.get_pressed()
    
    # moving the player
    if (keys[pygame.K_DOWN]):
        if (player.bottom + 7 < SCREEN_HEIGHT):
            player.y += 7 
            
    if (keys[pygame.K_UP]):
        if (player.top - 7 > 0):
            player.y -= 7
    
    # moving opponent (player 2)
            
    if (keys[pygame.K_s]):
        if (opponent.bottom + 7 < SCREEN_HEIGHT):
            opponent.y += 7
    if (keys[pygame.K_w]):
        if (opponent.top - 7 > 0):
            opponent.y -= 7
            
    ball_animation()
    
    redrawGameWindow()
    
pygame.quit()
