from Agent import Agent
import numpy as np
import threading
from pynput.keyboard import Key, Listener
from time import sleep
from Game import Game

class Train:
    def __init__(self, num_episodes=1000, qtable_filename = "snake_q_table.npy", decay=0.995, agent= Agent(), rate = 0, is_ui_on= False):
        self.num_episodes = num_episodes
        self.qtable_filename = qtable_filename
        self.decay = decay
        self.agent = agent
        self.rate = rate
        self.is_running = True
        self.next_step = False
        self.listener = None
        self.t1 = threading.Thread(target= self.listen_for_keys, daemon= True)
        self.is_ui_on = is_ui_on
    
    def train(self):
        """
        Training loop for the Snake Q-learning agent
        
        Parameters:
        - get_state_function: Function that returns the current state of the game
        - perform_action_function: Function that performs an action and returns (next_state, reward, done)
        - num_episodes: Number of training episodes

        rate:   0 step-by-step
                1 human readable (5/s)
                2 computer speed
        """
        game = Game()
        self.t1.start()
        rewards_per_episode = []
        for episode in range(self.num_episodes):
            if self.is_ui_on:
                game.display_board(board=self.agent.get_agent_board())
            if self.is_running is False:
                exit(0)
            state = self.agent.get_state()
            episode_reward = 0
            state_list, action_list, reward_list, next_state_list = [], [], [], []
            while self.agent.board.death is False:
                if self.is_running is False:
                    exit(0)
                action = self.agent.chose_action(state)
                print(self.agent.board.get_board())
                self.agent.last_move = action
                print(action)
                next_state, reward, done = self.agent.perform_action(action)
                self.agent.board.is_eating_apple()
                if self.agent.board.death is False:
                    self.agent.board.update_board()
                state = next_state
                episode_reward += reward
                state_list.append(state)
                action_list.append(action)
                reward_list.append(reward)
                next_state_list.append(next_state)
                while self.rate == 0 and self.next_step is False:
                    pass
                if self.rate == 1:
                    sleep(1)
                self.next_step = False
            for i in range(len(state_list)):
                self.agent.update_q_value(state_list[i], action_list[i], reward_list[i], next_state_list[i])
            self.agent.decay_exploration()
            rewards_per_episode.append(episode_reward)
            self.agent.board.resurrect()
            
        self.is_running = False
        self.listener.stop()
        self.agent.save_q_table(self.qtable_filename)
        self.t1.join()
        return self.agent, rewards_per_episode
    
    def listen_for_keys(self):
        def on_release(key):
            if key == Key.space:
                self.rate = 0 if self.rate == 2 else self.rate + 1
                print(f"Rate changed to {self.rate}")
            elif key == Key.enter:
                self.next_step = True
            elif key == Key.esc or self.is_running is False:
                print("Exiting...")
                self.is_running = False
                exit(0)

        with Listener(on_release=on_release) as listener:
            self.listener = listener
            listener.join()
