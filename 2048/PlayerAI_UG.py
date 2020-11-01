import random
import time
import sys
from Grid import Grid
from BaseAI import BaseAI
MINUS_INFINITY=-10000000
PLUS_INFINITY=10000000
Dmax=2
Tmax=.02




    
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
            evaluate=1.0*H1(puzzle)+1.0*H2(puzzle,move)

            return evaluate,move

        v=MINUS_INFINITY

        for a in [0,1,2,3]:

            copy=myCopy2(puzzle)
            
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

            if v2>v:
                v=v2
                move=a2

                alpha=max([v,alpha])
                
            if v>=beta:
                return v,move
                
        return v,move

    def minVal(self,puzzle,alpha,beta,move,depth):
        #evaluation function goes here  eval=1*H1(puzzle)
        depth+=1

        if depth>=Dmax:
            evaluate=1.0*H1(puzzle)+15.0/4.0*H2(puzzle,move)

            return evaluate,move

        v=PLUS_INFINITY

        for a in [0,1,2,3]:

            copy=myCopy2(puzzle)
            
            # copy is the next puzzle state
            if a==0:
                copy=slideUp(copy)
            elif a==1:
                copy=slideDown(copy)
            elif a==2:
                copy=slideLeft(copy)
            else:
                copy=slideRight(copy)

            
            v2,a2=self.maxVal(copy,alpha,beta,a,depth)

            if v2<v:
                v=v2
                move=a2

                beta=min([v,beta])
                
            if v<=alpha:
                return v,move
                
        return v,move

# count number of free spaces    
def H1(puzzle):
    count=0
    for i in puzzle:
        if i[0]==0:
            count+=1

    return count


def H2(puzzle,move):
    

    
    copy=myCopy2(puzzle)
    numFree=H1(puzzle)# number of free spaces before move
    if move==0:
        copy=slideUp(copy)
    elif move==1:
        copy=slideDown(copy)
    elif move==2:
        copy=slideLeft(copy)
    else:
        copy=slideRight(copy)

    curFree=H1(copy) # number of free tiles for speculative board

    diff=curFree-numFree# diff is the number of merges

    

    return diff
        
    
def myCopy2(s):
    n=[[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]

    for i in range(16):
        n[i][0]=s[i][0]

    return n








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
