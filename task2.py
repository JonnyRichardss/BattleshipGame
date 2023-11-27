import random,time
#Constants
diffDict = {"Beginner":(9,9,10),"Intermediate":(16,16,40),"Expert":(30,16,99)} #used to simplify calls to CreateBoard()

#Globals
mineList = [] #used for hint feature
totalMines = 0 #used for unflagged mines feature

class Square:
    #Class that stores all the information about squares on the board
    #This is the class that is inside the 2d array
    
    def __init__(self,row,col):
        #basic init, contains default attributes for the class as well as settable board position
        self.isMine = False
        self.isFlagged = False
        self.isHidden = True

        self.cueNumber = 0

        self.row = row
        self.col = col
        
    def GetNeighbours(self,board):
        #Returns every neighbour of a square
        #Inputs:
        #       board: 2d array of the Square class
        #Outputs:
        #       neighbours: 1d array of the Square class, containing every neighbour of the self square
        #board is passed through here to allow a list of squares to be returned rather than a list of coordinates
        
        neighbours = []
        
        for row in range(self.row-1,self.row+2): #iterate over +/- 1 row from the square
            for col in range(self.col-1,self.col+2): #iterate over +/- 1 column from the square
                if row <0 or col <0:
                    continue #stop negative indices wrapping around and causing incorrect cue numbers
                try:
                    neighbours.append(board[row][col]) #append the neighbour to the list
                except IndexError:
                    pass #if the index is off the board, ignore it
                
        neighbours.remove(self)#as the iteration included the original square, remove it
        return(neighbours)
    
    def SetCue(self,board):
        #Sets cue number for a give square
        #Inputs:
        #       board: 2d array of the Square class
        
        #PrintBoard(board,True) debug line
        
        totalMines = 0 #this isn't the global version of this variable, it just counts neighbours
        for neighbour in self.GetNeighbours(board): #gets all neighbours from GetNeighbours and iterates over them
            if neighbour.isMine:
                totalMines +=1 #adds up how many of them are miens

            
        self.cueNumber = totalMines #sets own cue number
        
        
    def OpenCells(self,board):
        #Recursive function to open up cells if a cell without any number is pressed
        #Inputs:
        #       board: 2d array of the Square class
        if self.isMine or self.isFlagged or not self.isHidden:
            return #prevents non-numbered squares being opened and infinite loops
        self.isHidden = False #opens self
        if self.cueNumber == 0:
            for neighbour in self.GetNeighbours(board):
                neighbour.OpenCells(board) #runs the function on all the square's neighbours if it has no number in it
    
    def Open(self,board):
        #Called when the player selects action 0
        #Inputs:
        #       board: 2d array of the Square class
        
        #checking for illegal cases
        if self.isFlagged:
            print("You can't open a flagged square!")
        elif not self.isHidden:
            print("That square is already opened!")
        
        elif self.isMine:
            return(True) #opening a mine will lose the game
        #safe squares start the recursive opening
        else:
            self.OpenCells(board)
    
    def Flag(self,val):
        #called when the player selects actions 1 or 2
        #Inputs:
        #       val: Boolean that determines if the function is being used to flag or unflag
        
        #decides if the function is being used to flag or unflag, sets text for player feedback appropriately
        if val:
            text = "flag"
        else:
            text = "unflag"
        
        #checking for illegal cases
        if not self.isHidden:
            print("You can't %s an opened square!" %(text))
            return(False)           
        elif val == self.isFlagged:
            print("That square is already %sged!" %(text))
            return(False)
        #flag/unflag the square
        else:
            self.isFlagged = val
            return(True)





def CreateBoard(rows,cols,mines):
    #Generates the board for the whole game
    #Inputs:
    #       rows: the number of rows the board should have
    #       cols: the number of columns the board should have
    #       mines: the number of mines to generate
    #Outputs:
    #       returns the board (2d array of the Square class)
    
    #makes the function set the global variables, so they can be accessed later
    global mineList
    global totalMines
    
    board = [[Square(row,col) for col in range(cols)] for row in range(rows)] #initialises the full board of the correct size
    
    #makes a list of every single coordinate on the board, this feels messy but it is a functional way to ensure the randomly squares are all unique (that works on non-square boards)
    fullrange = []
    for i in range(rows):
        for j in range(cols):
            fullrange.append((i,j))
    
    #setting global variables
    mineList = random.sample(fullrange,mines) #randomly picks unique coordinates for the mines
    totalMines = mines
    
    #applying the minesto the board
    for mine in mineList:
        board[mine[0]][mine[1]].isMine = True
    
    #sets cues for the whole board
    for row in range(rows):
        for col in range(cols):
           board[row][col].SetCue(board)
           
    return(board)#finally, return the board




def PrintBoard(board:list[list[Square]],debug=False): #type hint for intellisense
    # Modified example of a function to print the board in the terminal.
    # Inputs:
    #        board: 2d array of the Square class
    #        debug: boolean flag to unhide the whole board (and highlight mines in red using ANSI escape)

    rows = len(board)
    cols = len(board[0])
    colsIndex  = range(0,cols)

    print('\n\t', end='') # Required for proper visualization of the columns' numbers

    for i in colsIndex: # Print the numbers of columns
        print(i,'\t',end='')

    print('\n')
    for row in range(rows):
        print(row,'|\t',end='') # Print the numbers of rows

        for col in range (cols):
            currentSquare = board[row][col] #set the current square we are printing

            
                
            if  currentSquare.isHidden and not debug:   #cases where the square is hidden
                if currentSquare.isFlagged:
                    print("F", "\t", end="") #when a hidden square is flagged, print "F"
                else:
                    print("X","\t",end="") #otherwise, print "X"
                    
            elif currentSquare.isMine:
                if debug:
                    print("\u001b[41m*\u001b[0m","\t",end="")  #highlights mine in red if debug is enabled
                    
                else:
                    print("*","\t",end="") #prints mine normally, should only show at end of game
                
            elif currentSquare.cueNumber == 0:
                print(" ", "\t", end="") #empty squares are displayed with a space
            else:
                print(currentSquare.cueNumber, "\t", end="") #squares with clues have their number placed in them
            
        print('\n')


def CheckWin(board:list[list[Square]]): #type hint for intellisense
    #Checks if all safe squares are opened.
    #Inputs:
    #       board: 2d array of the Square class
    #Outputs:
    #       Boolean:True if the player has won, False if the game continues
    
    for row in board:
        for square in row: #iterate over every square
            if square.isHidden and not square.isMine:
                return(False) #if any safe square is unopened, the player has not won and the check will stop
    print("You Win!") #if the check gets through every square, the player has won
    return(True)
            

def PlayGame(board:list[list[Square]]):#type hint for intellisense
    #Main function for gameplay.
    #Inputs:
    #       board: 2d array of the Square class
    #Outputs:
    #       Boolean: True if the player wins, False if they lose
    flaggedSquares = 0
    while True:
        PrintBoard(board)  
        #PrintBoard(board,True)
        print("Unflagged mines %i."%(totalMines-flaggedSquares))
        print("Please choose an action:")
        print("0:Open")
        print("1:Flag")
        print("2:Unflag") 
        print("3:Hint") #start by printing main game information
        action = input(">>")#take input for action
    
        #if action == "debugwin": return(True)  secret cheat for debugging only
        
        #sanitize action input, first by checking it is an integer, then by checking it is in the correct range
        try:
            action = int(action)
        except ValueError:
            print("That was not a number, try again.")
            continue
        if action <0 or action >3:
            print("That is not a valid action, try again.")
            continue
        noSquare = True
        if action ==3: noSquare=False
        while noSquare:
            currentSquare = input("Please enter a square in the form row.col \n>>")#take input for coordinate, using a . to allow playing with only a numpad
            #sanitize coordinate input, first by checking the format, then that the coordinates are integers and that they are in range of the board
            try:
                coordinates = currentSquare.split(".")
                if len(coordinates) != 2:
                    print("That was not the correct format for the coordinate.")
                    continue
                currentSquare = board[int(coordinates[0])][int(coordinates[1])]
                noSquare = False
            except IndexError:
                print("That coordinate was out of range of the board.")
                continue
            except ValueError:
                print("Make sure the coordinates are integers.")
                continue
            
        currentSquare:Square #type hint for intellisense
        
        #case statement to do all the different actions the player can do
        match action:
            case 0:
                #action: open
                if currentSquare.Open(board):#if the opened square is a mine
                    
                    currentSquare.isHidden = False
                    PrintBoard(board)#show the player where the mine was
                    print("You opened a mine!")
                    return(False)#exit out of the game loop with a failure state
                
                elif CheckWin(board): #if the player opened a safe square, check if it was the last one
                    return(True)
            case 1:
                #action: flag
                if currentSquare.Flag(True): #make sure the square was sucessfully flagged before changing flaggedSquares
                    flaggedSquares +=1
            case 2:
                #action: unflag
                if currentSquare.Flag(False):#make sure the square was sucessfully unflagged before changing flaggedSquares
                    flaggedSquares -=1
            case 3:
                #action: hint
                hintCoordinates = str(random.choice(mineList)).split(", ") #reformats coordinate tuple to look like gameplay input format
                print("Mine at %s.%s" %(hintCoordinates[0],hintCoordinates[1]))
                pass
            case _:
                print("That is not a valid action, try again.") #this default case shouldn't be necessary as action is already sanitized but I left it in just in case
                continue


def Leaderboard(name,difficulty,totalTime):
    #writes information to the leaderboard
    #Inputs:
    #       name: string with the playe's name
    #       difficulty: string that shows the difficulty
    #       totalTime: the number of seconds that the game took
    with open("Leaderboard.txt", "a+") as file: #opens the file to append, creates it if it doesn't exist
        file.write(name+" "+difficulty+" "+str(totalTime))#writes the information
    print("Saved to leaderboard.txt!")
        


def main():
    #Main entry point for the program: collects information before the game starts and handles post-game actions (saving to leaderboard)
    name = input("Please enter your name \n>>")
    
    difficulty = None
    
    diffSelected = False
    
    while not diffSelected:
        
        print("Please choose a difficulty number:")
        print("0:Beginner (9x9, 10 mines)")
        print("1:Intermediate (16x16, 40 mines)")
        print("2:Expert(30x16, 99 mines)")
        
        difficulty = input(">>") #take input for player difficulty
        
        #sanitize difficulty input, first by making sure it is an integer, then that it is in range
        try:
            difficulty = int(difficulty)
        except ValueError:
            print("That was not a number, try again.")
            continue
        
        try:
            difficulty = [*diffDict][difficulty]
            diffSelected = True
        except IndexError:
            print("That is not a valid option, try again.")
            continue
      
        
    board = CreateBoard(*diffDict[difficulty])#creates a board using arguments unpacked from the tuple stored in the diffDict constant
    
    #keep count of time for total time

    startTime = int(time.time())
    
    if PlayGame(board):#PlayGame will return True if the player wins and False if they lose
        endTime = int(time.time())
        totalTime = endTime-startTime 
        Leaderboard(name,difficulty,totalTime) #Write to leaderboard before exiting
        
    print("Game Over")



if __name__ == "__main__":
    main()
    input("Press ENTER to quit")