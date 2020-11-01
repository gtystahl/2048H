import random
import time
import sys
from Grid import Grid
from BaseAI import BaseAI
MINUS_INFINITY=-10000000
PLUS_INFINITY=10000000





    
class PlayerAI(BaseAI):
    


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
