import numpy as np 
import gymnasium as gym 
import sys 

from firemangrid.core.grid import *
from firemangrid.core.constants import * 
from firemangrid.core.world_object import * 
from firemangrid.fireman_env import FiremanEnv


class FiremanWholeEnv(FiremanEnv):
    def __init__(self, grid_size=13, max_steps=500, render_mode='rgb_array', task='start2key'):
        super().__init__(grid_size, max_steps, render_mode) 

    def _gen_grid(self, width, height):
        self.grid = Grid(width=width, height=height)

        # Walls
        for i in range(0, width):
            self.grid.set(i, 0, Wall()) 
            self.grid.set(i, width-1, Wall()) 
        
        for j in range(0, height):
            self.grid.set(0, j, Wall()) 
            self.grid.set(height-1, j, Wall()) 

        for i in range(1, 5):
            self.grid.set(i, 5, Wall())

        for j in range(1, 5):
            self.grid.set(5, j ,Wall())     

        for j in range(8, 12):
            self.grid.set(j, 8, Wall())

        for j in range(10, 12):
            self.grid.set(8, j, Wall()) 

        for i in range(5, 11):
            self.grid.set(4, i, Wall()) 
        # Lava
        for j in range(2, 8):
            self.grid.set(9, j, Lava())
        for j in range(2, 8):
            self.grid.set(8, j, Lava())
        for i in range(1, 4):
            self.grid.set(i, 8, Lava())
        self.grid.set(5, 5, Lava())
        self.grid.set(6, 8, Lava())

        self.grid.set(5, 2, Door('yellow'))   
        self.grid.set(7, 3, Fire()) 
        self.grid.set(11, 3, FireExtinguisher()) 
        self.grid.set(2, 10, Key('yellow')) 
        self.grid.set(5, 8, Debris())

        survivor_x = np.random.choice([1, 2, 3, 4])
        survivor_y = np.random.choice([1, 2, 3, 4]) 
        self.grid.set(survivor_x, survivor_y, Survivor())

        for i in range(9, 12):
            for j in range(9, 12):
                self.grid.set(i, j, Start())

        # Initialize the agent 
        init_canditates = [] 
        for i in range(1, width-1): 
            for j in range(1, height-1): 
                if isinstance(self.grid.get(i, j), Start): 
                    init_canditates.append((i, j)) 
        
        self.agent_pos = init_canditates[np.random.choice(len(init_canditates))] 
        # print(self.agent_pos)
        self.agent_dir = np.random.choice(len(DIR_TO_VEC))
        # print(self.agent_dir)
        