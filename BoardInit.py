"""
Numbers and how they correlate to the board: 
-1 = exploded mine
0 = blank opened cell
1->8 = cell with number of mines surrounding it 
9 = hidden cell
10 = flagged cell
"""
import argparse, os, random, sys
from math import remainder
from typing import Any, Dict, Sequence, Tuple, Union
import numpy as np
import pandas as pd 



def initBoard (diff: str):
    """
    Setting up board 
    input: difficulty coded in
    output: 2D array 
    """
    
    def mineLoc(numMines: int, boardSize: int) -> set:
        """
        creates set with locations of the mines
        input: numMines(int) how many mines are on the board, boardSize(int) size of the board
        return: set with the locations of the mines on the board
        """
        locs = set() #Randomly places mines, into the board 
        while len(locs) < numMines: 
            randomInt01 = random.random() 
            randomMineLoc = randomInt01 * boardSize
            locs.add(int(randomMineLoc))

        return(locs)
    

    if diff == "easy":
        numCols = 8
        numRows = 8
        numMines = 10
        numCells = numCols*numRows

    elif diff == "medium":
        numCols = 16
        numRows = 16
        numMines = 40
        numCells = numCols*numRows
    elif diff == "hard":
        numCols = 16
        numRows = 30
        numMines = 99
        numCells = numCols*numRows

    board = [] #Creating 2D array full of Zeros
    for i in range(numRows): 
        row = []
        for ii in range(numCols):
            row.append(0)
        board.append(row)
    

    mineLocations = mineLoc(numMines, numCells) #Locations for the mines

    for mine in mineLocations: #adding mines into indexes created randomly
        mineRow = mine // numCols
        mineCol = mine - (mineRow*numCols)

        board[int(mineRow)][int(mineCol)] = -1  #Mines are denoted by -1 in the board


    #Goes through every index and adds up number of adjacent mines into square
    for i in range(numRows): 
        for ii in range(numCols):
            if board[i][ii] != -1: #If index is not a mine
                surroundingMines = 0

                #indices of adjacent blocks
                surroundingBlocks = [(i-1,ii-1),(i-1,ii),(i-1,ii+1),(i,ii+1),(i+1,ii+1),(i+1,ii),(i+1,ii-1),(i,ii-1)]

                for block in surroundingBlocks: 
                    if block[0] == -1 or block[1] == -1:
                        pass
                    else:
                        try: #Gets rid of index errors, so i don't have to code all the corner cases
                            if board[block[0]][block[1]] == -1:
                                surroundingMines +=1
                        except IndexError:
                            pass
                        

                board[i][ii] = surroundingMines

    return board


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Choose Difficulty for MineSweeper Board")
    parser.add_argument(
        "-d",
        "--difficulty",
        default="easy",
        help="Difficulty for minesweeper setting Allowed values: easy, medium, hard.",
    )

    args = parser.parse_args()
    board = initBoard(args.difficulty)
    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in board]))
