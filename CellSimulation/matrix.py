from multiprocessing import Pool

class Matrix:
  def __init__ (self, rows, columns):
    #store amount of rows, columns, and create empty matrix
    self._rows = rows
    self._columns = columns
    self._matrix = [["" for columns in range(self._columns)] for rows in range (self._rows)]
  
  #-----------------------------------------------------------------------------

  #prints matrix to console by seeking through and printing corresponding character
  def print_matrix(self):
    for row in self._matrix:
      for column in row:
        if (column == 0):
          print(".", end = "")
        else:
          print("O", end = "")
      print ("")
  
  #-----------------------------------------------------------------------------

  #checks the neighbors of the cells to determine how many of them are alive
  def check_neighbors(self, row, column):
    numAlive = 0;

    #ranges to check all immediate neighbors of cells
    for i in range(-1, 2):
      for j in range (-1, 2):
        if (i == 0 and j == 0):
          numAlive = numAlive
        else:
          #if the cell is on the edge, it gets the correct neighbors by "wrapping around"
          tempRow = row + i
          tempCol = column + j
          if (tempRow == -1):
            tempRow = len(self._matrix)-1
          elif (tempRow == self._rows):
            tempRow = 0
          if (tempCol == -1):
            tempCol = len(self._matrix[row])-1
          elif (tempCol == self._columns):
            tempCol = 0
          #if cell is alive, adds 1 to number alive
          if (self._matrix[tempRow][tempCol] == 1):
            numAlive += 1

    #returns number alive          
    return (numAlive)
        
  #-----------------------------------------------------------------------------

  #runs through the 100 iterations serially
  def new_matrix(self):
    for i in range(100):
      newRow = []
      allRows = []

      #goes through each cell one by one
      for row in range(len(self._matrix)):
        for column in range(len(self._matrix[row])):
          #gets number of neighbors that are alive
          numAlive = self.check_neighbors(row, column)
          #if the cell is alive, checks conditions and determines state for next cycle
          # appends 1 for alive or 0 for dead to build the next matrix
          if (self._matrix[row][column] == 1):
            if (numAlive > 1 and numAlive < 5):
              newRow.append(1)
            else:
              newRow.append(0)
          #if the cell is dead, checks conditions and determines state for next cycle
          # appends 1 for alive or 0 for dead to build the next matrix
          else:
            if (numAlive > 0 and numAlive%2 == 0):
              newRow.append(1)
            else:
              newRow.append(0)
        #at the end of the row, adds current row to "allRows" and clears it to build next one
        allRows.append(newRow)
        newRow = []

      #changes the matrix to the new rows that were just created so the loop can repeat
      self._matrix = allRows

      self.print_matrix()
      print("\n")

  #-----------------------------------------------------------------------------

  #the is pretty much the same as the previous function, but is compatible with muliprocessing
  def new_matrixThreaded(self, matrixData):
    rows = matrixData

    newRow = []
    allRows = []

    del matrixData

    #goes through each cell passed in
    for row in rows:
      for column in range (len(self._matrix[row])):
        #checks number of alive neighbors
        numAlive = self.check_neighbors(row, column)
        #if the cell is alive, checks conditions and determines state for next cycle
        # appends 1 for alive or 0 for dead to build the next matrix
        if (self._matrix[row][column] == 1):
          if (numAlive > 1 and numAlive < 5):
            newRow.append(1)
          else:
            newRow.append(0)
        #if the cell is dead, checks conditions and determines state for next cycle
          # appends 1 for alive or 0 for dead to build the next matrix
        else:
          if (numAlive > 0 and numAlive%2 == 0):
            newRow.append(1)
          else:
            newRow.append(0)
      #at the end of the row, adds current row to "allRows" and clears it to build next one
      allRows.append(newRow)
      newRow = []

    return(allRows)

  #-----------------------------------------------------------------------------

  def start_threading(self, threadNum):
    #determines how many rows will be in each section for muliprocessing
    if (self._rows >= threadNum):
      testSection = self._rows / threadNum
      #if it isnt an even split with division, rounds up
      if (testSection % 1 == 0):
        sectionSize = testSection
      else:
        sectionSize = (self._rows // threadNum) + 1
    else:
      sectionSize == 1

    processPool = Pool(processes=threadNum)

    rowList = []
    poolData = list()
    
    #assigns row numbers in groups depending on section size and appends them to a list
    for i in range (0, self._rows):
      rowList.append(i)
      if len(rowList) == sectionSize:
        poolData.append(rowList)
        rowList=[]
    
    #makes sure all row lists have been appended
    if (rowList != []):
      poolData.append(rowList)

    #runs multiproccessing 100 times
    for i in range(100):
      finalData = processPool.map(self.new_matrixThreaded, poolData)

      j = 0

      #reconstructs the matrix from all of the new rows created in the new_matrixThreaded function
      for section in finalData:
        for row in section:
          self._matrix[j] = row
          j += 1
      
      del finalData
      
      self.print_matrix()
      print("\n")