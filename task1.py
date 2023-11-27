
def ReadLines(path):
    #Attempts to read a given file
    #Inputs:
    #       path: string with file path to check
    #Outputs:
    #       lines: array of every line in the file
    
    try:
        with open (path, "r") as file: #attempts to open the file specified in path
            lines = file.read().splitlines() #reads the whole file into an array consisting of each line as a separate string
        return(lines) #returns the array
    except FileNotFoundError: #if the file is not found, a FileNotFound error occurs
        return #returns None which makes the While loop in main() go round again


def FindWord(word,lines):
    #Perform a binary search on an array of strings
    #Inputs:
    #       word: the string to search for
    #       lines: the array to search in
    #Outputs:
    #       Boolean: whether the word has been found
    #       Line: integer of the line the word is found on (1-indexed)
    
    #initialises index variables used for binary search
    lowerIndex = 0
    upperIndex = len(lines)-1
    currentIndex = upperIndex//2

    while True:#loops until the whole array is searched
        if lines[currentIndex] == word:
            return(True, currentIndex + 1) #case where the word is found

        if lowerIndex == upperIndex: #performing the check to see if the array is exhausted outside of the while statement itself allows the final value to be checked before breaking
            break

        if lines[currentIndex] > word: #if the desired word comes before the current array word in the alphabet
            #move the upper bound of the search down
            upperIndex = currentIndex - 1
        elif lines[currentIndex] < word: #if the desired word comes after the current array word in the alphabet
            #move the lower bound of the search up
            lowerIndex = currentIndex + 1
        
        currentIndex = (lowerIndex + upperIndex)//2 #change the currently checked word to be the center of the lower and upper bounds

    return(False, -1) #if the loop ends without returning, return False and -1 to show the word hasn't been found


def main():
    #Asks user for word to look for and runs FindWord() with it, printing the output
     print("Binary Search For lines")

     lines = None
     while lines == None: #loops until we have a list of lines read from a file
        filePath = input("Please enter the file path to use (blank for default file) \n>>") #asks for the file to load
        if filePath == "": 
            filePath = "words.txt" #case to use the default file
        
        lines = ReadLines(filePath) #attempts to read the specified file, lines is set to None if a file is not found

     word = input("Please enter the word to be found \n>>") # asks for the word to find, input does not need to be sanitized since we are searching for a string and input() gives a string
     wordFound,line = FindWord(word,lines) #runs findWord, which returns a boolean of whether the word was found and the line number
     if wordFound:
        print("Word found on line %i." %(line)) #case where the word was found
     else:
        print("Word not found in given file.")#case where the word was not



if __name__ == "__main__":
    main()
    input("Press ENTER to quit")