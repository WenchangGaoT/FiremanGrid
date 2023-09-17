# TODO: Add more realistic rendering for each object
from firemangrid.core.constants import *
from firemangrid.utils.rendering import *


class WorldObj:
    '''
    Basic class for grid world objects
    '''

    def __init__(self, type: str, color: str = None):
        assert type in IDX_TO_OBJECT, f"Invalid object type: {type}"
        assert color is None or color in IDX_TO_COLOR, f"Invalid color: {color}"

        self.type = type
        self.color = color
        self.contains = None

        self.init_pos = None 
        self.cur_pos = None 
        
    def can_overlap(self): 
        # Whether this object can be overlapped
        return False 
    
    def can_pickup(self):
        # Whether this object can be picked up
        return False
    
    def can_spray(self):
        # Whether this object can be sprayed to 
        return False 
    
    def can_be_sprayed(self):
        return False
    
    def can_save(self):
        # Whether this object can be saved 
        return False 
    
    def can_toggle(self):
        return False
    
    def toggle(self, env, pos):
        return False 
    
    def spray(self, env, pos):
        return False 
    
    def render(self, img: np.ndarray):
        fill_coords(img, point_in_rect(0, 1, 0, 1), COLORS[self.color])
    
    def encode(self):
        return (OBJECT_TO_IDX[self.type], COLOR_TO_IDX[self.color], 0)
    
    @staticmethod
    def decode(type_idx, color_idx, state):
        obj_type = IDX_TO_OBJECT[type_idx]
        color = IDX_TO_COLOR[color_idx] 

        # TODO: Implement other objects first
        return WorldObj(obj_type, color)
    

class Goal(WorldObj):
    '''
    Goal position for agents
    '''

    def __init__ (self):
        super().__init__("goal", 'green')
    
    def can_overlap(self):
        return True 


class Door(WorldObj):
    '''
    A door that can be opened and closed
    '''

    def __init__(self, color, is_open=False, is_locked=False):
        super().__init__(f"{color}door", color)
        self.is_open = is_open
        self.is_locked = is_locked
    
    def toggle(self, env, pos):
        if self.is_locked:
            if self.color in env.buttons_pressed:
                self.is_locked = False
                self.is_open = True
                return True
            return False
        self.is_open = not self.is_open
        return True
    
    def can_overlap(self):
        return self.is_open 
    
    def can_toggle(self):
        return True
    
    def encode(self):
        if self.is_open: 
            state = 0
        elif self.is_locked:
            state = 2
        else:
            state = 1
        return (OBJECT_TO_IDX[self.type], COLOR_TO_IDX[self.color], state)


class Button(WorldObj):

    def __init__(self, color, is_pressed=False):
        super().__init__(f"{color}button", color)
        self.is_pressed = is_pressed

    def toggle(self, env, pos):
        if self.color not in env.buttons_pressed:
            env.buttons_pressed.append(self.color)
        return True
    
    def encode(self):
        return (OBJECT_TO_IDX[self.type], COLOR_TO_IDX[self.color], 0)


class Wall(WorldObj):
    
    def __init__(self):
        super().__init__("wall", 'grey')
        
    def can_overlap(self):
        return False


class Lava(WorldObj):
    
    def __init__(self):
        super().__init__("lava", 'red')
        
    def can_overlap(self):
        return False
    

class Fire(WorldObj):
    def __init__(self):
        super().__init__('fire', 'orange') 
    
    def can_overlap(self):
        return False

    def can_be_sprayed(self):
        return True


class FireExtinguisher(WorldObj):
    def __init__(self):
        super().__init__('fireextinguisher', 'blue') 

    def can_pickup(self):
        return True 
    
    def can_overlap(self):
        return False 
    
    def can_spray(self):
        return True 
    
    

class Survivor(WorldObj):
    def __init__(self, name='Survivor1'):
        super().__init__(name, color='purple') 

    def can_save(self):
        return True
    
    def can_overlap(self):
        return False
    

class Debris(WorldObj):
    def __init__(self, type: str, color: str = None):
        super().__init__('debris', 'black') 


class Start(WorldObj):
    '''
    The starting grid of the agent at the beginning 
    '''
    def __init__(self):
        super().__init__('start', 'white') 
    
    def can_overlap(self):
        return True