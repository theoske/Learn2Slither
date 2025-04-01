from Agent import Agent
import numpy as np
import threading
import keyboard

class Train:
    def __init__(self, num_episodes=1000, qtable_filename = "snake_q_table.npy", decay=0.995, agent= Agent(), cadence = 0):
        self.num_episodes = num_episodes
        self.qtable_filename = qtable_filename
        self.decay = decay
        self.agent = agent
        self.cadence = cadence
        self.t1 = threading.Thread(self.change_cadence)
        self.is_running = True
    
    def train(self):
        """
        Training loop for the Snake Q-learning agent
        
        Parameters:
        - get_state_function: Function that returns the current state of the game
        - perform_action_function: Function that performs an action and returns (next_state, reward, done)
        - num_episodes: Number of training episodes

        cadence:    0 step-by-step
                    1 human readable (5/s)
                    2 computer speed
        """
        self.t1.start()
        rewards_per_episode = []
        
        for episode in range(self.num_episodes):
            state = self.agent.get_state()
            episode_reward = 0
            state_list, action_list, reward_list, next_state_list = [], [], [], []
            while self.agent.board.death is False:
                action = self.agent.chose_action(state)
                self.agent.last_move = action
                next_state, reward, done = self.agent.perform_action(action)
                #print(f"State: {state}, Action: {action}, Reward: {reward}")#recompense de laction quil fait dans un etat
                self.agent.board.is_eating_apple()
                if (self.agent.board.death is False):
                    self.agent.board.update_board()
                state = next_state
                episode_reward += reward
                state_list.append(state)
                action_list.append(action)
                reward_list.append(reward)
                next_state_list.append(next_state)
            for i in range(len(state_list)):
                self.agent.update_q_value(state_list[i], action_list[i], reward_list[i], next_state_list[i])
            self.agent.decay_exploration()
            rewards_per_episode.append(episode_reward)
            interval = (int)(self.num_episodes/10)
            if interval > 0 and episode % interval == 0:
                avg_reward = np.mean(rewards_per_episode[-interval:]) if len(rewards_per_episode) >= interval else np.mean(rewards_per_episode)
                print(f"Episode: {episode}, Average Reward: {avg_reward:.2f}, Exploration Rate: {self.agent.exploration_rate:.2f}")
            self.agent.board.resurrect()
        self.is_running = False
        # Save the trained Q-table
        self.agent.save_q_table(self.qtable_filename)
        self.t1.join()
        return self.agent, rewards_per_episode
    
    def change_cadence(self):
        while self.is_running:
            if keyboard.is_pressed("\n"):
                self.cadence = 0 if self.cadence == 3 else self.cadence + 1