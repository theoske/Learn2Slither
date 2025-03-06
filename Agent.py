import numpy as np
from Board import Board

class Agent:
    """
        The agent can only take 4 decisions (up/down/left/right).
    """
    def __init__(self):
        self.reward = 0
        self.state = 0
        self.qtable = np.array((240, 4))
        self.num_of_episodes = 0
        self.max_steps_per_episode = 0
        self.learning_rate = 0
        self.discount_factor = 0
        self.exploration_rate = 0
        self.board = Board()

    def vision_to_state(self):
        visible_row, visible_column = self.board.get_agent_vision()
        has_reached_snake = False
        first_object_west = 0
        first_object_east = 0
        for object in visible_row:
            if object == 5:
                has_reached_snake = True
                continue
            if has_reached_snake is False and first_object_west != 3 and object != 0: #(a gauche)si pomme verte +proche non nulle met pomme verte sinon met juste plus proche
                first_object_west = object
            elif has_reached_snake is True and first_object_east == 0 and object == 3: #+ proche non nul == pomme verte
                first_object_east = object
            elif has_reached_snake is True:
                first_object_east = object
        first_object_north = 0
        first_object_south = 0
        has_reached_snake = False
        for object in visible_column:
            if object == 5:
                has_reached_snake = True
                continue
            if has_reached_snake is False and first_object_west != 3 and object != 0: #(a gauche)si pomme verte +proche non nulle met pomme verte sinon met juste plus proche
                first_object_west = object
            elif has_reached_snake is True and first_object_east == 0 and object == 3: #+ proche non nul == pomme verte
                first_object_east = object
            elif has_reached_snake is True:
                first_object_east = object
        return (first_object_west, first_object_east, first_object_north, first_object_south)

    def learn(self):
        for i in range(self.num_of_episodes):
            self.episode()
    
    def episode(self):
        for i in range(self.max_steps_per_episode):
            self.state = self.board.get_agent_vision()
            self.chose_action()
            self.get_reward()

    def chose_action(self):
        pass
    
    def get_reward(self):
        pass

    def save_state(self):
        pass



