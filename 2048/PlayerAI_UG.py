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
    def __init__(self, hvals):
        self.hv = hvals

    def getMove(self, grid):
        puzzle=transformGrid(grid.map)
        node=Node(puzzle)
        
        alpha=value(None,MINUS_INFINITY)
        beta=value(None,PLUS_INFINITY)
        depth=0
        res=maxValue(node,alpha,beta,depth,time.clock(), self.hv)
        return  traceMove(res.getNode(),puzzle)


def maxValue(node,alpha,beta,depth,t_time, hv):
    
    "generate up(0) down(1) left(2) right(3) action nodes"
    

    
    puzzle=node.getPuzzle()

    c_time=time.clock()-t_time
    # c_time=0
    changeval = 2
    h = H1(puzzle)
    if h <= 8:
        changeval = 1
    elif h < 5:
        changeval = 0

    if depth >= MAX_DEPTH - changeval or c_time>TIME_MAX:
        move=node.getMove()
        evaluate=evaluateh(node,puzzle,move,hv)

        # debugDisplay(puzzle)

        val=value(node,evaluate)
        
        return val
    
    
    for a in [1,2,0,3]:
        copy=myCopy2(puzzle)

        # if depth == 0:
        #    print()
        
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
    
            temp=minValue(newNode,alpha,beta,depth,t_time, hv)

            # if depth == 0:
            #    print()

            if temp.value>alpha.value:
                alpha=temp

            if alpha.value>=beta.value:
                return beta
    return alpha

def minValue(node,alpha,beta,depth,t_time, hv):

    "generate up(0) down(1) left(2) right(3) action nodes"
    depth=depth+1

    
    puzzle=node.getPuzzle()
    h=H1(puzzle)
    if h==0:
        move=node.getMove()
        evaluate = MINUS_INFINITY + evaluateh(node,puzzle,move, hv)

        # debugDisplay(puzzle)

        val=value(node,evaluate)
        
        
        return val
    # elif h > 8:
    #    depth = MAX_DEPTH - 1
    
    for move in range(16):
        copy=myCopy2(puzzle) 

        if(copy[move][0]==0):
            movevals = [2]

            if h <= 3:
                movevals.append(4)

            for v in movevals:
                copy[move][0]=v
                newNode=Node(copy)
                newNode.setParent(node)


                temp=maxValue(newNode,alpha,beta,depth,t_time, hv)

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
    # This is the number of free spaces

    count = 0
    for i in puzzle:
        if i[0] == 0:
            count += 1

    return count


def H2(puzzle, move):
    # This tries to find merge number from this config

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

    for a in range(4):
        val = 0
        for b in range(4):
            rowval = puzzle[(a * 4) + b][0]
            val += rowval

        rv.append(val)

    good = True
    lastrowval = -1
    totalval = 0
    for rowval in rv:
        if rowval < lastrowval:
            good = False
        lastrowval = rowval
        totalval += rowval

    if good:
        return totalval

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
            start = False

            if itemval != 0:
                start = True

            if start or a == 3:
                if checkval < itemval:
                    rowgood = False
                else:
                    checkval = itemval
        if rowgood:
            val += rowval
    return val


def H6(puzzle):
    # Tries to get the same stuff next to each other
    val = 0
    for i in range(len(puzzle)):
        cell = puzzle[i]
        lst = [1, -1, 4, -4]
        for num in lst:
            try:
                loc = i + num
                if loc >= 0:
                    cell2 = puzzle[loc]
                    if cell[0] == cell2[0]:
                        #val += (cell[0] / 4)
                        val += cell[0]
                    # elif cell2[0]/2 == cell[0]:
                    #    val += (cell[0]/4)
            except:
                val += 0
    return val


def H7(puzzle):
    # tries to make sure that there arent stuff stuck where it cant be merged
    val = 0
    for i in range(len(puzzle)):
        cell = puzzle[i]
        if cell[0] != 0:
            # reduced cell val
            rcv = math.log2(cell[0])
            numbad = 0
            lst = [1, -1, 4, -4]
            for num in lst:
                try:
                    loc = i + num
                    if loc >= 0:
                        cell2 = puzzle[loc]
                        rcv2 = math.log2(cell2[0])
                        if not (rcv2 - 3 < rcv < rcv2 + 3):
                            numbad += 1
                        # elif cell2[0]/2 == cell[0]:
                        #    val += (cell[0]/4)
                except:
                    val += 0
            if numbad > 2:
                val -= cell[0]
    return val

def H8(puzzle):
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
            if val >= max(orv):
                return val
    return 0

def H9(puzzle):
    # Tries to get the ai to have the biggest value in the corner
    box = puzzle[12][0]
    bc = biggestCell(puzzle)
    if box != bc:
        return -(bc * 2)
    else:
        return 0

def H10(puzzle):
    # This goes straight for 2048
    val = biggestCell(puzzle)
    if val == 2048:
        return PLUS_INFINITY
    else:
        return 0

def evaluateh(n, puzzle, move, hv):
    return 1.0 * H1(puzzle) + 1.0 * H2(n.parent.puzzle, move) + (hv[0] + 1.0) * H3(puzzle) + (hv[1] + 1.0) * H4(puzzle) + (hv[2] + 1.0) * H5(puzzle) + (hv[3] + 1.0) * H6(puzzle) + (hv[4] + 1.0) * H7(
        puzzle) + (hv[0] + 1.0) * H8(puzzle) + (hv[5] + 1.0) * H9(puzzle) + H10(puzzle)

def biggestCell(puzzle):
    biggest = 0
    for i in range(len(puzzle)):
        if puzzle[i][0] > biggest:
            biggest = puzzle[i][0]
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
