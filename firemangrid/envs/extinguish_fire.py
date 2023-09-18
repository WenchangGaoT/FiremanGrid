import numpy as np 
import gymnasium as gym 
import sys 

from firemangrid.core.grid import *
from firemangrid.core.constants import * 
from firemangrid.core.world_object import * 
from firemangrid.fireman_env import FiremanEnv


class ExtinguishFireEnv(FiremanEnv):
    def __init__(self, grid_size=10, max_steps=500, render_mode='rgb_array'):
        super().__init__(grid_size, max_steps, render_mode) 

    def _gen_grid(self, width, height):
        self.grid = Grid(width=width, height=height)

        for i in range(0, width):
            self.grid.set(i, 0, 'wall') 
            self.grid.set(i, width-1, 'wall') 
        
        for j in range(0, height):
            self.grid.set(0, j, 'wall') 
            self.grid.set(height-1, j, 'wall') 
        
        self.grid.set(3, 5, 'fire') 
        self.grid.set(6, 6, 'fireextinguisher') 
        self.grid.set(6, 3, 'fireextinguisher') 

        # Initialize the agent 
        init_canditates = [] 
        for i in range(1, width-1): 
            for j in range(1, height-1): 
                if self.grid.get(i, j) is None: 
                    init_canditates.append((i, j)) 
        
        self.agent_pos = init_canditates[np.random.choice(len(init_canditates))] 
        # print(self.agent_pos)
        self.agent_dir = np.random.choice(len(DIR_TO_VEC))
        # print(self.agent_dir)
        