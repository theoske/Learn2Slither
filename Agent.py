import numpy as np
from Board import Board

class Agent:
    """
        The agent can only take 4 decisions (up/down/left/right).
    """
    def __init__(self):
        self.reward = 0
        self.state = 0
        self.qtable = np.array((625, 4))
        self.num_of_episodes = 0
        self.max_steps_per_episode = 0
        self.learning_rate = 0
        self.discount_factor = 0
        self.exploration_rate = 0
        self.board = Board()

    def learn(self):
        for i in range(self.num_of_episodes):
            self.episode()
    
    def episode(self):
        for i in range(self.max_steps_per_episode):
            self.state = self.get_state()
            self.chose_action()
            self.get_reward()

    def chose_action(self):
        pass
    
    def get_reward(self):
        pass

    def save_state(self):
        pass

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
    
    def choose_action(self, state):
        """Choose action using epsilon-greedy policy"""
        # Convert state to tuple for dictionary lookup
        state_tuple = tuple(map(tuple, state)) if isinstance(state, np.ndarray) else tuple(state)
        
        # If this state hasn't been seen before, add it to the Q-table
        if state_tuple not in self.q_table:
            self.q_table[state_tuple] = np.zeros(self.action_size)
        
        # Exploration: choose a random action
        if random.random() < self.exploration_rate:
            return random.randint(0, self.action_size - 1)
        # Exploitation: choose the action with highest Q-value
        else:
            return np.argmax(self.q_table[state_tuple])
    
    def decay_exploration(self):
        """Decay the exploration rate"""
        self.exploration_rate = max(self.min_exploration_rate, self.exploration_rate * self.exploration_decay)
    
    def save_q_table(self, filename):
        """Save Q-table to file"""
        np.save(filename, self.q_table)
    
    def load_q_table(self, filename):
        """Load Q-table from file"""
        self.q_table = np.load(filename, allow_pickle=True).item()
    
    def train(get_state_function, perform_action_function, num_episodes=10000):
        """
        Training loop for the Snake Q-learning agent
        
        Parameters:
        - get_state_function: Function that returns the current state of the game
        - perform_action_function: Function that performs an action and returns (next_state, reward, done)
        - num_episodes: Number of training episodes
        """
        # Initialize Q-learning agent
        # Assuming 4 possible actions: 0=up, 1=right, 2=down, 3=left
        agent = SnakeQLearning(state_size=None, action_size=4)  
        
        # Training statistics
        rewards_per_episode = []
    
        for episode in range(num_episodes):
            # Reset the game
            state = get_state_function()  # This is your function that returns the game state
            episode_reward = 0
            done = False
            
            while not done:
                # Choose action
                action = agent.choose_action(state)
                
                # Perform action and get next state and reward
                next_state, reward, done = perform_action_function(action)  # This is your function
                
                # Update Q-table
                agent.update_q_value(state, action, reward, next_state)
                
                # Move to next state
                state = next_state
                
                # Accumulate reward
                episode_reward += reward
                
                # If game is over (snake crashed or reached max steps)
                if done:
                    break
            
            # Decay exploration rate
            agent.decay_exploration()
            
            # Record rewards
            rewards_per_episode.append(episode_reward)
        
        # Print progress every 100 episodes
        if episode % 100 == 0:
            avg_reward = np.mean(rewards_per_episode[-100:]) if len(rewards_per_episode) >= 100 else np.mean(rewards_per_episode)
            print(f"Episode: {episode}, Average Reward: {avg_reward:.2f}, Exploration Rate: {agent.exploration_rate:.2f}")
    
        # Save the trained Q-table
        agent.save_q_table("snake_q_table.npy")
        
        return agent, rewards_per_episode

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
            
            if self.board.green2_pos[0] == self.board.snake_pos[0][0] and first_object_west != 3:
                first_object_west = self.green2_west()
            elif self.board.green2_pos[0] == self.board.snake_pos[0][0] and first_object_east != 3:
                first_object_east = self.green2_east()
            if self.board.green2_pos[1] == self.board.snake_pos[0][1] and first_object_south != 3:
                first_object_south = self.green2_south()
            elif self.board.green2_pos[1] == self.board.snake_pos[0][1] and first_object_north != 3:
                first_object_north = self.green2_north()
            
            if first_object_east == 0:
                first_object_east = self.board.board[self.board.snake_pos[0][0], self.board.snake_pos[0][1] + 1]
            if first_object_west == 0:
                first_object_west = self.board.board[self.board.snake_pos[0][0], self.board.snake_pos[0][1] - 1]
            if first_object_south == 0:
                first_object_south = self.board.board[self.board.snake_pos[0][0] + 1, self.board.snake_pos[0][1]]
            if first_object_north == 0:
                first_object_north = self.board.board[self.board.snake_pos[0][0] - 1, self.board.snake_pos[0][1]]
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
    
    def green1_north(self):#a verifier
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
    
    def green2_north(self):#a verifier
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



