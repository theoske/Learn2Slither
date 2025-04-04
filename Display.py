import pygame
import numpy as np
from Board import Board
import threading
from time import sleep

TILE_SIZE = 50

class Display:
    """
        display_board runs in another thread and display the self.board constantly.
        When set_board is called the board is updated.
    """
    def __init__(self, board= 0):
        pygame.init()
        self.screen = pygame.display.set_mode((TILE_SIZE * 12, TILE_SIZE * 12))
        pygame.display.set_caption("Learn2Slither")
        self.wall_sprite = pygame.image.load("sprites/wall.png").convert_alpha()
        self.snake_sprite = pygame.image.load("sprites/snake.png").convert_alpha()
        self.head_sprite = pygame.image.load("sprites/head.png").convert_alpha()
        self.red_sprite =  pygame.image.load("sprites/red.png").convert_alpha()
        self.green_sprite = pygame.image.load("sprites/green.png").convert_alpha()
        pygame.display.set_icon(self.head_sprite)
        self.t1 = threading.Thread(target= self.display_main, daemon= True)
        self.board = board
    
    def set_board(self, new_board):
        self.board = new_board
    
    def display_main(self):
        running = True
        while running:
            if self.board != 0:
                self.display_board(self.board)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            sleep(0.01)
        if running is False:
            pygame.quit()
    
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
"""
b = Board()
disp = Display()
disp.display_board(b.board)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
"""