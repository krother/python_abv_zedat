# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 22:06:35 2017

@author: Benny
"""

import random as rnd


def printField(field):
    '''printField printes the Minesweeperfield'''
    
    for row in range(len(field)):
        print()
        for col in range(len(field[0])):
            print(field[row][col], end = "")

class Field:
    '''Field is a class for gameboards specially for Minesweeper'''
    def __init__(self, height, width, p):
        self.height     = height
        self.width      = width
        self.p          = p
        self.emptyfield = self.generateField()
        self.minedfield = self.mineplanting()
        self.solution   = self.generateSolution()
        
        
        
    def generateField(self):
        '''generateField generates an empty (with 0 filled) Field'''
        gamefield = []
        
        for height in range(self.height):
            row = []
            for width in range(self.width):
                row.append(0)
            gamefield.append(row)
        
        return gamefield

    
    def mineplanting(self):
        '''mineplanting plants randomly a given number of mines in a new field with the
        objects height and width'''
        
        minelist = []
        field = []
        
        while len(minelist) < self.p:
            mine_x = rnd.randint(0, self.width-1)
            mine_y = rnd.randint(0, self.height-1)
            if not (mine_x, mine_y) in minelist:
                minelist.append( (mine_x, mine_y) )
        
        for height in range(self.height):
            row = []
            for width in range(self.width):
                if (width, height) in minelist:
                    row.append("*")
                else:
                    row.append(0)
            field.append(row)
        
        return field
        
        
    
    def generateSolution(self):
        '''generateSolution generates the solution to the field, with the field
        as model'''
        
        solution = self.generateField()
        
        for height in range(self.height):
            row = solution[height]
            for width in range(self.width):
                if self.minedfield[height][width] == '*':
                    row[width] = '*'
                else:
                    if height == 0:                h = (0,1)
                    elif height == self.height-1:  h = (0,-1)
                    else:                          h = (-1,0,1)
                    
                    if width == 0:                 b = (0,1)
                    elif width == self.width-1:    b = (0,-1)
                    else:                          b = (-1,0,1)
                    
                    for i in h:
                        for j in b:
                            if self.minedfield[height+i][width+j] == '*':
                                row[width] += 1
                    
                    if row[width] == 0:
                        row[width] = '.'
        return solution


if __name__ == "__main__":
    gameBoard = Field(5, 10, 5)
    printField(gameBoard.emptyfield)
    print("\n")
    printField(gameBoard.minedfield)
    print("\n")
    printField(gameBoard.solution)
