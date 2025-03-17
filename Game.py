from Board import Board
import pygame
import cv2
from Agent import Agent

TILE_SIZE = 50

class Game:
    """
        This class is used to play the snake game.
    """
    def __init__(self):
        self.board = Board()
        pygame.init()
        self.grass_sprite = 0
        self.wall_sprite = 0
        self.snake_sprite = 0
        self.red_sprite =  0
        self.green_sprite = 0
        self.screen = pygame.display.set_mode((TILE_SIZE * 12, TILE_SIZE * 12))
        pygame.display.set_caption('SkibidiSlither')

    
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
                elif event.key == pygame.K_DOWN:
                    self.board.snake_move_south()
                elif event.key == pygame.K_LEFT:
                    self.board.snake_move_west()
                elif event.key == pygame.K_RIGHT:
                    self.board.snake_move_east()
                elif event.key == pygame.K_ESCAPE:
                    exit(0)
            self.board.is_eating_apple()
            if self.board.death:
                self.death_screen()
            self.board.update_board()
            self.display_board()
    
    def display_gameplay(self, qtable_filename):
        self.grass_sprite = pygame.image.load("sprites/grass.png").convert_alpha()
        self.wall_sprite = pygame.image.load("sprites/wall.png").convert_alpha()
        self.snake_sprite = pygame.image.load("sprites/snake.png").convert_alpha()
        self.head_sprite = pygame.image.load("sprites/head.png").convert_alpha()
        self.red_sprite =  pygame.image.load("sprites/red.png").convert_alpha()
        self.green_sprite = pygame.image.load("sprites/green.png").convert_alpha()
        pygame.display.set_icon(self.head_sprite)
        
        agent = Agent()
        agent.load_q_table(qtable_filename)
        print("starttt")
        clock = pygame.time.Clock()
        running = True
        while running is True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            state = agent.get_state()
            action = agent.choose_action(state)
            print(action)
            agent.perform_action(action)
            agent.get_agent_board().is_eating_apple()
            if agent.get_agent_board().death:
                self.death_screen()
            agent.get_agent_board().update_board()
            self.display_board(agent.get_agent_board())
            clock.tick(1)
            

    def display_board(self, board= 0):
        if board != 0:
            self.board = board
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
                    self.board = Board()
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