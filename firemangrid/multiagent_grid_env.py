import gymnasium as gym
import numpy as np

from gymnasium import spaces
from enum import IntEnum
from abc import abstractmethod

from firemangrid.core.grid import Grid
from firemangrid.core.constants import *


class Action(IntEnum):
    '''
    Action space
    '''
    left = 0
    right = 1
    forward = 2
    press_button = 3
    toggle = 4
    hold = 5 # do nothing


class MultiAgentGridWorldEnv(gym.Env):
    '''
    2D grid world with multiple agents
    '''
    metadata = {
        "render_modes": ["human", "rgb_array"],
        "render_fps": 10,
        }
    
    def __init__(self, 
                 width:int = 10,
                 height: int = 10, 
                 num_agents: int = 2,
                 max_steps: int = 100,
                 render_mode: str = "rgb_array",):
        # Environment step settings
        self.step_cound = 0
        self.max_steps = max_steps
        self.width = width
        self.height = height
        self.button_pressed: [str] = []

        # Action space settings
        self.actions = Action
        self.action_space = spaces.Discrete(len(self.actions))

        # Agent settings
        self.n_agents: int = num_agents
        self.agents_pos: np.array | [(int, int)]= []
        self.agents_dir: [int] = []

        # Grid settings 
        self.grid = Grid(width, height)

        # Other settings
        self.render_mode = render_mode

    def reset(self, seed=None):
        super().reset(seed=seed)
        self.step_cound = 0 

        self.agents_pos = []
        self.agents_dir = []

        for agent_i in range(self.n_agents):
            self.agents_pos.append((-1, -1))
            self.agents_dir.append(-1)
        self._gen_grid(self.width, self.height) 

        # Agent initial positions, should be modified according to task
        start_cells = [self.grid.get(i) for i in self.agents_pos] 

        if self.render_mode == 'human':
            self.render() 
        n_obs = self.gen_obs() 
        return n_obs, {}

    def render(self, mode="human"):
        pass
    
    @abstractmethod
    def _gen_grid(self, width, height):
        pass

    def _gen_obs(self):
        '''
        Returns a list of ndarrays, each one for each agent
        '''
        n_obs = []
        original_obs = self.grid.encode()
        for agent_i in range(self.n_agents):
            obs_i = original_obs.copy()
            obs_i[self.agents_pos[agent_i][0], self.agents_pos[agent_i][1], :] = np.array(
                [OBJECT_TO_IDX["agent"], COLOR_TO_IDX["blue"], 0] # Agents see themselves as blue agents and see others as red agents
            )
            for agent_j in range(self.n_agents):
                if agent_i == agent_j:
                    continue
                obs_i[self.agents_pos[agent_j][0], self.agents_pos[agent_j][1], :] = np.array(
                    [OBJECT_TO_IDX["agent"], COLOR_TO_IDX["red"], 0]
                )
            n_obs.append(obs_i)
        return n_obs

    def _reward(self):
        # Sparse reward
        return 1-0.9*(self.step_cound/self.max_steps)
    
    def front_pos(self, pos, direction):
        '''
        Get the position in front of the agent
        '''
        return (pos[0] + DIR_TO_VEC[direction][0], pos[1] + DIR_TO_VEC[direction][1])
    
    def step(self, n_actions):
        assert len(n_actions) == self.n_agents
        self.step_cound += 1

        rewards = [0 for _ in range(self.n_agents)]
        terminated = False 
        truncated = False 

        n_fwd_pos = [self.front_pos(self.agents_pos[i], self.agents_dir[i]) for i in range(self.n_agents)] 
        n_fwd_cell = [self.grid.get(n_fwd_pos[i][0], n_fwd_pos[i][1]) for i in range(self.n_agents)]

        # TODO: add more tasks according to the task
        for agent_i in range(self.n_agents):
            if n_actions[agent_i] == self.actions.left: 
                self.agents_dir[agent_i] -= 1
                if self.agents_dir[agent_i] < 0:
                    self.agents_dir[agent_i] += 4
            
            elif n_actions[agent_i] == self.actions.right:
                self.agents_dir[agent_i] += 1 
                self.agents_dir[agent_i] %= 4 

            elif n_actions[agent_i] == self.actions.forward:
                if n_fwd_cell[agent_i] is None or n_fwd_cell[agent_i].can_overlap():
                    self.agents_pos[agent_i] = n_fwd_pos[agent_i]
                elif n_fwd_cell[agent_i] is not None and n_fwd_cell[agent_i].type == 'goal':
                    # rewards[agent_i] = self._reward()
                    terminated = True
                elif n_fwd_cell[agent_i] is not None and n_fwd_cell[agent_i].type == 'lava':
                    # rewards[agent_i] = -1
                    terminated = True 

            elif n_actions[agent_i] == self.actions.press_button:
                if n_fwd_cell[agent_i] is not None and n_fwd_cell[agent_i].type == 'button':
                    n_fwd_cell[agent_i].toggle(self) 
                    button_color = n_fwd_cell[agent_i].color
                    # TODO: add reward signals according to the task
            
            elif n_actions[agent_i] == self.actions.toggle:
                if n_fwd_cell[agent_i] is not None:
                    n_fwd_cell[agent_i].toggle(self) 
                    #TODO: add reward signals according to the task 
            
            elif n_actions[agent_i] == self.actions.hold:
                pass 
        
        if self.step_cound >= self.max_steps:
            truncated = True
        n_obs = self._gen_obs()

        return rewards, n_obs, terminated, truncated, {}
                