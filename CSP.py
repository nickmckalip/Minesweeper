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


def backtracking_search(adjacent: List[List[List[tuple]]], domain: List[List[int]], numberMines: int, totalMines: int) -> Tuple[Optional[List[int]], int]:
    """Perform backtracking search on CSP

    Args:
        adjacent (List[List[int]]): Indices of adjacent squares for each square
        queue (Set[Tuple[int, int]]): Variable constraints; (x, y) indicates x must be consistent with y
        domains (List[List[int]]): Domains for each variable

    Returns:
        Tuple[Optional[List[int]], int]: Solution or None indicating no solution found and the number of recursive backtracking calls
    """ 

    def backtrack(assignment: Dict[int, int]) -> Optional[Dict[int, int]]:
        """Backtrack search recursive function

        Args:
            assignment (Dict[int, int]): Values currently assigned to variables (variable index as key)

        Returns:
            Optional[Dict[int, int]]: Valid assignment or None if assignment is inconsistent
        """

        pass

    pass

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
    queue = []

    for i in range(len(board)): 

        #build 2d part of adjacent list an domain list
        adjacent.append([])
        domain.append([])

        for ii in range(len(board[i])):
            adjacent[i].append([])
            domain[i].append(0)
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
            for neighbor in adjacent[i][ii]:
                if board[neighbor[0]][neighbor[1]] == 10:
                    domain[i][ii] += 1

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
                 
    return backtracking_search((adjacent, domain, numberMines, totalMines))


if __name__ == "__main__":

    board = []
    j = 0
    for i in range(9):
        board.append([])
        for ii in range(9):
            board[i].append(j)
            j += 1
    minesweeper(board, 2) #given the fake board which is a reference to the realboard, but is all 9s