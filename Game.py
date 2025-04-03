from Board import Board
import pygame
import cv2
from Agent import Agent
from pynput.keyboard import Key, Listener
import threading

TILE_SIZE = 50

class Game:
    """
        This class is used to play the snake game.
    """
    def __init__(self, rate= 0, is_ui_on= False):
        self.board = Board()
        pygame.init()
        self.grass_sprite = 0
        self.wall_sprite = 0
        self.snake_sprite = 0
        self.red_sprite =  0
        self.green_sprite = 0
        self.screen = pygame.display.set_mode((TILE_SIZE * 12, TILE_SIZE * 12))
        pygame.display.set_caption('SkibidiSlither')
        self.last_move = -1
        self.rate = rate
        self.next_step = False
        self.t1 = threading.Thread(target= self.listen_for_keys, daemon= True)
        self.is_ui_on = is_ui_on

    
    def game_loop(self):
        self.grass_sprite = pygame.image.load("sprites/grass.png").convert_alpha()
        self.wall_sprite = pygame.image.load("sprites/wall.png").convert_alpha()
        self.snake_sprite = pygame.image.load("sprites/snake.png").convert_alpha()
        self.head_sprite = pygame.image.load("sprites/head.png").convert_alpha()
        self.red_sprite =  pygame.image.load("sprites/red.png").convert_alpha()
        self.green_sprite = pygame.image.load("sprites/green.png").convert_alpha()
        pygame.display.set_icon(self.head_sprite)
        pygame.mixer.init()
        pygame.mixer.music.load('sprites/game_soundtrack.mp3')
        if not self.setup_camera_background():
            exit(0)
        while True:
            if pygame.mixer.music.get_busy() is False:
                pygame.mixer.music.play(-1, 0.0)
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.board.snake_move_north()
                    self.last_move = 2
                elif event.key == pygame.K_DOWN:
                    self.last_move = 3
                    self.board.snake_move_south()
                elif event.key == pygame.K_LEFT:
                    self.board.snake_move_west()
                    self.last_move = 0
                elif event.key == pygame.K_RIGHT:
                    self.board.snake_move_east()
                    self.last_move = 1
                elif event.key == pygame.K_ESCAPE:
                    exit(0)
            self.state = self.get_state()
            print(self.state)
            print(self.get_reward())
            self.board.is_eating_apple()
            if self.board.death:
                self.death_screen()
            self.board.update_board()
            self.display_board()
    
    def get_reward(self):
        GREEN_APPLE_REWARD = 50
        RED_APPLE_REWARD = -10
        EMPTY_MOVE_REWARD = -1
        DEATH_REWARD = -100
        GREEN_DIRECTION_REWARD = 10

        if self.last_move == -1:
            return 0
        elif self.board.ate_green:
            self.board.ate_green = False
            return GREEN_APPLE_REWARD
        elif self.board.ate_red:
            self.board.ate_red = False
            return RED_APPLE_REWARD
        elif self.state[self.last_move] == 3 and self.board.death is False:
            return GREEN_DIRECTION_REWARD
        elif self.state[self.last_move] != 3 and self.board.death is False:
            return EMPTY_MOVE_REWARD
        elif self.board.death:
            return DEATH_REWARD

    def display_gameplay(self, qtable_filename):
        """
            Charge un agent existant.
            Le fait jouer avec display.
        """
        self.grass_sprite = pygame.image.load("sprites/grass.png").convert_alpha()
        self.wall_sprite = pygame.image.load("sprites/wall.png").convert_alpha()
        self.snake_sprite = pygame.image.load("sprites/snake.png").convert_alpha()
        self.head_sprite = pygame.image.load("sprites/head.png").convert_alpha()
        self.red_sprite =  pygame.image.load("sprites/red.png").convert_alpha()
        self.green_sprite = pygame.image.load("sprites/green.png").convert_alpha()
        pygame.display.set_icon(self.head_sprite)
        
        self.t1.start()
        agent = Agent(exploration_rate=0)
        agent.load_q_table(qtable_filename)
        clock = pygame.time.Clock()
        max_len = 0
        duration = 0
        running = True
        while running is True:
            duration += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            state = agent.get_state()
            action = agent.chose_action(state)
            print(agent.get_agent_board().get_agent_vision())
            print(state)
            self.print_action(action)
            agent.perform_action(action)
            agent.get_agent_board().is_eating_apple()
            if agent.get_agent_board().death:
                print(f"Max length of snake: {max_len}, Duration: {duration}")
                self.death_screen()
            agent.get_agent_board().update_board()
            if self.is_ui_on:
                self.display_board(agent.get_agent_board())
            if len(agent.get_agent_board().snake_pos) > max_len:
                max_len = len(agent.get_agent_board().snake_pos)
            while self.rate == 0 and self.next_step is False:
                pass
            self.next_step = False
            if self.rate == 1:
                clock.tick(60)
        print(f"Max length of snake: {max_len}")
        self.t1.join()
    
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

    def print_action(self, action):
        value_list = ["west", "east", "north", "down"]
        print(value_list[action])

    def display_board(self, board= 0):
        if isinstance(board, int) is False:
            self.board = board #cette board est larray np et pas la classe
        self.screen.fill((0, 0, 0))
        for y in range(self.board.board.shape[0]):
            for x in range(self.board.board.shape[1]):
                value = self.board.board[y, x]
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

    def death_screen(self):
        self.screen.fill((0, 0, 0))
        deathscreen = pygame.image.load("sprites/deathscreen.png").convert()
        pygame.mixer.music.load('sprites/death_soundtrack.mp3')
        self.screen.blit(deathscreen, (0, 0))
        pygame.display.flip()
        while True:
            if pygame.mixer.music.get_busy() is False:
                pygame.mixer.music.play(-1, 0.0)
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit(0)
                elif event.key == pygame.K_RETURN:
                    self.board.resurrect()
                    self.game_loop()
            
    def setup_camera_background(self):
        self.camera = cv2.VideoCapture(0)
        if not self.camera.isOpened():
            print("Error: Could not open camera.")
            return False
        return True
    
    def update_camera_background(self):
        ret, frame = self.camera.read()
        if not ret:
            print("Error: Failed to capture image")
            return None
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE) 
        frame = cv2.resize(frame, (self.screen.get_width(), self.screen.get_height()))
        camera_surface = pygame.surfarray.make_surface(frame)
        return camera_surface


    
    
#g = Game()
#g.game_loop()