import time
def valid(board, num, pos):
    # check row
    for i in range(len(board.cubes[0])):
        if(board.cubes[pos[0]][i].value == num and i != pos[1]):
            return False
    # check column
    for i in range(len(board.cubes)):
        if(board.cubes[i][pos[1]].value == num and i != pos[0]):
            return False
    # check box
    x = pos[0]//3
    y = pos[1]//3
    for i in range(x*3, x*3 + 3):
        for j in range(y*3, y*3 + 3):
            if(board.cubes[i][j].value == num and (i, j) != pos):
                return False
    return True
            
def print_board(board):
    for i in range(len(board.cubes)):
        if(i % 3 == 0 and i != 0):
            print("---------------------")
        for j in range(len(board.cubes[0])):
            if(j % 3 == 0 and j != 0):
                print("|", end = " ")
            print(board.cubes[i][j].value, end = " ")
        print()
            
def find_empty(board):
    for i in range(len(board.cubes)):
        for j in range(len(board.cubes[0])):
            if(board.cubes[i][j].value == 0):
                return (i, j)

def solve(board):
    time.sleep(0.25)
    find = find_empty(board)
    if (find == None):
        return True
    
    row, col = find
    for i in range(1, 10):
        board.cubes[row][col].value = i
        board.select((col, row))
        board.ReDraw(0)
        
        if valid(board, i, (row, col)):
            board.cubes[row][col].value = i
            board.ReDraw(0)
            if solve(board):
                return True
            board.select((col, row))            
            board.cubes[row][col].value = 0
        else:
            board.cubes[row][col].value = 0
        time.sleep(0.25)

    return False
