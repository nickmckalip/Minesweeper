import argparse, time
from http.client import CONFLICT
from typing import Dict, List, Optional, Set, Tuple
from xmlrpc.client import boolean 
import BoardInit as BI
import copy
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
    assignment = [] #0 = bomb, 1 = safe
    minesAdded = 0

    helper = 0
    removedBlocks = []

    def backtrack(assignment: List[tuple], q:List[tuple]) -> Optional[Dict[int, int]]:
        """Backtrack search recursive function

        Args:
            assignment (Dict[int, int]): Values currently assigned to variables (variable index as key)

        Returns:
            Optional[Dict[int, int]]: Valid assignment or None if assignment is inconsistent
        """
        #check to see if complete 


        nonlocal numMines
        nonlocal minesAdded
        nonlocal helper
        nonlocal removedBlocks

        #print("!!!!!!!!!!")

        #Checking to see that if a block is surrounded by knowns, that its domain is full
        allCheck = True
        if len(q) == len(removedBlocks):
            for i in range(len(domain)):
                for ii in range(len(domain[i])): 
                    if domain[i][ii][0] < 9 and domain[i][ii][0] != domain[i][ii][1]: #Block is opened, and the domain is not full
                        allCheck = False


        if len(q) == len(removedBlocks) and allCheck == True:
            #print("--")
            return assignment
        elif len(q) == len(removedBlocks) and allCheck == False:
            #print("-+-+")
            return None


        for block in queue:
            #helper += 1
            #print(helper)
            #print(q)
            #print(removedBlocks)
            #print(assignment)

            removedBlocks.append(block) #list of removed blocks
            conflict = False

            #iterating through whole list to see if new bomb is in neighborhood, if it is checks to see if adding it will ruin 
            for neighbor in adjacent[block[0]][block[1]]:
                if domain[neighbor[0]][neighbor[1]][1] + 1 > domain[neighbor[0]][neighbor[1]][0]: #Checks to see if number of surrounding bombs exceeds limit
                    conflict = True

            if totalMines < numMines:
                conflict = True 

            if conflict == False:
                for i in range(len(adjacent)):
                    for ii in range(len(adjacent[i])):
                        if block in adjacent[i][ii]:
                            domain[i][ii][1] += 1  #add to the domains of the adjacent blocks the new assignment 

                assignment.append(block)
                numMines += 1
                minesAdded += 1 #number of mines added to board for this run

                #q.remove(block)

                result = backtrack(assignment, q)
                #print("--")
                #print(result)

                if result != None:
                    return assignment 
                
                else: 
                    helper -=1 
                    assignment.remove(block) #removed assigned block in most recent 
                    numMines -= 1
                    minesAdded -= 1
                    for i in range(len(adjacent)):
                        for ii in range(len(adjacent[i])):
                            if block in adjacent[i][ii]:
                                domain[i][ii][1] -= 1 #removed from the domains of the adjacent blocks
                        
                    removedBlocks.pop()

            else:
                
                #q.remove(block)

                result = backtrack(assignment, q)

                if result != None:
                    return assignment 
                
                else: 
                    helper -=1 
                    removedBlocks.pop()
                
        #print("!")
        return None


    q = copy.deepcopy(queue)
    bombLocs = backtrack(assignment, q)

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
            if board[i][ii] == 10: #if block is a mine add to number of mines on board
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


    return backtracking_search(adjacent, domain, queue, numberMines, totalMines)


if __name__ == "__main__":

    board = [[1,2,9,9,9],
             [2,10,9,9,9],
             [2,9,9,9,9],
             [1,1,9,9,9]]

    print(minesweeper(board, 4)) 