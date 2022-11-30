import argparse, time
from http.client import CONFLICT
from typing import Dict, List, Optional, Set, Tuple
from xmlrpc.client import boolean 
import BoardInit as BI
"""
Variables: Squares on the Board
Domains: 8 adjacent squares
Constraints: Number of mines surrounding a square with a number and number of mines on the board


"""


def backtracking_search(adjacent: List[List[List[tuple]]], domain: List[List[List[int]]], queue: List[tuple], numMine: int, totalMines: int) -> Tuple[Optional[List[int]], int]:
    """Perform backtracking search on CSP

    Args:
        adjacent (List[List[List[tuple]]]): Indices of adjacent squares for each square
        domains (List[List[List[index, current number of mines]]]): Number of mines surrounding the index 
        queue (List[tuple]): List of indices of the frontier (being all blocks that are next to uncovered blocks)
        numMine (int): number of mines currently on the board 
        totalMines (int): total mines that can be placed on the board

    Returns:
        Tuple[Optional[List[int]], int]: Solution or None indicating no solution found and the number of recursive backtracking calls
    """ 
    numMines = numMine
    #where the bombs are
    assignment = []
    minesAdded = 0

    def backtrack(assignment: List[tuple]) -> Optional[Dict[int, int]]:
        """Backtrack search recursive function

        Args:
            assignment (Dict[int, int]): Values currently assigned to variables (variable index as key)

        Returns:
            Optional[Dict[int, int]]: Valid assignment or None if assignment is inconsistent
        """
        #check to see if complete 


        nonlocal numMines
        nonlocal minesAdded
        if totalMines == numMines:
            return assignment

        removedBlocks = []
        

        while len(queue) > 0:
            minesAdded += 1 #number of mines added to board
            block = queue.pop(0) #removing first part of queue
            print(block)
            removedBlocks.append(block) #list of removed blocks

            numMines += 1

            conflict = False

            #iterating through whole list to see if new bomb is in neighborhood, if it is checks to see if adding it will ruin 
            for row in adjacent:
                for col in row:
                    if block in col:
                        if domain[block[0]][block[1]][1] + 1 >= domain[block[0]][block[1]][0]: #Checks to see if number of surrounding bombs exceeds limit
                            conflict = True
            
            if conflict == False: #If no conflict continue parsing
                for i in range(len(adjacent)):
                    for ii in range(len(adjacent[i])):
                        if block in adjacent[i][ii]:
                            domain[i][ii][1] += 1  


                assignment.append(block)
                result = backtrack(assignment)


                if result != None:
                    return assignment
                            
                else: 
                    for index in removedBlocks:
                        domain[index[0]][index[1]][1] -= 1

                    removedBlocks.clear()    
                    numMines -= minesAdded
                    minesAdded = 0

                    assignment.remove(block)
            
            return None

    bombLocs = backtrack(assignment)

    return bombLocs

def minesweeper(board: List[List[int]], totalMines: int) -> List[List[int]]:
    """Solve minesweepr puzzle using backtracking search as far as it can go off of inferences

    Args:
        board (List[[int]]): 2D array of the minesweeper board
        totalMines (int): total number of mines allowed

    Returns:
        board List[[int]]: 2D array of minesweeper board solved as far as it could have been
    """
    numberMines = 0
    adjacent = [] #List of adjacent indices in a 2D matrix for each variable
    domain = [] #Number of surrounding mines for each variable
    queue = [] #list of frontier blocks

    for i in range(len(board)): 

        #build 2d part of adjacent list an domain list
        adjacent.append([])
        domain.append([])

        for ii in range(len(board[i])):
            adjacent[i].append([])
            domain[i].append([0,0])
            if board[i][ii] == 9: #if block is a mine add to number of mines on board
                numberMines += 1

            surroundingBlocks = [(i-1,ii-1),(i-1,ii),(i-1,ii+1),(i,ii+1),(i+1,ii+1),(i+1,ii),(i+1,ii-1),(i,ii-1)]


            for block in surroundingBlocks: #Populating the adjacent indices of each block in a 2d matrix
                if block[0] == -1 or block[1] == -1:
                    pass
                else: 
                    try: #Gets rid of index errors, so i don't have to code all the corner cases
                        board[block[0]][block[1]]
                        adjacent[i][ii].append(block)
                    except IndexError:
                        pass
            
            #creating domains of each variable (How many bombs are currently surrounding)
            domain[i][ii][0] = board[i][ii]
            for neighbor in adjacent[i][ii]:
                if board[neighbor[0]][neighbor[1]] == 10:
                    domain[i][ii][1] += 1
            
            #Adding frontier blocks to queue  (Blocks that are uncovered and not only surrounded by uncovered blocks)
            if board[i][ii] == 9: #If block is uncovered 
                t = True
                neighbors = set()
                for index in adjacent[i][ii]:
                    neighbors.add(board[index[0]][index[1]])

                if len(neighbors) == 1:
                    if 9 in neighbors or 10 in neighbors:
                        t = False
                elif len(neighbors) == 2:
                    if 9 in neighbors and 10 in neighbors:
                        t = False

                if t == True:
                    queue.append((i,ii))

    #Trying to make sense of outputs
    #Do I need that many dimensions of matrices??
    #The queue is adding too many

    return backtracking_search(adjacent, domain, queue, numberMines, totalMines)


if __name__ == "__main__":

    board = [[1,2,9],
             [1,10,2],
             [1,9,9]]

    print(minesweeper(board, 2)) 