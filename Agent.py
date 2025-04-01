import numpy as np
from Board import Board
import random

class Agent:
    """
        The agent can only take 4 decisions (up/down/left/right).
    """
    def __init__(self, action_size = 4, learning_rate=0.5, discount_factor=0.95, exploration_rate=1.0, exploration_decay=0.95, min_exploration_rate=0.1):
        self.reward = 0
        self.action_size = action_size
        self.state = 0
        self.q_table = {}
        self.num_of_episodes = 0
        self.max_steps_per_episode = 0
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.exploration_decay = exploration_decay
        self.min_exploration_rate = min_exploration_rate
        self.board = Board()
        self.last_move = -1
        self.step_mode = 0
    
    def get_reward(self):
        GREEN_APPLE_REWARD = 50
        RED_APPLE_REWARD = -10
        EMPTY_MOVE_REWARD = -1
        DEATH_REWARD = -100
        GREEN_DIRECTION_REWARD = 10

        if self.last_move == -1:
            return 0
        elif self.board.death:
            return DEATH_REWARD
        elif self.board.snake_pos[0] == self.board.green1_pos or self.board.snake_pos[0] == self.board.green2_pos:
            return GREEN_APPLE_REWARD
        elif self.board.red_pos == self.board.snake_pos[0]:
            return RED_APPLE_REWARD
        elif self.state[self.last_move] == 3:
            return GREEN_DIRECTION_REWARD
        elif self.state[self.last_move] != 3:
            return EMPTY_MOVE_REWARD
        

    def get_q_value(self, state, action):
        """Get Q-value for a state-action pair"""
        # Use state directly if it's already a tuple
        state_key = state if isinstance(state, tuple) else tuple(state)
        
        # If state not in Q-table, add it with zeros for all actions
        if state_key not in self.q_table:
            self.q_table[state_key] = np.zeros(self.action_size)
            
        return self.q_table[state_key][action]
    
    def update_q_value(self, state, action, reward, next_state):
        """Update Q-value using the Q-learning formula"""
        state_tuple = tuple(map(tuple, state)) if isinstance(state, np.ndarray) else tuple(state)
        next_state_tuple = tuple(map(tuple, next_state)) if isinstance(next_state, np.ndarray) else tuple(next_state)
        
        # If states not in Q-table, add them
        if state_tuple not in self.q_table:
            self.q_table[state_tuple] = np.zeros(self.action_size)
        if next_state_tuple not in self.q_table:
            self.q_table[next_state_tuple] = np.zeros(self.action_size)
        
        # Calculate the best future value
        best_future_value = np.max(self.q_table[next_state_tuple])
        
        # Current Q-value
        current_q = self.q_table[state_tuple][action]
        
        # Calculate new Q-value using the Q-learning formula
        # Q(s,a) = Q(s,a) + α * [R + γ * max(Q(s',a')) - Q(s,a)]
        new_q = current_q + self.learning_rate * (reward + self.discount_factor * best_future_value - current_q)
        
        # Update Q-table
        self.q_table[state_tuple][action] = new_q
    
    def chose_action(self, state):
        """chose action using epsilon-greedy policy"""
        # Convert state to a hashable tuple if it's not already
        if isinstance(state, np.ndarray):
            state_key = tuple(state.flatten())
        elif isinstance(state, tuple):
            # If it's a tuple containing numpy arrays, convert them to tuples
            state_key = tuple(tuple(x) if isinstance(x, np.ndarray) else x for x in state)
        else:
            state_key = state
        
        if state_key not in self.q_table:
            self.q_table[state_key] = np.zeros(self.action_size)
        
        # Exploration: chose a random action
        if random.random() < self.exploration_rate:
            return random.randint(0, self.action_size - 1)
        # Exploitation: chose the action with highest Q-value
        else:
            return np.argmax(self.q_table[state_key])
    
    def decay_exploration(self):
        """Decay the exploration rate"""
        self.exploration_rate = max(self.min_exploration_rate, self.exploration_rate * self.exploration_decay)
    
    def save_q_table(self, filename):
        """Save Q-table to file using pickle instead of numpy.save"""
        import pickle
        with open(filename, 'wb') as f:
            pickle.dump(self.q_table, f)
    
    def load_q_table(self, filename):
        """Load Q-table from file using pickle instead of numpy.load"""
        import pickle
        with open(filename, 'rb') as f:
            self.q_table = pickle.load(f)
    
    def get_state(self):
            """
                Takes the visible board and returns the closest tile or the closest green apple
                if there is no obstacle between the snake's head and the apple.
            """
            first_object_west = 0
            first_object_east = 0
            first_object_north = 0
            first_object_south = 0

            """
                Pour chaque direction, verifie si pommeVerte.
                Obstacles potentiels: pomme rouge, queue.
                Pomme rouge se verifie en comparant les coordonnées avec la pomme verte.
                Queue se vérifie en regardant d'abord si présente dans la direction.
                Si oui enregistrer coordonnées, comparer avec coordonnées pomme verte.

                Si obstacle présent ou si pas de pomme verte, donner case la plus proche.
            """
            if self.board.green1_pos[0] == self.board.snake_pos[0][0]:
                first_object_west = self.green1_west()
                first_object_east = self.green1_east()
            elif self.board.green1_pos[1] == self.board.snake_pos[0][1]:
                first_object_north = self.green1_north()
                first_object_south = self.green1_south()
            
            if self.board.green2_pos[0] == self.board.snake_pos[0][0]:
                if first_object_west != 3:
                    first_object_west = self.green2_west()
                if first_object_east != 3:
                    first_object_east = self.green2_east()
            if self.board.green2_pos[1] == self.board.snake_pos[0][1]:
                if first_object_south != 3:
                    first_object_south = self.green2_south()
                if first_object_north != 3:
                    first_object_north = self.green2_north()
            
            if first_object_east == 0:
                first_object_east = self.board.board[self.board.snake_pos[0][0], self.board.snake_pos[0][1] + 1]
            if first_object_west == 0:
                first_object_west = self.board.board[self.board.snake_pos[0][0], self.board.snake_pos[0][1] - 1]
            if first_object_south == 0:
                first_object_south = self.board.board[self.board.snake_pos[0][0] + 1, self.board.snake_pos[0][1]]
            if first_object_north == 0:
                first_object_north = self.board.board[self.board.snake_pos[0][0] - 1, self.board.snake_pos[0][1]]
            self.state = (first_object_west, first_object_east, first_object_north, first_object_south)
            return (first_object_west, first_object_east, first_object_north, first_object_south)

    def green1_west(self):
        obstacle = False
        if self.board.green1_pos[1] < self.board.snake_pos[0][1]:# pomme verte west.
            if self.board.green1_pos[0] != self.board.red_pos[0] or self.board.green1_pos[1] > self.board.red_pos[1] or self.board.red_pos[1] > self.board.snake_pos[0][1]:# rouge pas entre verte et tete
                for i in range(len(self.board.snake_pos)):
                    if i > 0:#snake body between green and head
                        if self.board.snake_pos[i][0] == self.board.snake_pos[0][0] and self.board.green1_pos[1] < self.board.snake_pos[i][1] and self.board.snake_pos[0][1] > self.board.snake_pos[i][1]:
                            obstacle = True
            else:
                obstacle = True
            if obstacle:
                return self.board.board[self.board.snake_pos[0][0], self.board.snake_pos[0][1] - 1]
            else:
                return self.board.board[self.board.green1_pos]
        return 0
    
    def green2_west(self):
        obstacle = False
        if self.board.green2_pos[1] < self.board.snake_pos[0][1]:# pomme verte west.
            if self.board.green2_pos[0] != self.board.red_pos[0] or self.board.green2_pos[1] > self.board.red_pos[1] or self.board.red_pos[1] > self.board.snake_pos[0][1]:# rouge pas entre verte et tete
                for i in range(len(self.board.snake_pos)):
                    if i > 0:#snake body between green and head
                        if self.board.snake_pos[i][0] == self.board.snake_pos[0][0] and self.board.green2_pos[1] < self.board.snake_pos[i][1] and self.board.snake_pos[0][1] > self.board.snake_pos[i][1]:
                            obstacle = True
            else:
                obstacle = True
            if obstacle:
                return self.board.board[self.board.snake_pos[0][0], self.board.snake_pos[0][1] - 1]
            else:
                return self.board.board[self.board.green2_pos]
        return 0
    
    def green1_east(self):
        obstacle = False
        if self.board.green1_pos[1] > self.board.snake_pos[0][1]:
            if self.board.green1_pos[0] != self.board.red_pos[0] or self.board.green1_pos[1] < self.board.red_pos[1] or self.board.red_pos[1] < self.board.snake_pos[0][1]:# rouge pas entre verte et tete
                for i in range(len(self.board.snake_pos)):
                    if i > 0:#snake body between green and head
                        if self.board.snake_pos[i][0] == self.board.snake_pos[0][0] and self.board.green1_pos[1] > self.board.snake_pos[i][1] and self.board.snake_pos[0][1] < self.board.snake_pos[i][1]:
                            obstacle = True
            else:
                obstacle = True
            if obstacle:
                return self.board.board[self.board.snake_pos[0][0], self.board.snake_pos[0][1] + 1]
            else:
                return self.board.board[self.board.green1_pos]
        return 0
    
    def green2_east(self):
        obstacle = False
        if self.board.green2_pos[1] > self.board.snake_pos[0][1]:
            if self.board.green2_pos[0] != self.board.red_pos[0] or self.board.green2_pos[1] < self.board.red_pos[1] or self.board.red_pos[1] < self.board.snake_pos[0][1]:# rouge pas entre verte et tete
                for i in range(len(self.board.snake_pos)):
                    if i > 0:#snake body between green and head
                        if self.board.snake_pos[i][0] == self.board.snake_pos[0][0] and self.board.green2_pos[1] > self.board.snake_pos[i][1] and self.board.snake_pos[0][1] < self.board.snake_pos[i][1]:
                            obstacle = True
            else:
                obstacle = True
            if obstacle:
                return self.board.board[self.board.snake_pos[0][0], self.board.snake_pos[0][1] + 1]
            else:
                return self.board.board[self.board.green2_pos]
        return 0
    
    def green1_north(self):
        obstacle = False
        if self.board.green1_pos[0] < self.board.snake_pos[0][0]:
            if self.board.green1_pos[1] != self.board.red_pos[1] or self.board.green1_pos[0] > self.board.red_pos[0] or self.board.red_pos[0] > self.board.snake_pos[0][0]:
                for i in range(len(self.board.snake_pos)):
                    if i > 0:
                        if self.board.snake_pos[i][1] == self.board.snake_pos[0][1] and self.board.green1_pos[0] < self.board.snake_pos[i][0] and self.board.snake_pos[0][0] > self.board.snake_pos[i][0]:
                            obstacle = True
            else:
                obstacle = True
            if obstacle:
                return self.board.board[self.board.snake_pos[0][0] - 1, self.board.snake_pos[0][1]]
            else:
                return self.board.board[self.board.green1_pos]
        return 0
    
    def green2_north(self):
        obstacle = False
        if self.board.green2_pos[0] < self.board.snake_pos[0][0]:
            if self.board.green2_pos[1] != self.board.red_pos[1] or self.board.green2_pos[0] > self.board.red_pos[0] or self.board.red_pos[0] > self.board.snake_pos[0][0]:
                for i in range(len(self.board.snake_pos)):
                    if i > 0:
                        if self.board.snake_pos[i][1] == self.board.snake_pos[0][1] and self.board.green2_pos[0] < self.board.snake_pos[i][0] and self.board.snake_pos[0][0] > self.board.snake_pos[i][0]:
                            obstacle = True
            else:
                obstacle = True
            if obstacle:
                return self.board.board[self.board.snake_pos[0][0] - 1, self.board.snake_pos[0][1]]
            else:
                return self.board.board[self.board.green2_pos]
        return 0
    
    def green1_south(self):
        obstacle = False
        if self.board.green1_pos[0] > self.board.snake_pos[0][0]:# pomme verte west.
            if self.board.green1_pos[1] != self.board.red_pos[1] or self.board.green1_pos[0] < self.board.red_pos[0] or self.board.red_pos[0] < self.board.snake_pos[0][0]:# rouge pas entre verte et tete
                for i in range(len(self.board.snake_pos)):
                    if i > 0:#snake body between green and head
                        if self.board.snake_pos[i][1] == self.board.snake_pos[0][1] and self.board.green1_pos[0] > self.board.snake_pos[i][0] and self.board.snake_pos[0][0] < self.board.snake_pos[i][0]:
                            obstacle = True
            else:
                obstacle = True
            if obstacle:
                return self.board.board[self.board.snake_pos[0][0] + 1, self.board.snake_pos[0][1]]
            else:
                return self.board.board[self.board.green1_pos]
        return 0
    
    def green2_south(self):
        obstacle = False
        if self.board.green2_pos[0] > self.board.snake_pos[0][0]:# pomme verte west.
            if self.board.green2_pos[1] != self.board.red_pos[1] or self.board.green2_pos[0] < self.board.red_pos[0] or self.board.red_pos[0] < self.board.snake_pos[0][0]:# rouge pas entre verte et tete
                for i in range(len(self.board.snake_pos)):
                    if i > 0:#snake body between green and head
                        if self.board.snake_pos[i][1] == self.board.snake_pos[0][1] and self.board.green2_pos[0] > self.board.snake_pos[i][0] and self.board.snake_pos[0][0] < self.board.snake_pos[i][0]:
                            obstacle = True
            else:
                obstacle = True
            if obstacle:
                return self.board.board[self.board.snake_pos[0][0] + 1, self.board.snake_pos[0][1]]
            else:
                return self.board.board[self.board.green2_pos]
        return 0
    
    def perform_action(self, action_nb : int):
        if action_nb == 0:
            self.board.snake_move_west()
        elif action_nb == 1:
            self.board.snake_move_east()
        elif action_nb == 2:
            self.board.snake_move_north()
        elif action_nb == 3:
            self.board.snake_move_south()
        self.board.update_board()
        return self.get_state(), self.get_reward(), self.board.death
    
    def get_agent_board(self):
        return (self.board)

#train(num_episodes=1000000, qtable_filename="snake1000000.npy", decay=0.995)
# verif si reward correspond a action et state
# decalage mange pomme-recompense
