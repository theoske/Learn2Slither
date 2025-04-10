from Agent import Agent
from time import sleep
import pygame
from pynput.keyboard import Key, Listener
import threading

TILE_SIZE = 50
title = "Learn2Slither"
wall = "sprites/wall.png"
s = "sprites/snake.png"
head = "sprites/head.png"
red = "sprites/red.png"
green = "sprites/green.png"


class Train:
    def __init__(self, num_episodes=1000,
                 qtable_filename="snake_q_table.npy",
                 decay=0.995, agent=Agent(), rate=0,
                 is_ui_on=False):
        self.num_episodes = num_episodes
        self.qtable_filename = qtable_filename
        self.decay = decay
        self.agent = agent
        self.rate = rate
        self.is_running = True
        self.next_step = False
        self.is_ui_on = is_ui_on
        if is_ui_on:
            pygame.init()
            self.screen = pygame.display.set_mode((TILE_SIZE * 12,
                                                   TILE_SIZE * 12))
            pygame.display.set_caption('Learn2Slither')
        else:
            self.t1 = threading.Thread(target=self.listen_for_keys,
                                       daemon=True)
            self.listener = None

    def train(self):
        """
        Training loop for the Snake Q-learning agent

        Parameters:
        - get_state_function: Function that returns the
            current state of the game
        - perform_action_function: Function that
            performs an action and
            returns (next_state, reward, done)
        - num_episodes: Number of training episodes

        rate:   0 step-by-step
                1 human readable
                2 computer speed
        """
        if self.is_ui_on:
            self.train_ui()
            return
        rewards_per_episode = []
        self.t1.start()
        for episode in range(self.num_episodes):
            if self.is_running is False:
                break
            state = self.agent.get_state()
            episode_reward = 0
            state_list = []
            action_list = []
            reward_list = []
            next_state_list = []
            while self.agent.board.death is False:
                if self.is_running is False:
                    break
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
                    if self.is_running is False:
                        break
                    sleep(0.01)
                if self.rate == 1:
                    sleep(1.5)
                self.next_step = False
            for i in range(len(state_list)):
                self.agent.update_q_value(state_list[i], action_list[i],
                                          reward_list[i], next_state_list[i])
            self.agent.decay_exploration()
            rewards_per_episode.append(episode_reward)
            self.agent.board.resurrect()
        while not self.listener:
            pass
        self.listener.stop()
        self.t1.join()
        self.agent.save_q_table(self.qtable_filename)

    def train_ui(self):
        """
            Copy of train function with ui made with pygame.
        """
        self.wall_sprite = pygame.image.load(wall).convert_alpha()
        self.snake_sprite = pygame.image.load(s).convert_alpha()
        self.head_sprite = pygame.image.load(head).convert_alpha()
        self.red_sprite = pygame.image.load(red).convert_alpha()
        self.green_sprite = pygame.image.load(green).convert_alpha()
        pygame.display.set_icon(self.head_sprite)

        clock = pygame.time.Clock()

        rewards_per_episode = []
        for episode in range(self.num_episodes):
            self.process_pygame_events()
            if not self.is_running:
                break
            state = self.agent.get_state()
            episode_reward = 0
            state_list = []
            action_list = []
            reward_list = []
            next_state_list = []
            while self.agent.board.death is False:
                self.process_pygame_events()
                if not self.is_running:
                    break
                action = self.agent.chose_action(state)
                print(self.agent.board.get_board())
                self.agent.last_move = action
                print(action)
                next_state, reward, done = self.agent.perform_action(action)
                self.agent.board.is_eating_apple()
                if self.agent.board.death is False:
                    self.agent.board.update_board()
                self.display_board(self.agent.board.get_board())
                state = next_state
                episode_reward += reward
                state_list.append(state)
                action_list.append(action)
                reward_list.append(reward)
                next_state_list.append(next_state)

                if self.rate == 0:
                    self.next_step = False
                    while self.rate == 0 and not self.next_step:
                        self.process_pygame_events()
                        if not self.is_running:
                            break
                        clock.tick(30)
                elif self.rate == 1:
                    clock.tick(2)
                else:
                    clock.tick(120)
                self.next_step = False
            if not self.is_running:
                break
            for i in range(len(state_list)):
                self.agent.update_q_value(state_list[i], action_list[i],
                                          reward_list[i], next_state_list[i])
            self.agent.decay_exploration()
            rewards_per_episode.append(episode_reward)
            self.agent.board.resurrect()

        self.is_running = False
        self.agent.save_q_table(self.qtable_filename)
        return self.agent, rewards_per_episode

    def display_board(self, board):
        self.screen.fill((0, 0, 0))
        for y in range(board.shape[0]):
            for x in range(board.shape[1]):
                value = board[y, x]
                if value == 0:
                    continue
                elif (value == 1):
                    sprite = self.snake_sprite
                elif (value == 2):
                    sprite = self.red_sprite
                elif (value == 3):
                    sprite = self.green_sprite
                elif (value == 4):
                    sprite = self.wall_sprite
                elif (value == 5):
                    sprite = self.head_sprite
                if sprite:
                    pos_x = x * TILE_SIZE
                    pos_y = y * TILE_SIZE
                    self.screen.blit(sprite, (pos_x, pos_y))
        pygame.display.flip()

    def process_pygame_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.rate = 0 if self.rate == 2 else self.rate + 1
                    print(f"Rate changed to {self.rate}")
                elif event.key == pygame.K_RETURN:
                    self.next_step = True
                elif event.key == pygame.K_ESCAPE:
                    print("Exiting...")
                    self.is_running = False
                    return

    def listen_for_keys(self):
        def on_release(key):
            if key == Key.space:
                self.rate = 0 if self.rate == 2 else self.rate + 1
                print(f"Rate changed to {self.rate}")
            elif key == Key.enter:
                self.next_step = True
            elif key == Key.esc or not self.is_running:
                print("Exiting...")
                self.is_running = False
                return

        with Listener(on_release=on_release) as listener:
            self.listener = listener
            listener.join()
