import numpy as np
from random import randint


class Board:
    """
        This class is the backend of the snake game.
    """
    def __init__(self):
        self.death = False
        self.board = np.zeros((12, 12), dtype=int)
        self.snake_pos = self.random_snake_pos()
        self.red_pos = self.random_apple_pos()
        self.green1_pos = self.random_apple_pos()
        self.green2_pos = self.random_apple_pos()
        self.gen_board()

    def resurrect(self):
        self.death = False
        self.board = np.zeros((12, 12), dtype=int)
        self.snake_pos = self.random_snake_pos()
        self.red_pos = self.random_apple_pos()
        self.green1_pos = self.random_apple_pos()
        self.green2_pos = self.random_apple_pos()
        self.gen_board()

    def gen_board(self):
        while (self.red_pos in self.snake_pos):
            self.red_pos = self.random_apple_pos()
        while (self.green1_pos in self.snake_pos or
               self.red_pos == self.green1_pos):
            self.green1_pos = self.random_apple_pos()
        while (self.green2_pos in self.snake_pos or
               self.green2_pos == self.green1_pos or
               self.red_pos == self.green2_pos):
            self.green2_pos = self.random_apple_pos()

        self.board[self.snake_pos[0]] = 5
        self.board[self.snake_pos[1]] = 1
        self.board[self.snake_pos[2]] = 1
        self.board[self.red_pos] = 2
        self.board[self.green1_pos] = 3
        self.board[self.green2_pos] = 3

        self.put_wall()

    def random_snake_pos(self):
        x = randint(3, 9)
        y = randint(1, 10)
        return [(y, x), (y, x-1), (y, x-2)]

    def random_apple_pos(self):
        x = randint(1, 10)
        y = randint(1, 10)
        return (y, x)

    def put_wall(self):
        self.board[0, :] = 4
        self.board[11, :] = 4
        self.board[:, 0] = 4
        self.board[:, 11] = 4

    def snake_move_east(self):
        if self.is_move_legal("east") is False:
            self.death = True
            return
        for i in range(len(self.snake_pos) - 1, -1, -1):
            if i != 0:
                self.snake_pos[i] = self.snake_pos[i-1]
            else:
                self.snake_pos[0] = (self.snake_pos[0][0],
                                     self.snake_pos[0][1] + 1)

    def snake_move_west(self):
        if self.is_move_legal("west") is False:
            self.death = True
            return
        for i in range(len(self.snake_pos) - 1, -1, -1):
            if i != 0:
                self.snake_pos[i] = self.snake_pos[i-1]
            else:
                self.snake_pos[0] = (self.snake_pos[0][0],
                                     self.snake_pos[0][1] - 1)

    def snake_move_north(self):
        if self.is_move_legal("north") is False:
            self.death = True
            return
        for i in range(len(self.snake_pos) - 1, -1, -1):
            if i != 0:
                self.snake_pos[i] = self.snake_pos[i-1]
            else:
                self.snake_pos[0] = (self.snake_pos[0][0] - 1,
                                     self.snake_pos[0][1])

    def snake_move_south(self):
        if self.is_move_legal("south") is False:
            self.death = True
            return
        for i in range(len(self.snake_pos) - 1, -1, -1):
            if i != 0:
                self.snake_pos[i] = self.snake_pos[i-1]
            else:
                self.snake_pos[0] = (self.snake_pos[0][0] + 1,
                                     self.snake_pos[0][1])

    def is_move_legal(self, move_name):
        head = self.snake_pos[0]
        if move_name == "east":
            future_pos = (head[0], head[1] + 1)
        elif move_name == "west":
            future_pos = (head[0], head[1] - 1)
        elif move_name == "north":
            future_pos = (head[0] - 1, head[1])
        elif move_name == "south":
            future_pos = (head[0] + 1, head[1])
        else:
            print("Error in is_move_legal: else condition called")
            exit(0)
        forbiden_collision_list = [1, 4]
        if self.board[future_pos] in forbiden_collision_list:
            return False
        return True

    def update_board(self):
        self.board[1:11, 1:11] = 0
        for i in range(len(self.snake_pos)):
            self.board[self.snake_pos[i]] = 1
        self.board[self.snake_pos[0]] = 5
        self.board[self.red_pos] = 2
        self.board[self.green1_pos] = 3
        self.board[self.green2_pos] = 3

    def get_board(self):
        return self.board

    def is_eating_apple(self):
        """
        checks if snake head is on apple
        update snake size
        """
        snake_head = self.snake_pos[0]
        if snake_head == self.green1_pos:
            self.augment_snake()
            self.respawn_green1()
        elif snake_head == self.green2_pos:
            self.augment_snake()
            self.respawn_green2()
        elif snake_head == self.red_pos:
            self.reduce_snake()
            self.respawn_red()

    def respawn_green1(self):
        while (self.green1_pos in self.snake_pos or
               self.green1_pos == self.green2_pos or
               self.green1_pos == self.red_pos):
            self.green1_pos = self.random_apple_pos()

    def respawn_green2(self):
        while (self.green2_pos in self.snake_pos or
               self.green2_pos == self.green1_pos or
               self.red_pos == self.green2_pos):
            self.green2_pos = self.random_apple_pos()

    def respawn_red(self):
        while (self.red_pos in self.snake_pos or
               self.red_pos == self.green1_pos or
               self.red_pos == self.green2_pos):
            self.red_pos = self.random_apple_pos()

    def reduce_snake(self):
        self.snake_pos.pop()
        if len(self.snake_pos) == 0:
            self.death = True
            return

    def augment_snake(self):
        tail = self.snake_pos[-1]
        self.snake_pos.append(tail)

    def get_agent_vision(self):
        """
            The agent only sees the column and the row of the snakes head.
            Tiles not visible to the snake set as -1.
            return (row, column)
        """
        head_pos = self.snake_pos[0]
        return (self.board[head_pos[0], :], self.board[:, head_pos[1]])
