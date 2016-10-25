from tkinter import *
import random
import time
import sys
#import pygame
#import winsound
#winsound.PlaySound("scottysoundtrack.wav",winsound.SND_ASYNC)




################################################################################# "PLAYER" #########################################################################
def findPacman():
    grid = canvas.data.grid
    rows = len(grid)
    cols = len(grid[0])
    for row in range(rows):
        for col in range(cols):
            if (grid[row][col] == "P"):
                return (row, col)

            

def movePacman(drow, dcol):
    grid = canvas.data.grid
    rows = len(grid)
    cols = len(grid[0])
    (row0,col0) = findPacman()
    (row1,col1) = (row0+drow, col0+dcol)
    target1 = grid[row1][col1]
    
    if (target1 == "%"):
        canvas.data.gameOverMessage == "Cannot move through wall!!"
        
        
    elif (target1 == "."):
        # move to a blank
        grid[row0][col0] = "b"
        grid[row1][col1] = "P"
        canvas.data.points += 1
        flag = True
        canvas.data.gameOverMessage = " "
        
    #when the pacman moves to a blank space           
    elif (target1 == "b"):
        # move to a blank
        grid[row0][col0] = "b"
        grid[row1][col1] = "P"
        flag = True
        canvas.data.gameOverMessage = " "

    #when pacman hits a worm
    elif (target1 == "G"):
        canvas.data.gameOverMessage = ""
        canvas.data.mode = "GameOver"
        winsound.PlaySound("gameover.wav",winsound.SND_ASYNC)

       
    else:
        print ("Cannot Move :-P")# should never happen
##################################################################################### "BAD GUYS" #############################################################################
def findWorm(): 
    grid = canvas.data.grid
    rows = len(grid)
    cols = len(grid[0])
    l =[]
    for row in range(rows):
        for col in range(cols):
            if (grid[row][col] == "G"):
                l+=[(row, col)]
    return l

def saveHighscore(text): 
    fileHandler = open("highscores.txt", "a") # open the file in append mode
    fileHandler.write(text) # write the text
    fileHandler.close() # close the file
    

def moveWorm(drow, dcol):
    grid = canvas.data.grid
    rows = len(grid)
    cols = len(grid[0])
    l = findWorm()
    #(row0,col0) = findBaddy()

    for (row0,col0) in l:
        (row1,col1) = (row0+drow, col0+dcol)
        target1 = grid[row1][col1]
        if (target1 == "%"): pass
            
        elif (target1 == "."):#when the worms move to a point location
            # move to a blank
            
            grid[row0][col0] = "."
            grid[row1][col1] = "G"
         
            
        elif (target1 == "b"):#when the worms move to a blank
            # move to a blank
            
            grid[row0][col0] = "b"
            grid[row1][col1] = "G"


        elif (target1 == "P"):
            canvas.data.gameOverMessage = ""
            canvas.data.mode = "GameOver"
            winsound.PlaySound("gameover.wav",winsound.SND_ASYNC)

        else: pass

    redrawAll()
############################################################################### CONTROLLERS ############################################################################################
def keyPressed(event):
    if canvas.data.mode == "background":
        if (event.keysym == "Left"):
            if (canvas.data.tracker == 0 or canvas.data.tracker == 1 or canvas.data.tracker == 2 or canvas.data.tracker == 3):
                canvas.data.tracker =  1
                canvas.data.pacman = canvas.data.pacmanleft

        elif (event.keysym == "Right"):
            if (canvas.data.tracker == 0 or canvas.data.tracker == 1 or canvas.data.tracker == 2 or canvas.data.tracker == 3):
                canvas.data.tracker = 0
                canvas.data.pacman = canvas.data.pacmanright
        elif (event.keysym == "Up"):
            if (canvas.data.tracker == 0 or canvas.data.tracker == 1 or canvas.data.tracker == 2 or canvas.data.tracker == 3):
                canvas.data.tracker = 3
                canvas.data.pacman = canvas.data.pacmanup
                
        elif (event.keysym == "Down"):
            if (canvas.data.tracker == 0 or canvas.data.tracker == 1 or canvas.data.tracker == 2 or canvas.data.tracker == 3):
                canvas.data.tracker = 2
                canvas.data.pacman = canvas.data.pacmandown
    redrawAll()


def mousePressed(event):
    # event.x and event.y contain the coordinates of the mouse click
    #if canvas.data.mode == "game over":
    if canvas.data.mode == "menu":
        if (300 < event.x < 480) and (185 < event.y < 225):
            canvas.data.mode = "background"
        elif ( 490 < event.x < 665) and (185 < event.y < 225):
            canvas.data.mode = "instructions"
      
            
    if canvas.data.mode == "instructions":
        if (750 < event.x < 890) and (670 < event.y <710):
            canvas.data.mode = "menu"
    if canvas.data.mode == "background":
        if (750 < event.x < 890) and (670 < event.y <710):
            canvas.data.mode = "menu"
            init()
    if canvas.data.mode == "scores":
        if (750 < event.x < 890) and (670 < event.y <710):
            canvas.data.mode = "menu"
    if canvas.data.mode == "GameOver":
        if (750 < event.x < 890) and (670 < event.y <710):
            canvas.data.mode = "menu"
            winsound.PlaySound("scottysoundtrack.wav",winsound.SND_ASYNC)
            canvas.data.gameOverMessage = ""
        if (400 <event.x<500) and (150 <event.y<200):
            canvas.data.mode = "background"
                
    redrawAll()

def timerFired(previousTime):
    currentTime = time.time()
    # time passed since the last execution of the timer
    dt = currentTime - previousTime
    #The movement of the front pacman
    if canvas.data.x > 900 - 100: # right wall
        canvas.data.vx = -canvas.data.vx
        canvas.data.x = 900 - 100 # anti stuck
        canvas.data.b = True
    elif canvas.data.x < 10: # left wall
        canvas.data.vx = -canvas.data.vx
        canvas.data.x = 10 # anti stuck
        canvas.data.b = False 
    canvas.data.x += canvas.data.vx * dt
    #the background
    if canvas.data.mode == "background":
        l = [(0,-1),(0,+1),(-1,0),(+1,0)]
       # for i in range(5):
        (x, y) = random.choice(l)
        
        moveWorm(x,y)


    
##for automated movement of player:
    if canvas.data.mode == "background":
        if (canvas.data.tracker == 0):
                movePacman(0, +1)
        elif (canvas.data.tracker == 1):
                movePacman(0, -1)
        elif (canvas.data.tracker == 2):
                movePacman(+1, 0)
        elif (canvas.data.tracker == 3):
                movePacman(-1, 0)
            ################


            
    if canvas.data.points ==canvas.data.foodCount  and canvas.data.level == 1:
        
        canvas.data.tracker = 0
        canvas.data.pacman = canvas.data.pacmanright       
        canvas.data.points = 0
        canvas.data.level = 2
        canvas.data.flag=True


        gameGrid()
       
    elif canvas.data.points == canvas.data.foodCount and canvas.data.level == 2:
        
        canvas.data.tracker = 0
        canvas.data.pacman = canvas.data.pacmanright       
        canvas.data.level = 3
        canvas.data.points = 0
        canvas.data.flag=True



    elif canvas.data.points == canvas.data.foodCount and canvas.data.level == 3: #latestLevel very hard to win, so far no one did
        
        canvas.data.tracker = 0
        canvas.data.pacman = canvas.data.pacmanright       
        canvas.data.level = 0
        canvas.data.points = 0
        canvas.data.flag=True
        canvas.data.flag2=True

        
        gameGrid()
         
    # update the view
    redrawAll()
    # schedule the next call to timerFired
    canvas.after(150, timerFired, currentTime)

def countFood():
    g = canvas.data.grid
    count = 0
    for row in g:
        for thing in row:
            if thing == ".":
                count += 1
    return count
    
#################################################### GRID AND GRID DRAWING ###############################################################
def gameGrid():

    if canvas.data.level == 1:
        canvas.data.grid = [
  ["%","%","%","%","%","%","%","%","%","%","%","%","%","%","%","%","%","%","%","%","%","%","%","%","%","%","%","%","%","%","%"],
  ["%",".",".",".",".",".","%",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".","%",".",".",".",".",".","%"],
  ["%","%","%","%","%",".","%",".","%","%","%",".","%","%","%","%","%","%","%",".","%","%","%",".","%",".","%","%","%","%","%"],
  ["%",".","%",".",".","G",".",".","%",".",".",".",".",".",".","%",".",".",".",".",".",".","%",".",".","G",".",".","%",".","%"],
  ["%",".",".",".","%","%","%",".","%",".","%","%","%","%",".","%",".","%","%","%","%",".","%",".","%","%","%",".",".",".","%"],
  ["%","%","%",".","%",".",".",".","%",".","%",".",".",".",".",".",".",".",".",".","%",".","%",".",".",".","%",".","%","%","%"],
  ["%",".",".",".","%",".","%","%","%",".","%",".","%","%","%","%","%","%","%",".","%",".","%","%","%",".","%",".",".",".","%"],
  ["%",".","%","%","%",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".","G","%","%","%",".","%"],
  ["%",".",".",".","%",".","%","%","%",".","%",".","%","%","%","%","%","%","%",".","%",".","%","%","%",".","%",".",".",".","%"],
  ["%","%","%",".","%",".",".",".","%",".","%",".",".",".",".",".",".",".",".",".","%",".","%",".",".",".","%",".","%","%","%"],
  ["%",".",".",".","%","%","%",".","%",".","%","%","%","%",".","%",".","%","%","%","%",".","%",".","%","%","%",".",".",".","%"],
  ["%",".","%",".",".",".",".",".","%",".",".",".",".",".",".","%",".",".",".",".",".",".","%",".",".",".",".",".","%",".","%"],
  ["%","%","%","%","%",".","%",".","%","%","%",".","%","%","%","%","%","%","%",".","%","%","%",".","%",".","%","%","%","%","%"],
  ["%",".",".",".",".",".","%",".",".",".",".",".",".",".",".","P",".",".",".",".",".",".",".",".","%",".",".",".",".",".","%"],
  ["%","%","%","%","%","%","%","%","%","%","%","%","%","%","%","%","%","%","%","%","%","%","%","%","%","%","%","%","%","%","%"]]
        

    elif canvas.data.level == 2:
        canvas.data.grid = [
  ["%","%","%","%","%","%","%","%","%","%","%","%","%","%","%","%","%","%","%","%","%","%","%","%","%","%","%","%","%","%","%"],
  ["%",".",".",".",".",".","%",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".","%",".",".",".",".",".","%"],
  ["%","%","%","%","%",".","%",".","%","%","%",".","%","%","%","%","%","%","%",".","%","%","%",".","%",".","%","%","%","%","%"],
  ["%",".","%",".",".","G",".",".","%",".",".",".",".",".",".","%",".",".",".",".",".",".","%",".",".","G",".",".","%",".","%"],
  ["%",".",".",".","%","%","%",".","%",".","%","%","%","%",".","%",".","%","%","%","%",".","%",".","%","%","%",".",".",".","%"],
  ["%","%","%",".","%",".",".",".","%",".","%",".",".",".",".",".",".",".",".",".","%",".","%",".",".",".","%",".","%","%","%"],
  ["%",".",".",".","%",".","%","%","%",".","%",".","%","%","%","%","%","%","%",".","%",".","%","%","%",".","%",".",".",".","%"],
  ["%",".","%","%","%","G",".",".",".",".",".",".",".",".",".","G",".",".",".",".",".",".",".",".",".","G","%","%","%",".","%"],
  ["%",".",".",".","%",".","%","%","%",".","%",".","%","%","%","%","%","%","%",".","%",".","%","%","%",".","%",".",".",".","%"],
  ["%","%","%",".","%",".",".",".","%",".","%",".",".",".",".",".",".",".",".",".","%",".","%",".",".",".","%",".","%","%","%"],
  ["%",".",".",".","%","%","%",".","%",".","%","%","%","%",".","%",".","%","%","%","%",".","%",".","%","%","%",".",".",".","%"],
  ["%",".","%",".",".",".",".",".","%",".",".",".",".",".",".","%",".",".",".",".",".",".","%",".",".",".",".",".","%",".","%"],
  ["%","%","%","%","%",".","%",".","%","%","%",".","%","%","%","%","%","%","%",".","%","%","%",".","%",".","%","%","%","%","%"],
  ["%",".",".",".",".",".","%",".",".",".",".",".",".",".",".","P",".",".",".",".",".",".",".",".","%",".",".",".",".",".","%"],
  ["%","%","%","%","%","%","%","%","%","%","%","%","%","%","%","%","%","%","%","%","%","%","%","%","%","%","%","%","%","%","%"]]


    elif canvas.data.level == 3:
        canvas.data.grid = [
  ["%","%","%","%","%","%","%","%","%","%","%","%","%","%","%","%","%","%","%","%","%","%","%","%","%","%","%","%","%","%","%"],
  ["%",".",".",".",".",".","%",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".","%",".",".",".",".",".","%"],
  ["%","%","%","%","%",".","%",".","%","%","%",".","%","%","%","%","%","%","%",".","%","%","%",".","%",".","%","%","%","%","%"],
  ["%",".","%",".",".","G",".",".","%",".",".",".",".",".",".","%",".",".",".",".",".",".","%",".",".","G",".",".","%",".","%"],
  ["%",".",".",".","%","%","%",".","%",".","%","%","%","%",".","%",".","%","%","%","%",".","%",".","%","%","%",".",".",".","%"],
  ["%","%","%",".","%",".",".",".","%",".","%",".",".",".",".",".",".",".",".",".","%",".","%",".",".",".","%",".","%","%","%"],
  ["%",".",".",".","%",".","%","%","%",".","%",".","%","%","%","%","%","%","%",".","%",".","%","%","%",".","%",".",".",".","%"],
  ["%",".","%","%","%","G",".",".",".",".",".",".",".",".",".","G",".",".",".",".",".",".",".",".",".","G","%","%","%",".","%"],
  ["%",".",".",".","%",".","%","%","%",".","%",".","%","%","%","%","%","%","%",".","%",".","%","%","%",".","%",".",".",".","%"],
  ["%","%","%",".","%",".",".",".","%",".","%",".",".",".",".",".",".",".",".",".","%",".","%",".",".",".","%",".","%","%","%"],
  ["%",".",".",".","%","%","%",".","%",".","%","%","%","%",".","%",".","%","%","%","%",".","%",".","%","%","%",".",".",".","%"],
  ["%",".","%",".",".","G",".",".","%",".",".",".",".",".",".","%",".",".",".",".",".",".","%",".",".","G",".",".","%",".","%"],
  ["%","%","%","%","%",".","%",".","%","%","%",".","%","%","%","%","%","%","%",".","%","%","%",".","%",".","%","%","%","%","%"],
  ["%",".",".",".",".",".","%",".",".",".",".",".",".",".",".","P",".",".",".",".",".",".",".",".","%",".",".",".",".",".","%"],
  ["%","%","%","%","%","%","%","%","%","%","%","%","%","%","%","%","%","%","%","%","%","%","%","%","%","%","%","%","%","%","%"]]



    

  

    return canvas.data.grid
  
def drawCellBackground(piece, left, top, right, bottom):
    color = None 
    if (piece == "."):
        color = "black" # outside
    elif (piece == "%"):
        color = "#9a0000" # wall
    elif (piece == "G"):
        color = "#0B9E06" # inside
    elif (piece == 'P'):
        color = "black"
    elif (piece == "b"):
        color = "black"
        
    canvas.create_rectangle(left, top, right, bottom, fill=color, outline="")

def drawCellForeground(piece, left, top, right, bottom, row, col):
    color = None

    
    if (piece == "."):
        canvas.create_oval(left+12, top+12, right-12, bottom-12, fill="yellow")
        
    elif piece == "P":
        canvas.create_oval(left, top, right, bottom, outline="black", width= 3, fill="yellow")
        canvas.create_image(col*30, row*30,image=canvas.data.pacman, anchor=NW)

    elif piece == "G":
        canvas.create_image(col*30, row*30,image=canvas.data.worm, anchor=NW)

   
def drawCell(row, col):
    grid = canvas.data.grid
    rows = len(grid)
    cols = len(grid[0])
    cellSize = 30
    piece = grid[row][col]
    left = cellSize * col
    right = left + cellSize
    top = cellSize * row
    bottom = top + cellSize
    drawCellBackground(piece, left, top, right, bottom)
    drawCellForeground(piece, left, top, right, bottom, row, col)


 ############################################### VIEW ################################################################################   
def redrawAll():
    canvas.delete(ALL)
    
    if canvas.data.mode == "menu":
        canvas.create_image(0,0,image=canvas.data.menu, anchor=NW)
        if canvas.data.b == False:
            canvas.create_image(canvas.data.x, canvas.data.y, image=canvas.data.photo, anchor=NW)
        else:
            canvas.create_image(canvas.data.x, canvas.data.y, image=canvas.data.photo1, anchor=NW)
    elif canvas.data.mode == "instructions":
        canvas.create_image(0,0,image=canvas.data.instructions, anchor=NW)
    elif canvas.data.mode == "scores":
        canvas.create_image(0,0,image=canvas.data.scores, anchor=NW)
    elif canvas.data.mode == "background":
        canvas.create_image(0,0,image=canvas.data.photobackground, anchor=NW)
        
       
            
    
    # draw the grid, cell by cell
        grid = canvas.data.grid
        rows = len(grid)
        cols = len(grid[0])
     #   canvas.data.points = 0
        for row in range(rows):
            for col in range(cols):
                drawCell(row, col)

#score box
        canvas.create_rectangle(50, 475, 200, 520, fill = "#9a0000", outline= "black", width= 5)
        if (canvas.data.flag==True):
            canvas.create_image(520,380,image=canvas.data.nextLevel)
            canvas.create_text(520, 650, text="Next Level" + str(canvas.data.level), font=("Helvetica", 40), fill ="white")

 
            canvas.data.flag=False

        if canvas.data.flag2 == True:
            canvas.create_image(520,380,image=canvas.data.win)
            canvas.create_text(520, 650, text="You Win!!!!" , font=("Helvetica", 40), fill ="white")
            canvas.create_image(520,380,image=canvas.data.win)
            init()
            
            
##
       
        canvas.create_text(120, 500, text="Score: " + str(canvas.data.points), font=("Helvetica", 20), fill ="black")

   
        
    elif canvas.data.mode == "GameOver":
 
        canvas.create_image(0,0,image=canvas.data.photobackground, anchor=NW)
      
        canvas.data.points = 0
        
        canvas.data.grid = gameGrid()
        grid = canvas.data.grid
        rows = len(grid)
        cols = len(grid[0])

        for row in range(rows):
            for col in range(cols):
                drawCell(row, col)
        canvas.create_image(420,180,image=canvas.data.gameover)
        canvas.data.pacman = canvas.data.pacmanright

        
           
#Message:
    msg = canvas.data.gameOverMessage
    if (msg != ""):
        canvas.create_text(400, 520, text=msg, font=("Helvetica", 25), fill ="Blue")
  

        
#################################################### MODEL #################################################################
def init():
      ###BACKGROUND
    canvas.data.mode = "menu"
    canvas.data.photobackground = PhotoImage(file="background.pbm")
    canvas.data.instructions = PhotoImage(file="Instructions.pbm")
    canvas.data.menu = PhotoImage(file="MENU.pbm")
    canvas.data.scores = PhotoImage(file="scores.pbm")
    canvas.data.gameover = PhotoImage(file="Game Over.pbm")
    canvas.data.nextLevel = PhotoImage(file="win.pbm")
    canvas.data.win = PhotoImage(file="win.pbm")
    canvas.data.points = 0
    canvas.data.worm = PhotoImage(file="worm.pbm")
    canvas.data.pacmanleft = PhotoImage(file="pacmanleft.pbm")
    canvas.data.pacmanright= PhotoImage(file="pacmanright.pbm")
    canvas.data.pacmanup = PhotoImage(file="pacmanup.pbm")
    canvas.data.pacmandown = PhotoImage(file="pacmandown.pbm")
    canvas.data.pacman = canvas.data.pacmanright
    
#    canvas.data.trackGame = 0
    canvas.data.level = 1
    
    # make the main grid 
    canvas.data.grid = gameGrid()
    canvas.data.foodCount = countFood()

    #Messages:
    canvas.data.gameOverMessage = "" # so game is not over!

    #tracker
    canvas.data.tracker = 0
    canvas.data.flag=False
    canvas.data.flag2=False


    
    #The moving pacman for the frontpage
    canvas.data.x=10
    canvas.data.y=650
    canvas.data.photo = PhotoImage(file="Pacman 02.gif")
    canvas.data.photo1 = PhotoImage(file="Pacman 03.gif")
    canvas.data.vx = 150
    canvas.data.b = False





def run():
    # create root and canvas
    global canvas
    root = Tk()
    canvas = Canvas(root, width=920, height=900)
    canvas.pack()
    # store canvas in root and canvas itself
    root.canvas = canvas.canvas = canvas
    # set up a structure to store the model
    class MyModel: pass
    canvas.data = MyModel()
    init()
    # set up events
    root.bind("<Key>", keyPressed)
    root.bind("<Button-1>", mousePressed)
    timerFired(time.time())
    # start the main loop
    root.mainloop()

run()

