import pygame

pygame.init()

# screen dimensions
SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 600

#colors 
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREY = (169, 169, 169)
SILVER = (192, 192, 192)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 69, 0)
PINK = (255, 0, 255)
VIOLET = (138, 43, 226)

# coordinates of boxes containing colors
WHITEBOX = (1230, 290)
BLACKBOX = (1265, 290)
REDBOX = (1300, 290)
BLUEBOX = (1230, 325)
GREENBOX = (1265, 325)
YELLOWBOX = (1300, 325)
ORANGEBOX = (1230, 360)
PINKBOX = (1265, 360)
VIOLETBOX = (1300, 360)

# images
icon = pygame.image.load('paint.png') # the logo at the top left corner
eraserImg = pygame.image.load('eraser.png')

win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("PAINT")
pygame.display.set_icon(icon)

# font
font = pygame.font.SysFont('comicsans', 50)
Numberfont = pygame.font.SysFont('comicsans', 40)
run = True

clock = pygame.time.Clock()


win.fill(WHITE)
pygame.display.update()


def save():
    pygame.image.save(win, "screenshot.jpeg")

    
def drawColorPalette():
    
    pygame.draw.rect(win, SILVER, (sidePanelX + 10, 210, 270, 200))
    text = font.render("COLORS:", 1, BLACK)
    win.blit(text, (sidePanelX + 30, 230))
    
    for i in range(4):
        pygame.draw.line(win, BLACK, (colorPalette[0], colorPalette[1] + i * 35), (colorPalette[0] + 105, colorPalette[1] + i * 35))
    
    for i in range(4):
        pygame.draw.line(win, BLACK, (colorPalette[0] + i * 35, colorPalette[1]), (colorPalette[0] + i * 35, colorPalette[1] + 105))
     
    pygame.draw.rect(win, WHITE, (WHITEBOX[0], WHITEBOX[1], 35, 35))
    pygame.draw.rect(win, BLACK, (BLACKBOX[0], BLACKBOX[1], 35, 35))
    pygame.draw.rect(win, RED, (REDBOX[0], REDBOX[1], 35, 35))
    pygame.draw.rect(win, BLUE, (BLUEBOX[0], BLUEBOX[1], 35, 35))
    pygame.draw.rect(win, GREEN, (GREENBOX[0], GREENBOX[1], 35, 35))
    pygame.draw.rect(win, YELLOW, (YELLOWBOX[0], YELLOWBOX[1], 35, 35))
    pygame.draw.rect(win, ORANGE, (ORANGEBOX[0], ORANGEBOX[1], 35, 35))
    pygame.draw.rect(win, PINK, (PINKBOX[0], PINKBOX[1], 35, 35))
    pygame.draw.rect(win, VIOLET, (VIOLETBOX[0], VIOLETBOX[1], 35, 35))
 

def redrawWindow():

    # draw multiple lines between points (to avoid discontinuous lines)
    
    keys = pygame.mouse.get_pressed()
    if (keys[0]): # check if the left mouse button is pressed
        
        mouse_pos = pygame.mouse.get_pos()
        dots.append(mouse_pos)
        pygame.draw.lines(win, COLOR, False, dots, THICKNESS)  # use this, much more efficient than drawing every line between the points
        # keep closed(the third parameter above) as False
    
    pygame.draw.line(win, BLACK, (sidePanelX, 0), (sidePanelX, SCREEN_HEIGHT), 5)
    win.fill(GREY, (SCREEN_WIDTH-300, 0, 300, SCREEN_HEIGHT))
    
    # render the size options
    pygame.draw.rect(win, SILVER, (sidePanelX + 10, 10, 270, 80))
    
    text = font.render("SIZE:", 1, BLACK)
    win.blit(text, (sidePanelX + 30, 30))
    
    pygame.draw.rect(win, BLACK, (size1[0], size1[1], 35, 35), 1)
    one = Numberfont.render("1", 1, BLACK)
    win.blit(one, (size1[0] + one.get_width()//2 + 4, size1[1] + one.get_height()//2 - 10))
    
    pygame.draw.rect(win, BLACK, (size2[0], size2[1], 35, 35), 1)
    two = Numberfont.render("2", 1, BLACK)
    win.blit(two, (size2[0] + two.get_width()//2 + 4, size2[1] + two.get_height()//2 - 10))
    
    pygame.draw.rect(win, BLACK, (size3[0], size3[1], 35, 35), 1)
    three = Numberfont.render("3", 1, BLACK)
    win.blit(three, (size3[0] + three.get_width()//2 + 4, size3[1] + three.get_height()//2 - 10))
    
    # render the erase button
    pygame.draw.rect(win, SILVER, (sidePanelX + 10, 110, 270, 80))
    
    text = font.render("ERASER:", 1, BLACK)
    win.blit(text, (sidePanelX + 30, 130))
    win.blit(eraserImg, (eraser[0] , eraser[1]))
    
    drawColorPalette()
    
    # save button
    pygame.draw.rect(win, SILVER, (sidePanelX + 10, 430, 270, 80))
    text = font.render("SAVE" , 1, BLACK)
    win.blit(text, (sidePanelX + 10 + 270//2 - text.get_width()//2, 430 + 80//2 - text.get_height()//2 ))
    
    pygame.display.update()
        
        
COLOR = BLACK
THICKNESS = 3
dots = []  

sidePanelX = SCREEN_WIDTH-300 # the divider between the drawing area and the tools 
size1 = (sidePanelX + 30 + 91 + 10, 30)
size2 = (sidePanelX + 30 + 91 + 10 + 45, 30)
size3 = (sidePanelX + 30 + 91 + 10 + 90, 30)
eraser = (1408, 130)
colorPalette = (sidePanelX + 30, 290)
SAVEBUTTON = (sidePanelX + 10, 430)

while (run):
    
    clock.tick(240)
    
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            run = False

        if (event.type == pygame.MOUSEBUTTONDOWN):
            x, y = pygame.mouse.get_pos()
            dots = [(x, y)]
            
            if (x > sidePanelX):
                if (x > size1[0] and x < size1[0] + 35 and y > size1[1] and y < size1[1] + 35):
                    THICKNESS = 3
                    
                elif (x > size2[0] and x < size2[0] + 35 and y > size2[1] and y < size2[1] + 35):
                    THICKNESS = 5
                    
                elif (x > size3[0] and x < size3[0] + 35 and y > size3[1] and y < size3[1] + 35):
                    THICKNESS = 10
                    
                elif (x > eraser[0] and x < eraser[0] + 24 and y > eraser[1] and y < eraser[1] + 24):
                    THICKNESS = 50
                    COLOR = WHITE
                
                else:
                    if (x > WHITEBOX[0] and x < WHITEBOX[0] + 35 and y > WHITEBOX[1] and y < WHITEBOX[1] + 35):
                        COLOR = WHITE
                        
                    elif (x > BLACKBOX[0] and x < BLACKBOX[0] + 35 and y > BLACKBOX[1] and y < BLACKBOX[1] + 35):
                        COLOR = BLACK   
                        
                    elif (x > REDBOX[0] and x < REDBOX[0] + 35 and y > REDBOX[1] and y < REDBOX[1] + 35):
                        COLOR = RED                
            
                    elif (x > BLUEBOX[0] and x < BLUEBOX[0] + 35 and y > BLUEBOX[1] and y < BLUEBOX[1] + 35):
                        COLOR = BLUE
                        
                    elif (x > GREENBOX[0] and x < GREENBOX[0] + 35 and y > GREENBOX[1] and y < GREENBOX[1] + 35):
                        COLOR = GREEN
    
                    elif (x > YELLOWBOX[0] and x < YELLOWBOX[0] + 35 and y > YELLOWBOX[1] and y < YELLOWBOX[1] + 35):
                        COLOR = YELLOW    
    
                    elif (x > ORANGEBOX[0] and x < ORANGEBOX[0] + 35 and y > ORANGEBOX[1] and y < ORANGEBOX[1] + 35):
                        COLOR = ORANGE   
    
                    elif (x > PINKBOX[0] and x < PINKBOX[0] + 35 and y > PINKBOX[1] and y < PINKBOX[1] + 35):
                        COLOR = PINK    
    
                    elif (x > VIOLETBOX[0] and x < VIOLETBOX[0] + 35 and y > VIOLETBOX[1] and y < VIOLETBOX[1] + 35):
                        COLOR = VIOLET   
                        
                    elif (x > SAVEBUTTON[0] and x < SAVEBUTTON[0] + 270 and y > SAVEBUTTON[1] and y < SAVEBUTTON[1] + 80):
                        save()   
    
    
    
    redrawWindow()
    
pygame.quit()
