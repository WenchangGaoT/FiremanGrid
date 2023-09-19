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
        self.task = task

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

        fire_pos = (7, 3)
        fe_pos = (11, 3)
        key_pos = (2, 10)
        debris_pos = (5, 8) 
        door_pos = (5, 2)


        self.grid.set(5, 2, Door('yellow'))   
        if not (self.task == 'fire2start' or self.task == 'fire2key' or self.task == 'fire2door' or self.task == 'fire2fireextinguisher' or self.task == 'fire2debris' or self.task == 'fire2survivor'):
            self.grid.set(*fire_pos, Fire())

        if not (self.task == 'fireextinguisher2start' or self.task == 'fireextinguisher2key' or self.task == 'fireextinguisher2door' or self.task == 'fireextinguisher2fire' or self.task == 'fireextinguisher2debris' or self.task == 'fireextinguisher2survivor'):
            self.grid.set(*fe_pos, FireExtinguisher())  

        if not (self.task == 'key2start' or self.task == 'key2door' or self.task == 'key2fireextinguisher' or self.task == 'key2fire' or self.task == 'key2debris' or self.task == 'key2survivor'):
            self.grid.set(*key_pos, Key('yellow')) 
        if not (self.task == 'debris2start' or self.task == 'debris2key' or self.task == 'debris2door' or self.task == 'debris2fireextinguisher' or self.task == 'debris2fire' or self.task == 'debris2survivor'):
            self.grid.set(*debris_pos, Debris())

        survivor_x = np.random.choice([1, 2, 3, 4])
        survivor_y = np.random.choice([1, 2, 3, 4]) 
        self.grid.set(survivor_x, survivor_y, Survivor())

        for i in range(9, 12):
            for j in range(9, 12):
                self.grid.set(i, j, Start())

        # Initialize the agent 
        if self.task == 'start2key' or self.task == 'start2door' or self.task == 'start2fireextinguisher' or self.task == 'start2fire' or self.task == 'start2debris' or self.task == 'start2survivor':
            init_canditates = [] 
            for i in range(1, width-1): 
                for j in range(1, height-1): 
                    if isinstance(self.grid.get(i, j), Start): 
                        init_canditates.append((i, j)) 
        
            self.agent_pos = init_canditates[np.random.choice(len(init_canditates))] 

        if self.task == 'key2start' or self.task == 'key2door' or self.task == 'key2fireextinguisher' or self.task == 'key2fire' or self.task == 'key2debris' or self.task == 'key2survivor':
            self.agent_pos = key_pos
        
        if self.task == 'door2start' or self.task == 'door2key' or self.task == 'door2fireextinguisher' or self.task == 'door2fire' or self.task == 'door2debris' or self.task == 'door2survivor':
            self.agent_pos = door_pos
        
        if self.task == 'fireextinguisher2start' or self.task == 'fireextinguisher2key' or self.task == 'fireextinguisher2door' or self.task == 'fireextinguisher2fire' or self.task == 'fireextinguisher2debris' or self.task == 'fireextinguisher2survivor':
            self.agent_pos = fe_pos
        
        if self.task == 'fire2start' or self.task == 'fire2key' or self.task == 'fire2door' or self.task == 'fire2fireextinguisher' or self.task == 'fire2debris' or self.task == 'fire2survivor':
            self.agent_pos = fire_pos
        
        if self.task == 'debris2start' or self.task == 'debris2key' or self.task == 'debris2door' or self.task == 'debris2fireextinguisher' or self.task == 'debris2fire' or self.task == 'debris2survivor':
            self.agent_pos = debris_pos
        
        # self.agent_pos = init_canditates[np.random.choice(len(init_canditates))] 
        print(self.agent_pos)
        
        self.agent_dir = np.random.choice(len(DIR_TO_VEC))
        # print(self.agent_dir)
        
    def reset(self, seed=None, options=None):
        super().reset(seed=seed) 
        self.agent_pos = (-1, -1)
        self.agent_dir = -1 
        self.step_count = 0

        self._gen_grid(self.grid_size, self.grid_size)

        # Check some conditions
        assert self.agent_pos[0] >= 0 and self.agent_pos[0] < self.grid.width
        assert self.agent_pos[1] >= 0 and self.agent_pos[1] < self.grid.height 
        assert self.agent_dir >= 0 and self.agent_dir < len(DIR_TO_VEC) 

        self.carrying = None 

        # TODO: Add starting states based on the graph environment 

        if self.task == 'key2start' or self.task == 'key2door' or self.task == 'key2fireextinguisher' or self.task == 'key2fire' or self.task == 'key2debris' or self.task == 'key2survivor':
            self.carrying = Key('yellow') 
        
        if self.task == 'fireextinguisher2start' or self.task == 'fireextinguisher2key' or self.task == 'fireextinguisher2door' or self.task == 'fireextinguisher2fire' or self.task == 'fireextinguisher2debris' or self.task == 'fireextinguisher2survivor':
            self.carrying = FireExtinguisher()

        if self.render_mode == 'human':
            self.render() 

        obs = self.observation()
        return obs, {} 
    
    