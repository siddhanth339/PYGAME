import pygame
import math
import random

wordlist = ["PROGRAMMER", "IDE", "LANGUAGE", "DEBUG", "RUN", "LOAD", "CSE", "COMPUTER", "GPU", "THREAD", "DATA", "ALGORITHMS", "JAVA", "PYTHON"]
    
# setup display
pygame.init()
WIDTH, HEIGHT = 800, 500
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("HANGMAN GAME!!")

# button variables
RADIUS = 20
GAP = 15

# fonts
LETTER_FONT = pygame.font.SysFont('comicsans', 40)
WORD_FONT = pygame.font.SysFont('comicsans', 60)
TITLE_FONT = pygame.font.SysFont('comicsans', 70)

# load images
images = []
for i in range(7):
    image = pygame.image.load("hangman" + str(i) + ".png")
    images.append(image)
    

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
   
letters = []

# game variables
hangman_status = 0 # image no.
word = random.choice(wordlist)
guessed = []


# setup game loop
FPS = 60
clock = pygame.time.Clock()
run = True

def init():
    # game variables
    global hangman_status
    global word
    global guessed
    global letters 
    
    hangman_status = 0 # image no.
    word = random.choice(wordlist)
    guessed = []
    letters = []

    # positioning the buttons
    startx = 70
    starty = 400
    ASCII_VAL = 65
    letters.append([startx, starty, chr(ASCII_VAL), True]) # for the first circle in first row, the bool True is to make the button visible or invisible
    ASCII_VAL += 1 # because the for loop below is going to start append for the letter B
    for i in range(12):
        x = startx + (GAP + 2 * RADIUS)
        startx = x
        letters.append([x, starty, chr(ASCII_VAL), True])
        ASCII_VAL += 1
        
    startx = 70
    starty = 400 + (GAP + 2 * RADIUS)
    letters.append([startx, starty, chr(ASCII_VAL), True]) # for the first circle in second row
    ASCII_VAL += 1
    for i in range(12):
        x = startx + (GAP + 2 * RADIUS)
        startx = x
        letters.append([x, starty, chr(ASCII_VAL), True])
        ASCII_VAL += 1


def draw():
    win.fill(WHITE)
    # draw title
    text = TITLE_FONT.render("HANGMAN", 1, BLACK)
    win.blit(text, (WIDTH/2 - text.get_width()/2, 20))
    
    # draw word
    display_word = ""
    for w in word:
        if(w in guessed):
            display_word += w + " "
        else:
            display_word += "_ "
    text = WORD_FONT.render(display_word, 1, BLACK)
    win.blit(text, (400, 200))
    
    # draw buttons
    for letter in letters:
        x, y, ltr, visible = letter
        if(visible):
            pygame.draw.circle(win, BLACK, (x, y), RADIUS, 3) # here the last parameter "3" is the thickness of the circumference
            text = LETTER_FONT.render(ltr, 1, BLACK) # ??????
            win.blit(text, (x - text.get_width()/2, y - text.get_height()/2))
        
    win.blit(images[hangman_status], (150, 100)) # draw images[hangman_status] image at (150, 100) position
    pygame.display.update()

# display the result at the end of the game 
def display_result(message):
    win.fill(WHITE)
    text = WORD_FONT.render(message, 1, BLACK)
    win.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2))
    pygame.display.update()
    
def ShowAns():
    win.fill(WHITE)
    text = WORD_FONT.render("ANSWER: " + word, 1, BLACK)
    win.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2))
    pygame.display.update()
    
init() # initialize set pos of buttons etc...
while (run):
    clock.tick(FPS)

    draw()

    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            run = False
        if(event.type == pygame.MOUSEBUTTONDOWN):
            m_x, m_y = pygame.mouse.get_pos()
            for letter in letters:
                x, y, ltr, visible = letter
                if(visible):
                    dis = math.sqrt((x - m_x)**2 + (y - m_y)**2)
                    if (dis < RADIUS):
                        letter[3] = False
                        guessed.append(ltr)
                        if(ltr not in word):
                            hangman_status += 1
                    
                            
    won = True
    for letter in word:
        if(letter not in guessed):
            won = False
            break

        
    if(won == True):
        draw() # to update the window with the last input
        pygame.time.delay(1000)
        display_result("YOU WON!!!")
        pygame.time.delay(3000)
        init()
    
    if(hangman_status == 6): # you make it to the last pic
        draw() 
        pygame.time.delay(1000)
        display_result("YOU LOST :(")
        pygame.time.delay(3000)
        ShowAns()
        pygame.time.delay(3000)
        init()
        
pygame.quit()