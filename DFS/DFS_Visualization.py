import pygame
import time
SCREEN_WIDTH = 600
win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_WIDTH))
pygame.display.set_caption("Path finding using BFS")

RED = (255, 0, 0) # visited
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255) # not visited
BLACK = (0, 0, 0) # barrier
pathColor = [128, 0, 128] # purple
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class Spot:
    def __init__(self, row, col, width):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        
    def get_pos(self):
        return self.row, self.col
    
    def is_barrier(self):
        return self.color == BLACK
    
    def is_start(self):
        return self.color == ORANGE
    
    def is_end(self):
        return self.color == TURQUOISE
    
    def reset(self):
        self.color = WHITE
    
    def make_barrier(self):
        self.color = BLACK   
        
    def make_start(self):
        self.color = ORANGE
        
    def make_end(self):
        self.color = TURQUOISE    
        
    def draw(self):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))
    
    def update_neighbors(self, grid):
        self.neighbors = []
        if (self.col + 1 < ROWS and not grid[self.row][self.col + 1].is_barrier()): # CHECK if there is a barrier on RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])
            
        if (self.row + 1 < ROWS and not grid[self.row + 1][self.col].is_barrier()): # CHECK if there is a barrier DOWN
            self.neighbors.append(grid[self.row + 1][self.col])
    
        if (self.col - 1 >= 0 and not grid[self.row][self.col - 1].is_barrier()): # CHECK if there is a barrier on LEFT
            self.neighbors.append(grid[self.row][self.col - 1])
    
        if (self.row - 1 >= 0 and not grid[self.row - 1][self.col].is_barrier()): # CHECK if there is a barrier UP
            self.neighbors.append(grid[self.row - 1][self.col])


def make_grid(rows, width):
    grid = []
    box_width = width // rows # width of each small box in the grid
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, box_width)
            grid[i].append(spot)
    
    return grid

def draw_grid(): # draw lines
    box_width = SCREEN_WIDTH // ROWS
    for i in range(ROWS):
        pygame.draw.line(win, GREY, (0, i * box_width), (SCREEN_WIDTH, i * box_width))
    
    for i in range(ROWS):
        pygame.draw.line(win, GREY, (i * box_width, 0), (i * box_width, SCREEN_WIDTH))
    
   
def draw(grid):
    win.fill(WHITE)
    for row in grid: 
        for spot in row:
            spot.draw()
            
    draw_grid()
    
    pygame.display.update()
    
    
def get_clicked_pos(pos):
    box_width = SCREEN_WIDTH // ROWS
    y, x = pos
    row = y // box_width
    col = x // box_width
    return row, col

def visualize(path):
    
    for i in path:
        pygame.event.pump()
        if (i != path[0]):
            pygame.draw.rect(win, pathColor, (i[0] * 60, i[1] * 60, 60, 60))
            draw_grid()
            pygame.display.update()
            time.sleep(0.25)
            
    # reset
    for i in path:
        pygame.event.pump()
        if (i != path[0]):
            pygame.draw.rect(win, WHITE, (i[0] * 60, i[1] * 60, 60, 60))
            draw_grid()
            pygame.display.update()
            time.sleep(0.25)
        
def DFS(grid, start, end):
    path.append([start.row, start.col])
    
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            pygame.quit()
        
    if (start == end):
        visualize(path)
        end.make_end()
        end.draw()
        draw_grid()
        pygame.display.update()
        del path[-1]
        return 
    
    visited[start.row][start.col] = True
    
    for neighbor in start.neighbors:
        if (visited[neighbor.row][neighbor.col] == False):
            DFS(grid, neighbor, end)
          
    visited[start.row][start.col] = False
    del path[-1]       
    
ROWS = 10
grid = make_grid(ROWS, SCREEN_WIDTH)
path = []

start = None
end = None

run = True
started = False

visited = []

for i in range(len(grid)):
    visited.append([])
    for j in range(len(grid[0])):
        visited[i].append(False)
        
while run:
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            run = False
            
        if (started): # if algorithm has started, then don't allow the user to press any key other than the quit (X) button
            continue
        
        if (pygame.mouse.get_pressed()[0]): # pressed the left mouse button
            pos = pygame.mouse.get_pos()
            row, col = get_clicked_pos(pos)
            spot = grid[row][col]
            
            if not start and spot != end: # assign start 
                start = spot
                start.make_start()
            
            elif not end and spot != start: # assign end
                end = spot
                end.make_end()
                
            elif spot != end and spot != start: # make barrier
                spot.make_barrier()
                
        if (pygame.mouse.get_pressed()[2]): # pressed the right mouse button
            pos = pygame.mouse.get_pos()
            row, col = get_clicked_pos(pos)
            spot = grid[row][col]
            spot.reset()
            
            if (spot == start):
                start = None
            elif (spot == end):
                end = None
            
        if (event.type == pygame.KEYDOWN):
            """
            when a key is pressed and that key is the spacebar
            and the algorithm has not been started yet then ADD THE EDGES
            """
            if (event.key == pygame.K_SPACE and not started): # assign edges
                for row in grid:
                    for spot in row:
                        spot.update_neighbors(grid)

                DFS(grid, start, end)
                                
                start = None
                end = None
                for row in grid: 
                    for spot in row:
                        spot.reset()
    draw(grid)
    
pygame.quit()

