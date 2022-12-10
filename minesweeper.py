"""
Create New Board 
Create user board similar to real board 
Make first move 
See result
Pass board to CSP
Make assumption 
Flag if 100% 
Pick spot if not in results


"""
import argparse, os, random, sys
import BoardInit as bi
import CSP as csp
import logic as l



def frontier(board: list[list]) -> list[(tuple)]:
    """
    Gives frontier for all the bombs from the player board 

    Input: Player board list[list(int)
    
    Outputs: Locations of the frontier blocks

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

    return queue






if __name__ == "__main__": 
    fail = 0
    numberRuns = 0

    #Run it n times
    while numberRuns < 1000:
        difficulty = "easy"

        #Starting board where first guess is 0 
        hiddenBoard = bi.initBoard(difficulty)
        while hiddenBoard[0][0] != 0:
            hiddenBoard = bi.initBoard(difficulty)

        playerBoard = bi.initBoard(difficulty)

        for i in range(len(playerBoard)):
            for ii in range(len(playerBoard[i])):
                playerBoard[i][ii] = 9

        playerBoard[0][0] = hiddenBoard[0][0]

        #num of bombs based on difficulty
        numBombs = 10
        if difficulty == "medium":
            numBombs = 40
        elif difficulty == "hard":
            numBombs = 99


        bomb = False
        flags = 0
        num = 0

        #stops when it hits a bomb or it places the right amount of flags
        while bomb == False and flags < numBombs:

            safe = set()
            flag = set()
            newInfo = False
            q = frontier(playerBoard)
            
            #First attempt
            primaryResults = l.primary(playerBoard)
            
            #If there are safe blocks add to queue
            if len(primaryResults[0]) > 0:
                newInfo = True
                for each in primaryResults[0]:
                    safe.add(each)
            #If there are flags ass
            elif len(primaryResults[1]) > 0:
                newInfo = True
                for each in primaryResults[1]:
                    flag.add(each)

            #If nothing is 100% 
            if newInfo == False:
                #If q is too long just guess since 2^n options 
                if len(q) > 5:
                    randomInt01 = random.random()
                    newIndex = int(randomInt01 * len(q))
                    safe.add(q[newIndex])
                
                else:
                    bombLocs = csp.minesweeper(playerBoard, numBombs)

                    #adds result into dictionary 
                    combinedOdds = {"total": 0}
                    for result in bombLocs:
                        combinedOdds["total"] +=1
                        for block in result:
                            if block in combinedOdds:
                                combinedOdds[block] += 1
                            else:
                                combinedOdds[block] = 1

                    #Looks at index with lowest probabilty to show up 
                    lowestPercent = 10000
                    lowestPercentLoc = [0,0]
                    for loc in combinedOdds:
                        if loc != "total":
                            if combinedOdds[loc] < lowestPercent:
                                lowestPercentLoc[0] = loc[0]
                                lowestPercentLoc[1] = loc[1]
                    
                    safe.add((lowestPercentLoc[0], lowestPercentLoc[1]))

            #Sometimes it gets stuck in a loop where the hidden squares can't get into the queue
            num += 1
            stop = False
            if num > 1000:
                for i in range(len(playerBoard)):
                    for ii in range(len(playerBoard[i])):
                        if playerBoard[i][ii] == 9 and stop == False:
                            safe.add((i,ii))
                            stop = True

            #Goes through safe blocks
            for block in safe:
                if hiddenBoard[block[0]][block[1]] == -1:
                    playerBoard[block[0]][block[1]] = hiddenBoard[block[0]][block[1]]
                    bomb = True
                    fail +=1
                else:
                    playerBoard[block[0]][block[1]] = hiddenBoard[block[0]][block[1]]


            for block in flag:
                playerBoard[block[0]][block[1]] = 10
                flags +=1


        numberRuns +=1
        print(numberRuns)


    print("ACCURACY")
    print(fail/numberRuns)

    """
    Easy: 
    5 / 50,000 / 20 // 0.543 / 0.512 / 0.529 / 

    7 / 50,000 / 20 // 0.533
    3 / 50,000 / 20 // 0.513 

    5 / 10,000 / 20 // 0.493
    5 / 75,000 / 20 // 0.526

    5 / 50,000 / 10 // 0.516
    5 / 50,000 / 100 // 0.537
    
    """
