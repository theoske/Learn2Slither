from Board import Board
import pygame
import cv2

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
            #print(self.board.board)
            self.vision_to_state(self.board.get_agent_vision())

    def display_board(self):
        self.screen.fill((0, 0, 0))
        camera_surface = self.update_camera_background()
        if camera_surface is not None:
            self.screen.blit(camera_surface, (0, 0))
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


    def vision_to_state(self, v):
            """
                Takes the visible board and returns the closest tile or the closest green apple
                if there is no obstacle between the snake's head and the apple.
            """
            visible_row, visible_column = v
            has_reached_snake = False
            first_object_west = 0
            first_object_east = 0

            head_x = 0
            head_y = 0

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
            if self.board.green2_pos[0] == self.board.snake_pos[0][0] and (self.board.green1_pos[0] != self.board.snake_pos[0][0] or (self.board.green2_pos[1] > self.board.green1_pos[1] and self.board.green2_pos[1] < self.board.snake_pos[0][1])):
                first_object_west = self.green2_west()
            elif self.board.green2_pos[0] == self.board.snake_pos[0][0] and (self.board.green1_pos[0] != self.board.snake_pos[0][0] or (self.board.green2_pos[1] < self.board.green1_pos[1] and self.board.green2_pos[1] > self.board.snake_pos[0][1])):
                first_object_east = self.green2_east()
            """
                faire pareil pour green2
                voir si green2 sur entre tete et green1
                si oui, reva dans algo pour green2
                continuer pour chaque direction
            """            
            print (first_object_west, first_object_east, first_object_north, first_object_south)

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
                return self.board.board[self.board.snake_pos[0][0], self.board.snake_pos[0][1] - 1]
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
                return self.board.board[self.board.snake_pos[0][0], self.board.snake_pos[0][1] - 1]
            else:
                return self.board.board[self.board.green2_pos]
        return 0
    
g = Game()
g.game_loop()