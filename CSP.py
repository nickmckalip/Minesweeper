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


def backtracking_search(adjacent: List[List[List[tuple]]], domain: List[List[tuple]], queue: List[tuple], numberMines: int, totalMines: int) -> Tuple[Optional[List[int]], int]:
    """Perform backtracking search on CSP

    Args:
        adjacent (List[List[List[tuple]]]): Indices of adjacent squares for each square
        domains (List[List[tuple]]): Number of mines surrounding the index 
        queue (List[tuple]): List of indices of the frontier (being all blocks that are next to uncovered blocks)
        numberMines (int): number of mines currently on the board 
        totalMines (int): total mines that can be placed on the board

    Returns:
        Tuple[Optional[List[int]], int]: Solution or None indicating no solution found and the number of recursive backtracking calls
    """ 

    #where the bombs are
    assignment = []

    def backtrack(assignment: List[tuple]) -> Optional[Dict[int, int]]:
        """Backtrack search recursive function

        Args:
            assignment (Dict[int, int]): Values currently assigned to variables (variable index as key)

        Returns:
            Optional[Dict[int, int]]: Valid assignment or None if assignment is inconsistent
        """
        #check to see if complete 
        if numberMines == totalMines:
            return assignment
        
        removedBlocks = []
        minesAdded = 0
 
        minesAdded += 1 #number of mines added to board
        block = queue.pop(0) #removing first part of queue
        removedBlocks.append(block) #list of removed blocks

        numberMines += 1

        conflict = False

        #iterating through whole list to see if new bomb is in neighborhood, if it is checks to see if adding it will ruin 
        for row in adjacent:
            for col in row:
                if block in col:
                    if domain[block[0]][block[1]][1] + 1 >= domain[block[0]][block[1]][0]:
                        conflict = True

        
        if conflict == False:
            domain[block[0]][block[1]][1] += 1 

            result = assignment.append(block)

            if result != None:
                return assignment
                        
            else: 
                for index in removedBlocks:
                    domain[index[0]][index[1]][1] -= 1

                removedBlocks.clear()    
                numberMines -= minesAdded
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
            domain[i].append((0,0))
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

            #Adding frontier blocks to queue 
            if board[i][ii] == 0:
                t = True
                j = 0
                while t == True or j < len(adjacent[i][ii]):
                    if adjacent[i][ii][j] != 0:
                        t = False
                    elif (j+1) == len(adjacent[i][ii]):
                        queue.append((i,ii))
                    j+=1
                 
    return backtracking_search((adjacent, domain, queue, numberMines, totalMines))


if __name__ == "__main__":

    board = [[1,1,9],[1,10,9],[2,9,9]]

    print(minesweeper(board, 2)) #given the fake board which is a reference to the realboard, but is all 9s