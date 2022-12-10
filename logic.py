

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

    output = []
    output.append(adjacent)
    output.append(domain)
    output.append(queue)


    return output


def primary(board: list[list]) -> list[list]:
    """
    Input game board 
    output two arrays, first one is safe cells, second one is bomb cells
    """
    safeFlag = [set(),set()]
    f = frontier(board)
    adjacent = f[0]
    domain = f[1]
    queue = f[2]

    for i in range(len(domain)):
        for ii in range(len(domain[i])):

            #If the domain is full (enough flags surround) then all other adjacent unopened blocks are safe
            if domain[i][ii][0] == domain[i][ii][1]:
                for block in adjacent[i][ii]:
                    if board[block[0]][block[1]] == 9:
                        safeFlag[0].add(block)

            #Cells are mines when #hidden cells = number of block - surrounding mines 
            else:
                var = domain[i][ii][0] - domain[i][ii][1]
                num = 0
                for block in adjacent[i][ii]:
                    if board[block[0]][block[1]] == 9:
                        num +=1
                if var == num:
                    for block in adjacent[i][ii]:
                        if board[block[0]][block[1]] == 9:
                            safeFlag[1].add(block)
    
    return safeFlag
            


if __name__ == "__main__":

    board =  [[9,1,1,9,9],
             [9,1,10,9,9],
             [0,1,2,9,9],
             [0,1,2,9],
             [0,1,9,9,9]]
