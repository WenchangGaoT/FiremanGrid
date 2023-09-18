from copy import deepcopy
import numpy as np  
import math

from firemangrid.core.constants import *
from firemangrid.utils.rendering import *


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
    
    def render(self, agent_pos, agent_dir, tile_size):
        if self.render_mode == 'human':
            w_px = self.width * tile_size
            h_px = self.height * tile_size
            img = np.zeros((w_px, h_px, 3), dtype=np.uint8) # The rendered image
            for i in range(self.height):
                for j in range(self.width):
                    cell = self.get(i, j)                    
                    xmin = i * tile_size 
                    ymin = j * tile_size
                    xmax = (i + 1) * tile_size
                    ymax = (j + 1) * tile_size 
                    if cell is not None:
                        cell.render(img[xmin:xmax, ymin:ymax, :]) 

                    if i == agent_pos[0] and j == agent_pos[1]:
                        # Render the agent with its direction
                        # These lines are copied and adapted from https://github.com/Farama-Foundation/Minigrid/blob/master/minigrid/core/grid.py
                        tri_fn = point_in_triangle(
                        (0.12, 0.19),
                        (0.87, 0.50),
                        (0.12, 0.81),
                    )
                        tri_fn = rotate_fn(tri_fn, cx=0.5, cy=0.5, theta=0.5 * math.pi * agent_dir)
                        fill_coords(img[xmin:xmax, ymin:ymax, :], tri_fn, (255, 0, 0))

            return img
        
        elif self.render_mode == 'rgb_array':
            # TODO: Implement this
            pass 

        elif self.render_mode == 'cli':
            img = np.zeros((self.width, self.height), dtype=np.uint8)
            for i in range(self.height):
                for j in range(self.width):
                    cell = self.get(i, j)
                    if cell is not None:
                        img[i, j] = cell.encode()[0]
                    if self.agent_pos[0] == i and self.agent_pos[1] == j:
                        img[i, j] = 20+agent_dir # Encode the agent's direction in cli
            return img

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
        
        