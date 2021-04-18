## Cierra Ditmore (R#11574054) | Project 1 | 11/24/2020
##
## This program executes the first 100 steps of a cellular life simulator
##    and outputs the final matrix created to a file
##

import getopt, sys
import tkinter as tk

window = tk.Tk()

from matrix import Matrix

def main(argv):
  question = "How many threads would you like to run? (1-20): "
  

  #makes amount of threads into int
  threads = int(input(question))

  while ((threads < 1) or (threads > 20)):
      threads = int(input(question))
  
  #creates matrix based on input file
  startingMatrix = read_file("input.txt")

  #if there is only one thread i have it run serially with a different function
  # otherwise, go to threading function
  if (threads == 1):
    startingMatrix.new_matrix()
  else:
    startingMatrix.start_threading(threads)

  #write final matrix to output.txt
  write_file("output.txt", startingMatrix)


#-----------------------------------------------------------------------------

#read input file and form the starting matrix
def read_file (inputFile):
  file = open(inputFile, "r")

  columnNum = -1
  rowNum = 1

  #get amount of rows and columns in file
  for char in (file.readline()):
    columnNum += 1
  while file.readline():
    rowNum += 1

  #create empty matrix
  startingMatrix = Matrix(rowNum, columnNum)

  file.seek(0,0)

  #seek through file and input the values into the empty matrix
  #  error if there is an invalid character
  for i in range(rowNum):
    j = 0
    for char in (file.readline()):
      if (char == "."):
        startingMatrix._matrix[i][j] = 0
      elif (char == "O"):
        startingMatrix._matrix[i][j] = 1
      elif char == "\n":
        i = i
      else:
        print("Invalid char in array input")
        exit(1)
      j += 1
  
  #close file and return matrix
  file.close()
  return(startingMatrix)

#-----------------------------------------------------------------------------

def write_file(outputFile, finalMatrix):
  file = open(outputFile, "w")

  #seek through the final matrix and write the correct character to output.txt
  for row in finalMatrix._matrix:
    for column in row:
      if (column == 1):
        file.write("O")
      else:
        file.write(".")
    file.write("\n")
  
  file.close()

#-----------------------------------------------------------------------------

if __name__ == "__main__":
  main(sys.argv[1:])
