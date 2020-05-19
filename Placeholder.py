# Placeholder
# Concept by Ethan Camba
# Programming by Ryan Flynn
# Made 5 / 17 / 2020

#Determine the number of rows and columns [Min: 4]
r = 0
c = 0
while r < 4 and c < 4:
    i = str(input("What size board would you like [R C]: "))
    i = i.split()
    r = int(i[0])
    c = int(i[1])

#Determine the number of pieces needed in a row to win [Min: 3]
winCon = 0
while winCon >= max(r, c) or winCon < 3:
    i = str(input("Win condition [# > 2]: "))
    winCon = int(i)

#Create the board
board = []
for i in range(r):
    l1 = []
    for j in range(c):
        l1.append('-')
    board.append(l1)

#Determines if someone has won
def win(board, winCon, xCount, oCount):
    lenx = len(board[0])
    leny = len(board)
    
    #Horizontal
    for y in range(leny):
        for x in range(lenx - 2):
            check = 1
            for i in range(winCon - 1):
                if board[y][x + i] != board[y][x + i + 1]:
                    # print("Check failed at", x, y)
                    check = 0
                    break
            if board[y][x] != '-' and check == 1:
                return 1
    
    #Vertical
    for x in range(lenx):
        for y in range(leny - 2):
            check = 1
            for i in range(winCon - 1):
                if board[y + i][x] != board[y + i + 1][x]:
                    check = 0
                    break
            if board[y][x] != '-' and check == 1:
                return 1        

    #Diagonal to Right
    for y in range(leny - 2):
        for x in range(lenx - 2):
            check = 1
            for i in range(winCon - 1):
                if board[y + i][x + i] != board[y + i + 1][x + i + 1]:
                    # print("Check failed at", x, y)
                    check = 0
                    break
            if board[y][x] != '-' and check == 1:
                return 1

    #Diagonal to Left
    for y in range(2, leny):
        for x in range(lenx - 2):
            check = 1
            for i in range(winCon - 1):
                if board[y - i][x + i] != board[y - i - 1][x + i + 1]:
                    # print("Check failed at", x, y)
                    check = 0
                    break
            if board[y][x] != '-' and check == 1:
                return 1     
    return 0

#Print the board
def printB(board):
    print()
    print("   ", end=" ")
    for i in range(len(board[0])):
        print(i, "  ", end=" ")
    print()
    for i in range(len(board)):
        print(i, board[i])
        print()

#Place a piece on the board
def place(board, turn):
    check = 0
    while check == 0:
        i = str(input("Input a location [x y]: "))
        i = i.split()
        x = int(i[0])
        y = int(i[1])
        if validPlace(board, turn, y, x) == 1:
            if turn % 2 == 0:
                board[y][x] = 'X'
            else:
                board[y][x] = 'O'
            check = 1
    return board

#Make a move
def makeMove(board, turn):
    check = 0
    piecex = 0
    piecey = 0
    while check == 0:
        i = str(input("Which piece would you like to move [x y]: "))
        i = i.split()
        piecex = int(i[0])
        piecey = int(i[1])
        if turn % 2 == 0:
            if board[piecey][piecex] == 'X':
                check = 1
        else:
            if board[piecey][piecex] == 'O':
                check = 1
    check = 0
    while check == 0:
        i = str(input("Where do you want to move the piece [x y]: "))
        i = i.split()
        x = int(i[0])
        y = int(i[1])
        if validMove(board, turn, y, x, piecey, piecex) == 1:
            board[piecey][piecex] = '-'
            if turn % 2 == 0:
                board[y][x] = 'X'
                check = 1
            else:
                board[y][x] = 'O'
                check = 1
    return board

#Check if the move was valid
def validMove(board, turn, y, x, piecey, piecex):
    lenx = len(board[0])
    leny = len(board)
    if x > lenx - 1 or x < 0 or y > leny - 1 or y < 0:
        print("Not a valid x or y value")
        return 0
    if board[y][x] != '-':
        print("Empty space")
        return 0
    if abs(y - piecey) > 1 or abs(x - piecex) > 1:
        print("Can't move that far!")
        return 0
    return 1

#Make the piece jump over another piece and remove it
def makeJump(board, turn):
    check = 0
    while check == 0:
        i = str(input("Input your piece and the piece you want to jump [x y x y]: "))
        i = i.split()
        x = int(i[0])
        y = int(i[1])
        rx = int(i[2])
        ry = int(i[3])
        jumpy = ry - (y - ry)
        jumpx = rx - (x - rx)
        if validJump(board, turn, y, x, ry, rx, jumpy, jumpx):
            board[y][x] = '-'
            board[ry][rx] = '-'
            if turn % 2 == 0:
                board[jumpy][jumpx] = 'X'
            else:
                board[jumpy][jumpx] = 'O'
            check = 1
            board = checkForExtraJump(board, turn, jumpy, jumpx)
    return board

#Check if the jump is valid
def validJump(board, turn, y, x, ry, rx, jumpy, jumpx):
    lenx = len(board[0])
    leny = len(board)
    if x > lenx - 1 or x < 0 or y > leny - 1 or y < 0 or rx > lenx - 2 or rx < 1 or ry > leny - 2 or ry < 1:
        print("Not a valid x or y")
        return 0
    if turn % 2 == 0:
        if board[y][x] != 'X' or board[ry][rx] != 'O' or board[jumpy][jumpx] != '-':
            print("Not a valid selection or jump location")
            return 0
    else:
        if board[y][x] != 'O' or board[ry][rx] != 'X' or board[jumpy][jumpx] != '-':
            print("Not a valid selection or jump location")
            return 0  
    if abs(y - ry) > 1 or abs(x - rx) > 1:
        print("Can't jump that far!")
        return 0
    return 1

#Check if the piece can jump AGAIN
def checkForExtraJump(board, turn, y, x):
    s = [[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]
    check = 0
    for i in range(-1, 1):
        for j in range(-1, 1):
            s[(i + 2) * (j + 1)][0] = y + i
            s[(i + 2) * (j + 1)][1] = x + j
    for j in range(len(s)):
        checky = s[j][0]
        checkx = s[j][1]
        if turn % 2 == 0:
            if board[checky][checkx] == 'O':
                jumpy = checky - (y - checky)
                jumpx = checkx - (x - checkx)
                if validJump(board, turn, y, x, checky, checkx, jumpy, jumpx) == 1:
                    check = 1
        else:
            if board[checky][checkx] == 'X':
                jumpy = checky - (y - checky)
                jumpx = checkx - (x - checkx)
                if validJump(board, turn, y, x, checky, checkx, jumpy, jumpx) == 1:
                    check = 1
    if check == 1:
        i = str(input("Would you like to make a jump [x y of piece you are jumping if yes, n if no]: "))
        if i != "no":
            i = i.split()
            rx = int(i[0])
            ry = int(i[1])
            jumpy = ry - (y - ry)
            jumpx = rx - (x - rx)
            if validJump(board, turn, y, x, ry, rx, jumpy, jumpx) == 1:
                board[y][x] = '-'
                board[ry][rx] = '-'
                if turn % 2 == 0:
                    board[jumpy][jumpx] = 'X'
                else:
                    board[jumpy][jumpx] = 'O'
                checkForExtraJump(board, turn, jumpy, jumpx)
    return board

#Check if the place chosen is valid
def validPlace(board, turn, y, x):
    lenx = len(board[0])
    leny = len(board)
    if x > lenx - 1 or x < 0 or y > leny - 1 or y < 0:
        print("Not a valid x or y")
        return 0
    if board[y][x] != '-':
        print("Not an empty space")
        return 0
    return 1

#Count the number of X's on the board
def countX(board):
    count = 0
    for x in range(len(board[0])):
        for y in range(len(board)):
            if (board[x][y] == 'X'):
                count = count + 1
    return count

#Count the number of O's on the board
def countO(board):
    count = 0
    for x in range(len(board[0])):
        for y in range(len(board)):
            if (board[x][y] == 'O'):
                count = count + 1
    return count

#Variable Initialization
turn = 0
end = 0
xCount = 0
oCount = 0

#Play the game
while win(board, winCon, xCount, oCount) == 0 and end != 1:
    printB(board)
    xCount = countX(board)
    oCount = countO(board)
    
    #Who's turn is it?
    if turn % 2 == 0:
        print("X's turn")
    else:
        print("O's turn")
    
    #Player chooses what to do this turn
    c = 'n'
    while c == 'n':
        c = str(input("[p] Place a Piece [m] Move a Piece [j] Jump a Piece [e] End Game: "))
        if turn % 2 == 0:
            if (c == 'm' or c == 'j') and xCount == 0:
                print("You don't have any pieces...")
                c = 'n'
        else:
            if (c == 'm' or c == 'j') and oCount == 0:
                print("You don't have any pieces...")
                c = 'n'
        if c == 'p':
            board = place(board, turn)
        elif c == 'm':
            board = makeMove(board, turn)
        elif c == 'j':
            board = makeJump(board, turn)
        elif c == 'e':
            end = 1
    turn = turn + 1

#When the game is finished
print()
print("Turns:", turn, "Final Board:")   
printB(board)