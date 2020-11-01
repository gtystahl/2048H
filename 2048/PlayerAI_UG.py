import random
import time
import sys
from Grid import Grid
from BaseAI import BaseAI
import math
MINUS_INFINITY=-10000000
PLUS_INFINITY=10000000
Dmax=6
Tmax=.02
possiblenexts = [2, 4]




    
class PlayerAI(BaseAI):
    def __init__(self):
        self.board=0


    def getMove(self,grid):
        move=0
        puzzle=transformGrid(grid.map)
        # max min with alpha beta pruning
        depth=0
        V,move=self.maxVal(puzzle,MINUS_INFINITY,PLUS_INFINITY,move,depth)

        return move
    
    def maxVal(self,puzzle,alpha,beta,move,depth):
        #evaluation function goes here  eval=1*H1(puzzle)
        depth+=1

        if depth>=Dmax:
            evaluate = evaluateh(puzzle, move)

            return evaluate,move

        v=MINUS_INFINITY

        for a in [0,1,2,3]:

            copy = myCopy2(puzzle)
            
            # copy is the next puzzle state
            if a==0:
                copy=slideUp(copy)
            elif a==1:
                copy=slideDown(copy)
            elif a==2:
                copy=slideLeft(copy)
            else:
                copy=slideRight(copy)

            
            v2,a2=self.minVal(copy,alpha,beta,a,depth)

            v2 += H2(puzzle, a)

            if v2>v:
                v=v2
                move=a

                alpha=max([v,alpha])
                
            if v>=beta:
                return v,move
                
        return v,move

    def minVal(self,puzzle,alpha,beta,move,depth):
        #evaluation function goes here  eval=1*H1(puzzle)
        depth+=1

        if depth>=Dmax:
            evaluate = evaluateh(puzzle, move)

            return evaluate,move

        v=PLUS_INFINITY

        cells = availablecells(puzzle)
        if not cells:
            return MINUS_INFINITY, move

        # Need to find a way to return the percentage of failure
        for cellnum in cells:
            for val in possiblenexts:
                copy = myCopy2(puzzle)
                copy[cellnum][0] = val

                v2,a2=self.maxVal(copy,alpha,beta,move,depth)

                if v2<v:
                    v=v2
                    move=a2

                    beta=min([v,beta])

                
        return v,move


def H1(puzzle):
    # This is the number of free spaces

    count = 0
    for i in puzzle:
        if i[0] == 0:
            count += 1

    return count


def H2(puzzle,move):
    # This tries to find merge number from this config

    copy = myCopy2(puzzle)
    numFree = H1(puzzle) # number of free spaces before move
    if move==0:
        copy=slideUp(copy)
    elif move==1:
        copy=slideDown(copy)
    elif move==2:
        copy=slideLeft(copy)
    else:
        copy=slideRight(copy)

    curFree=H1(copy) # number of free tiles for speculative board

    diff=curFree-numFree # diff is the number of merges

    

    return diff


def H3(puzzle):
    # This tries to get all the higher value on the bottom

    # Other row vals
    orv = []

    for a in range(4):
        val = 0
        for b in range(4):
            rowval = puzzle[(a * 4) + b][0]
            val += rowval

        if a != 3:
            orv.append(val)
        else:
            if val > max(orv):
                return val
    return 0


def H4(puzzle):
    # This gets the amount of higher valued things
    val = 0
    nums = {}

    for i in range(len(puzzle)):
        itemval = puzzle[i][0]
        if itemval != 0:
            if itemval in nums:
                nums[itemval] += 1
            else:
                nums[itemval] = 1

    for key in nums:
        num = nums[key]
        val += (math.log2(key) ** 3) * num

    return val


def H5(puzzle):
    # This tries to get rows in the order from greatest on the left to least on right
    val = 0
    for a in range(4):
        rowgood = True
        checkval = PLUS_INFINITY
        rowval = 0
        for b in range(4):
            itemval = puzzle[(a * 4) + b][0]
            rowval += itemval
            if itemval != 0:
                if checkval < itemval:
                    rowgood = False
                else:
                    checkval = itemval
        if rowgood:
            val += rowval
    return val


def evaluateh(puzzle, move):
    return 1.0*H1(puzzle) + 1.0*H3(puzzle) + 1.0*H4(puzzle) + 1.0*H5(puzzle)


def myCopy2(s):
    n=[[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]

    for i in range(16):
        n[i][0]=s[i][0]

    return n

def availablecells(puzzle):
    cells = []

    for i in range(len(puzzle)):
        cell = puzzle[i]
        if cell[0] == 0:
            cells.append(i)

    return cells






def isSame(s1,s2):
    for i in range(16):
        if s1[i][0]!=s2[i][0]:
            return False
    return True

def reset(s):
    for i in range(16):
        s[i][1]=0
        
    
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
