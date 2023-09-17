from copy import deepcopy
import numpy as np  

from firemangrid.core.constants import *


class Grid:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [None] * width * height 

    def copy(self):
        return deepcopy(self)
    
    def set(self, i, j, v):
        assert i >= 0 and i < self.width
        assert j >= 0 and j < self.height
        self.grid[j * self.width + i] = v

    def get(self, i, j):
        assert i >= 0 and i < self.width
        assert j >= 0 and j < self.height
        return self.grid[j * self.width + i]
    
    def render(self):
        pass 

    def encode(self):
        encoded = np.zeros((self.width, self.height, 3), dtype=np.uint8)

        for i in range(self.width):
            for j in range(self.height):
                v = self.get(i, j)
                if v is None:
                    encoded[i, j, 0] = OBJECT_TO_IDX['empty']
                    encoded[i, j, 1] = 0 
                    encoded[i, j, 2] = 0
                else: 
                    encoded[i, j, :] = v.encode()
        return encoded
        
        