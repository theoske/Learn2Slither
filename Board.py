import numpy as np
from random import randint


class Board:
    board = np.zeros((10, 10), dtype=int)
    snake_pos = [0, 0]
    red_pos = [0, 0]
    green1_pos = [0, 0]
    green2_pos = [0, 0]

    def gen_board(self):
        self.snake_pos = self.random_snake_pos()
        self.red_pos = self.random_apple_pos()
        self.green1_pos = self.random_apple_pos()
        self.green2_pos = self.random_apple_pos()

        snake_entire_body_pos = [[self.snake_pos[0], self.snake_pos[1] - 2], [self.snake_pos[0], self.snake_pos[1] - 1], [self.snake_pos[0], self.snake_pos[1]]]
        while (self.red_pos in snake_entire_body_pos):
            self.red_pos = self.random_apple_pos()
        while (self.green1_pos in snake_entire_body_pos or self.red_pos is self.green1_pos):
            self.green1_pos = self.random_apple_pos()
        while (self.green2_pos in snake_entire_body_pos or self.green2_pos is self.green1_pos or self.red_pos is self.green2_pos):
            self.green2_pos = self.random_apple_pos()
        
        self.board[self.snake_pos[0], self.snake_pos[1]] = 1
        self.board[self.snake_pos[0], self.snake_pos[1] - 1] = 1
        self.board[self.snake_pos[0], self.snake_pos[1] - 2] = 1
        self.board[self.red_pos[0], self.red_pos[1]] = 2
        self.board[self.green1_pos[0], self.green1_pos[1]] = 3
        self.board[self.green2_pos[0], self.green2_pos[1]] = 3

        return self.board

    def random_snake_pos(self):
        x = randint(2, 8)
        y = randint(0, 9)
        return [y, x]

    def random_apple_pos(self):
        x = randint(0, 9)
        y = randint(0, 9)
        return [y, x]

    

b = Board()
print(b.gen_board())