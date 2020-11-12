# Project: 8 2048 Solver
# Program name: PlayerAI_UG.py
# Author: Greg Tystahl
# Date Created 11/02/2020
# Purpose: Win the 2048 puzzle 50% of the time

# Revision History:

# How to run: Run the GameManager.py and it should take care of everything

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
        np=myCopy2(pzzle)
        np0=H1(slideUp(np))
        np=myCopy2(pzzle)
        np1=H1(slideLeft(np))

        if np0>=np1:
            return 0
        return 3
    
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

    # This is for dynamic maxdepth to help with the speed problem
    # This is the variable that holds the difference of max depth
    changeval = 2

    # This gets the amount of spaces available
    h = H1(puzzle)
    if h <= 8:
        # If there is less than half left then switch to a deeper depth
        changeval = 1
    elif h < 5:
        # If there is only a few left go even deeper
        changeval = 0

    if depth >= MAX_DEPTH - changeval or c_time>TIME_MAX:
        move=node.getMove()
        evaluate=evaluateh(node,puzzle,move)

        val=value(node,evaluate)
        
        return val
    
    for a in [1,2,0,3]:
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
    h=H1(puzzle)
    if h==0:
        move=node.getMove()
        evaluate = MINUS_INFINITY + evaluateh(node,puzzle,move)

        val=value(node,evaluate)
        
        return val
    
    for move in range(16):
        copy=myCopy2(puzzle) 

        if(copy[move][0]==0):
            # This is a list that holds the possible values the computer will use. It default holds just 2 for speed
            movevals = [2]

            # If there are only three available spots left, add 4 to the list of possibles
            if h <= 3:
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


def H1(puzzle):
    # This gets the number of free spaces. (Made in class)

    count = 0
    for i in puzzle:
        if i[0] == 0:
            count += 1

    return count


def H2(puzzle, move):
    # Gets the amount of merges done before the current puzzle to now

    copy = myCopy2(puzzle)
    numFree = H1(puzzle)  # number of free spaces before move
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


def H3(puzzle):
    # This tries to get all the higher values towards the bottom

    # row vals
    rv = []

    # Goes through each of the rows
    for a in range(4):
        # The value of the row
        val = 0
        # Goes through each item in the row
        for b in range(4):
            # Gets the value
            itemval = puzzle[(a * 4) + b][0]

            # Adds it to the overall row val
            val += itemval

        # Adds the rowval to rowvals
        rv.append(val)

    # Used later to determine if the rows are in order
    good = True

    # This is used to hold the previous rows value
    lastrowval = -1

    # This is the total value of all rows
    totalval = 0

    # Goes through each rowval
    for rowval in rv:
        # If the new row is less than the last row then then it is not in order
        if rowval < lastrowval:
            good = False
        # Sets lastrowval to be the current row
        lastrowval = rowval

        # Adds the rowval to the total
        totalval += rowval

    # If it is in order return the total
    if good:
        return totalval

    # If it is not in order then return nothing
    return 0


def H4(puzzle):
    # This gets the amount of higher valued things

    # This is the value returned at the end
    val = 0

    # This will hold the values currently on the board and the number of times they appear
    nums = {}

    # Go through each item in the puzzle
    for i in range(len(puzzle)):
        # Gets the value
        itemval = puzzle[i][0]
        # If the value is not zero
        if itemval != 0:
            # If the item is already in the dictionary
            if itemval in nums:
                # Add one to the number of appearences
                nums[itemval] += 1
            else:
                # If it isnt then add it and set the val to 1
                nums[itemval] = 1

    # For each key in the dictionary
    for key in nums:
        # Gets the number of times the number appears
        num = nums[key]

        # Does some math to make sure the higher value is valued more than multiple small values
        val += (math.log2(key) ** 3) * num

    # Returns the total value of all numbers and their appearences
    return val


def H5(puzzle):
    # This tries to get rows in the order from greatest on the left to least on right

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

            # This is for when zeros are leading
            start = False

            # If we hit an item that not zero that is the start
            if itemval != 0:
                start = True

            # The a3 part is to make sure there are as little 0s in the bottom row as possible
            if start or a == 3:
                # If the lastval is less than the new val the row is bad
                if checkval < itemval:
                    rowgood = False
                else:
                    # If it is good then set the next checkval
                    checkval = itemval
        # If the row is in order, add the rows val to the return val
        if rowgood:
            val += rowval
    # Return the total vals of the good rows
    return val


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
                        val += cell[0]/2
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
                            if not (rcv2 - 3 < rcv < rcv2 + 3):
                                # If they are add to the numbad
                                numbad += 1
                except:
                    val += 0
            # If the number of bad spaces is over half
            if numbad > 2:
                # Subtract from the eval total
                val -= cell[0]
    # Return the total val
    return val

def H8(puzzle):
    # This tries to get all the higher value on the bottom row

    # Other row vals
    orv = []

    # Goes through each row
    for a in range(4):
        # This is the rows val
        val = 0

        # For each item in the row
        for b in range(4):
            # Gets the items val
            itemval = puzzle[(a * 4) + b][0]

            # Adds the val to the rowtotal
            val += itemval
        # If the rows is not the bottom, add it to the other row list
        if a != 3:
            orv.append(val)
        else:
            # If it is the bottom row, check to make sure the bottom row has the highest value
            if val >= max(orv):
                # If it is return the value of the row
                return val
    # If it isnt the highest row then return nothing
    return 0

def H9(puzzle):
    # Tries to get the ai to have the biggest value in the bottom left corner

    # Gets the bottom left row
    box = puzzle[12][0]

    # Gets the biggest cell in the puzzle
    bc = biggestCell(puzzle)

    # If the biggest val is not in the bottom left, return double the negative of the biggest value
    if box != bc:
        return -(bc * 2)
    else:
        # else return nothing
        return 0

def H10(puzzle):
    # This goes straight for 2048. Washes out some other hueristics but does so to complete the main objective

    # Gets the biggest cells value
    val = biggestCell(puzzle)

    # If the value is 2048, return positive infinity
    if val == 2048:
        return PLUS_INFINITY
    else:
        # If it is not then this h is nothing
        return 0


def evaluateh(n, puzzle, move):
    # This is the function that adds all of the hueristics together
    return 1.0 * H1(puzzle) + 1.0 * H2(n.parent.puzzle, move) + 1.0 * H3(puzzle) + 1.0 * H4(puzzle) + 1.0 * H5(puzzle) + 1.0 * H6(puzzle) + 1.0 * H7(
        puzzle) + 1.0 * H8(puzzle) + 1.0 * H9(puzzle) + H10(puzzle)

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
