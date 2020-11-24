# Project: 8 2048 Solver
# Program name: PlayerAI_UG.py
# Author: Greg Tystahl
# Date Created 11/02/2020
# Purpose: Win the 2048 puzzle 50% of the time

# Revision History:
# Date          Author          Revision
# 11/9/2020     Greg Tystahl    Completely reworked to better follow the article
# 11/23/2020    Greg Tystahl    Added in comments and article link

# How to run: Run the GameManager.py and it should take care of everything

# Article to which I gathered Heuristic ideas:
# https://www.businessinsider.com/artificial-intelligence-crushed-all-human-records-in-the-addictive-tile-game-2048--heres-how-2015-5

# (I am only commenting the stuff that I added)

import random
import time
import sys
from Grid import Grid
from BaseAI import BaseAI
import math
MINUS_INFINITY=-10000000
PLUS_INFINITY=10000000
MAX_DEPTH=4
TIME_MAX=.2

class Node(object):
    def __init__(self,pzle): 
        self.parent=None
        self.puzzle=pzle
        self.depth=0
        self.move=-1
    
    def setMove(self,m):
        self.move=m

    def getMove(self):
        return self.move

    def getPuzzle(self):
        return self.puzzle
    
    def getParent(self):
        return self.parent

    def setParent(self,parent):
        self.parent=parent

def traceMove(node,pzzle):
    
    move=-1
    
    move1=-1
    while node!=None:
        move1=move
        move=node.getMove()
       
        node=node.getParent()

    if move1==-1:
        # This is a modified way to get the next best move based on spaces available

        # This holds the values of the moves
        dict = {1: MINUS_INFINITY * 10, 2: MINUS_INFINITY * 10, 3: MINUS_INFINITY * 10, 0: MINUS_INFINITY * 10}

        p = Node(pzzle)
        curr = Node(pzzle)
        curr.parent = p

        # These get the moves availalbe from the current puzzle to the move specified
        np = myCopy2(pzzle)
        d = slideDown(np)
        if not isSame(pzzle, d):
            dict[1] = evaluateh(curr, d, 1)

        np = myCopy2(pzzle)
        l = slideLeft(np)
        if not isSame(pzzle, l):
            dict[2] = evaluateh(curr, l, 2)

        np = myCopy2(pzzle)
        r = slideRight(np)
        if not isSame(pzzle, r):
            dict[3] = evaluateh(curr, r, 3)

        np = myCopy2(pzzle)
        u = slideUp(np)
        if not isSame(pzzle, u):
            dict[0] = evaluateh(curr, u, 0)

        # This gets the best move out of the moves above
        move1 = 1
        biggest = MINUS_INFINITY * 10
        for num in dict:
            if biggest < dict[num]:
                biggest = dict[num]
                move1 = num

    return move1



class value(object):
    def __init__(self,n,v):
        self.node=n
        self.value=v

    def getNode(self):
        return self.node
    def getValue(self):
        return value

    
class PlayerAI(BaseAI):

    def getMove(self, grid):
        puzzle=transformGrid(grid.map)
        node=Node(puzzle)
        
        alpha=value(None,MINUS_INFINITY)
        beta=value(None,PLUS_INFINITY)
        depth=0
        res=maxValue(node,alpha,beta,depth,time.clock())
        return  traceMove(res.getNode(),puzzle)


def maxValue(node,alpha,beta,depth,t_time):
    
    "generate up(0) down(1) left(2) right(3) action nodes"
    

    
    puzzle=node.getPuzzle()

    c_time=time.clock()-t_time

    if depth >= MAX_DEPTH or c_time>TIME_MAX:
        move=node.getMove()
        evaluate = evaluateh(node, puzzle, move)

        val=value(node,evaluate)
        
        return val
    
    for a in [1,2,3,0]:
        copy=myCopy2(puzzle)
        
        if a==0:
            copy=slideUp(copy)
        elif a==1:
            copy=slideDown(copy)
        elif a==2:
            copy=slideLeft(copy)
        else:
            copy=slideRight(copy)

        if not isSame(copy,puzzle):
            reset(copy)
            newNode=Node(copy)
            newNode.setParent(node)
          
            newNode.setMove(a)
    
            temp=minValue(newNode,alpha,beta,depth,t_time)

            if temp.value>alpha.value:
                alpha=temp

            if alpha.value>=beta.value:
                return beta
    return alpha

def minValue(node,alpha,beta,depth,t_time):

    "generate up(0) down(1) left(2) right(3) action nodes"
    depth=depth+1

    puzzle=node.getPuzzle()
    h=spacesOpen(puzzle)
    if h==0:
        move=node.getMove()
        ev = evaluateh(node, puzzle, move)
        evaluate = MINUS_INFINITY + ev

        val=value(node,evaluate)
        
        return val
    
    for move in range(16):
        copy=myCopy2(puzzle) 

        if(copy[move][0]==0):
            # This is a list that holds the possible values the computer will use. It default holds just 2 for speed
            movevals = [2]

            # If there are only three available spots left, add 4 to the list of possibles
            if h <= 1:
                movevals.append(4)

            # This goes through each of the possible placeable values
            for v in movevals:
                copy[move][0]=v
                newNode=Node(copy)
                newNode.setParent(node)

                temp=maxValue(newNode,alpha,beta,depth,t_time)

                if temp.value<beta.value:
                    beta=temp

                if beta.value<=alpha.value:
                    return alpha
    return beta
      



def myCopy2(s):
    n=[[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]

    for i in range(16):
        n[i][0]=s[i][0]

    return n


def spacesOpen(puzzle):
    # This gets the number of free spaces. (Made in class)

    count = 0
    for i in puzzle:
        if i[0] == 0:
            count += 1

    return count

def H1(puzzle):
    # Reworked the class H1 to follow tip 3 in article
    left = spacesOpen(puzzle)
    if left > 3:
        return -left
    else:
        return left

def H2(puzzle, move):
    # Gets the amount of merges done before the current puzzle to now

    copy = myCopy2(puzzle)
    numFree = H1(puzzle)  # number of free spaces before move
    if numFree > 5:
        if move == 0:
            copy = slideUp(copy)
        elif move == 1:
            copy = slideDown(copy)
        elif move == 2:
            copy = slideLeft(copy)
        else:
            copy = slideRight(copy)

        curFree = H1(copy)  # number of free tiles for speculative board

        diff = curFree - numFree  # diff is the number of merges

        return diff
    else:
        return 0

def H3(puzzle):
    # This tries to get rows in the order from greatest on the left to least on right
    # Gets inspiration from tip 2 in article

    # This is the variable that will be returned
    val = 0

    # Goes through each row
    for a in range(4):
        # Variable that checks to make sure the row is in order
        rowgood = True

        # This is the previous item value
        checkval = PLUS_INFINITY

        # This is the rows total
        rowval = 0

        # Goes through each item in the row
        for b in range(4):
            # Gets the items value
            itemval = puzzle[(a * 4) + b][0]

            # Adds the value to the rows total
            rowval += itemval

            if itemval != 0:
                if checkval < itemval:
                    rowgood = False
            checkval = itemval

        # If the row is in order, add the rows val to the return val
        if rowgood:
            val += rowval * (a + 1)
        else:
            val -= rowval * (a + 1)
    # Return the total vals of the good rows
    return val

def H4(puzzle):
    # This tries to get the highest values in line from bottom being highest to top being lowest
    # Gets inspiration from tip 2 in article

    val = 0
    for a in range(4):
        columnval = 0
        lastval = MINUS_INFINITY
        columngood = True
        for b in range(4):
            cellval = puzzle[(b*4) + a][0]
            if cellval != 0:
                if lastval > cellval:
                    columngood = False
            lastval = cellval
            columnval += cellval
        if columngood:
            val += columnval * (4 - a)
        else:
            val -= columnval * (4 - a)

    return val

def H5(puzzle):
    # Tries to get the ai to have the biggest value in the bottom left corner
    # This stems from tip 1 in article

    # Gets the bottom left row
    box = puzzle[12][0]

    # Gets the biggest cell in the puzzle
    bc = biggestCell(puzzle)

    # If the biggest val is not in the bottom left, return double the negative of the biggest value
    if box != bc:
        return -bc
    else:
        # else return nothing
        return bc

def H6(puzzle):
    # Tries to get the same stuff next to each other

    # This is the return var
    val = 0

    # Goes through each item in the puzzle
    for i in range(len(puzzle)):
        # Gets the cell of the puzzle
        cell = puzzle[i]

        # This is the possible neighbor location differences
        lst = [1, -1, 4, -4]

        # For each number in the above list
        for num in lst:
            # Try to get that new location
            try:
                # Gets the new location
                loc = i + num

                # Checks to make sure the item exists
                check = (i % 4) + num

                # If the item does exist
                if check >= 0 and check < 4:
                    # Gets the second cell
                    cell2 = puzzle[loc]

                    # checks to see if they are equal
                    if cell[0] == cell2[0]:
                        # If they are add to the total val
                        val += cell[0]
            except:
                val += 0
    # returns the vals that are the same
    return val

def H7(puzzle):
    # Tries to make sure that there arent stuff stuck where it cant be merged

    # This is the return val
    val = 0

    # Goes through each item in the puzzle
    for i in range(len(puzzle)):
        # Gets the cell
        cell = puzzle[i]

        # Makes sure the cell isnt zero
        if cell[0] != 0:
            # reduced cell val: This is the exponent of 2
            rcv = math.log2(cell[0])
            # The number of bad spaces next to it
            numbad = 0
            biggest = 0
            lst = [1, -1, 4, -4]
            for num in lst:
                try:
                    # Gets the next location
                    loc = i + num

                    # Gets the check to make sure its possible
                    check = (i % 4) + num
                    if check >= 0 and check < 4:
                        # Gets the next cell
                        cell2 = puzzle[loc]

                        # Makes sure the next cell isnt zero
                        if cell2[0] != 0:
                            # Gets the exponent of the second number
                            rcv2 = math.log2(cell2[0])

                            # Checks to make sure the exponents arent too far apart
                            if not (rcv2 - 1 < rcv < rcv2 + 1):
                                # If they are add to the numbad
                                numbad += 1
                                if cell2[0] > biggest:
                                    biggest = cell2[0]
                except:
                    numbad += 1
            # If the number of bad spaces is over half
            if numbad > 2:
                # Subtract from the eval total
                val -= biggest
    # Return the total val
    return val

def evaluateh(n, puzzle, move):
    # debugDisplay(puzzle)
    # This is the function that adds all of the hueristics together
    h1 = 1.0 * H1(puzzle) # Spaces open
    h2 = 1.0 * H2(n.parent.puzzle, move) # Num of merges
    h3 = 1.0 * H3(puzzle) * 10 # Left to right
    h4 = 1.0 * H4(puzzle) * 10 # Top to Bottom
    h5 = 1.0 * H5(puzzle) * 50 # Biggest in bottom left
    h6 = 1.0 * H6(puzzle) # Same next to each other
    h7 = 1.0 * H7(puzzle) # Bad spaces

    total = h1 + h2 + h3 + h4 + h5 + h6 + h7

    return total

def biggestCell(puzzle):
    # This is a function I made to get the biggest value

    # The var that holds the biggest
    biggest = 0

    # Goes through each item in the puzzle
    for i in range(len(puzzle)):
        # If the item is bigger, update the biggest variable
        if puzzle[i][0] > biggest:
            biggest = puzzle[i][0]
    # Return the biggest value
    return biggest

def isSame(s1,s2):
    for i in range(16):
        if s1[i][0]!=s2[i][0]:
            return False
    return True

def reset(s):
    for i in range(16):
        s[i][1]=0

def debugDisplay(puzzle):
    # This was used for debugging, allowed me to see the board before it was evaluated

    # Below goes through the whole puzzle and prints it to the screen
    print()
    a = 0
    for i in range(len(puzzle)):
        print(puzzle[i][0], end=" ")
        a += 1
        if a == 4:
            print()
            a = 0
    print()

def slideRight(s1):
    for out in range(3):
        for c in range(3,0,-1):
            for r in range(0,4):
                i=4*r+c-1
                j=i+1
                
                if s1[j][0]==0:
                    s1[j][0]=s1[i][0]
                    s1[i][0]=0
                    s1[i][1]=0
                if s1[j][0]!=0:
                    if s1[j][0]==s1[i][0] and s1[j][1]!=1 and s1[i][1]!=1:
                        s1[j][0]=s1[j][0]+s1[j][0]
                        s1[i][0]=0
                        s1[i][1]=0
                        s1[j][1]=1

            

    return s1
            
def slideLeft(s1):
    for out in range(3):
        for c in range(0,3):
            
            for r in range(0,4):
                i=4*r+c+1
                j=i-1

                if s1[j][0]==0:
                    s1[j][0]=s1[i][0]
                    s1[i][0]=0
                    s1[i][1]=0
                if s1[j][0]!=0:
                    if s1[j][0]==s1[i][0] and s1[j][1]!=1 and s1[i][1]!=1:
                        s1[j][0]=s1[j][0]+s1[j][0]
                        s1[i][0]=0
                        s1[i][1]=0
                        s1[j][1]=1
                        

            

    return s1

def slideUp(s1):
    for out in range(3):
        for c in range(3):
            for r in range(0,4):
                i=4*c+r+4
                j=i-4
                
                if s1[j][0]==0:
                    s1[j][0]=s1[i][0]
                    s1[i][0]=0
                    s1[i][1]=0
                if s1[j][0]!=0:
                    if s1[j][0]==s1[i][0] and s1[j][1]!=1 and s1[i][1]!=1:
                        s1[j][0]=s1[j][0]+s1[j][0]
                        s1[i][0]=0
                        s1[i][1]=0
                        s1[j][1]=1
            

    return s1

def slideDown(s1):
    for out in range(3):
        for c in range(3,0,-1):
            for r in range(4,0,-1):
                i=4*c+r-5
                j=i+4
                if s1[j][0]==0:
                    s1[j][0]=s1[i][0]
                    s1[i][0]=0
                    s1[i][1]=0

                if s1[j][0]!=0:
                    if s1[j][0]==s1[i][0] and s1[j][1]!=1 and s1[i][1]!=1:
                        s1[j][0]=s1[j][0]+s1[j][0]
                        s1[i][0]=0
                        s1[i][1]=0
                        s1[j][1]=1
            

    return s1

def transformGrid(grid):
    newGrid=[[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]
    for i in range(4):
        for j in range(4):
            newGrid[4*i+j][0]=grid[i][j]
    return newGrid
