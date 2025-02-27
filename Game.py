from Board import Board
import pygame

TILE_SIZE = 50

class Game:
    def __init__(self):
        self.board = Board()
        pygame.init()
        self.grass_sprite = 0
        self.wall_sprite = 0
        self.snake_sprite = 0
        self.red_sprite =  0
        self.green_sprite = 0
        self.screen = pygame.display.set_mode((TILE_SIZE * 12, TILE_SIZE * 12))
    
    def game_loop(self):
        self.grass_sprite = pygame.image.load("sprites/grass.png").convert()
        self.wall_sprite = pygame.image.load("sprites/wall.png").convert()
        self.snake_sprite = pygame.image.load("sprites/snake.png").convert()
        self.head_sprite = pygame.image.load("sprites/head.png").convert()
        self.red_sprite =  pygame.image.load("sprites/red.png").convert()
        self.green_sprite = pygame.image.load("sprites/green.png").convert()
        running = True
        while running:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.board.snake_move_north()
                elif event.key == pygame.K_DOWN:
                    self.board.snake_move_south()
                elif event.key == pygame.K_LEFT:
                    self.board.snake_move_west()
                elif event.key == pygame.K_RIGHT:
                    self.board.snake_move_east()
            self.board.is_eating_apple()
            self.board.update_board()
            self.display_board()

        pygame.quit()

    def display_board(self):
        self.screen.fill((0, 0, 0))
        for y in range(self.board.board.shape[0]):
            for x in range(self.board.board.shape[1]):
                value = self.board.board[y, x]
                if (value == 0):
                    sprite = self.grass_sprite
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


    
g = Game()
g.game_loop()