from collections import deque
import random
import copy
import threading
from observable import Observable


def tile_to_key(tile):
    return str(tile[0]) + " " + str(tile[1])


class SnakeModel:
    def __init__(self, grid_width, grid_height):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.grid_tiles = self.grid_width * self.grid_height
        self.game_tick_seconds = 0.15

        # The following are variables that are set and documented in the reset_game() method
        self.player_start = None
        self.player_body = None
        self.player_head = None
        self.fruit = None
        self.direction = None
        self.proposed_direction = None
        self.game_loop_itr = None
        self.snake_length = None
        self.game_status = None

        self.game_loop_observable = Observable()

    def reset(self):
        self.player_start = [0, 1]
        self.player_body = deque([[0, 0]])
        self.player_head = self.player_start

        # 0 = up, 1 = left, 2 = down, 3 = right
        self.direction = 0

        self.proposed_direction = 0
        self.game_loop_itr = 0
        self.snake_length = 1

        # -1 = player has died,   1 = player has won,   0 = non terminal state
        self.game_status = 0
        self.randomise_fruit()

        # This is here to notify listeners of the initial state of the board, such as the view so it can draw it
        self.game_loop_observable.notify()

    def move_player(self):
        old_player_head = copy.deepcopy(self.player_head)
        if self.direction == 0:
            self.player_head[1] += 1
        elif self.direction == 1:
            self.player_head[0] -= 1
        elif self.direction == 2:
            self.player_head[1] -= 1
        elif self.direction == 3:
            self.player_head[0] += 1

        if self.can_eat():
            self.player_body.appendleft(old_player_head)
            self.randomise_fruit()
            self.snake_length += 1
        else:
            self.player_body[-1] = old_player_head
            self.player_body.rotate(1)

    def change_direction(self, direction):
        self.proposed_direction = direction

    def lock_in_direction(self):
        if self.proposed_direction + self.direction == 4 or self.proposed_direction + self.direction == 2:
            return

        self.direction = self.proposed_direction

    # Checks whether the game has reached a terminal state, and what kind it is
    # -1 = player has died,   1 = player has won,   0 = non terminal state
    def termination_check(self):
        if self.player_head in self.player_body:
            return -1
        elif self.player_head[0] == -1 or self.player_head[1] == -1 or self.player_head[0] >= self.grid_width \
                or self.player_head[1] >= self.grid_height:
            return -1
        elif (len(self.player_body) + 1) == self.grid_tiles:
            return 1
        return 0

    def can_eat(self):
        return self.player_head == self.fruit

    def randomise_fruit(self):
        free_tiles = dict()

        for i in range(self.grid_width):
            for j in range(self.grid_height):
                free_tiles[tile_to_key([i, j])] = [i, j]

        del free_tiles[(tile_to_key(self.player_head))]

        for body_piece in self.player_body:
            del free_tiles[(tile_to_key(body_piece))]

        self.fruit = list(free_tiles.values())[random.randint(0, len(free_tiles) - 1)]

    def step(self):
        self.game_loop_itr += 1
        self.lock_in_direction()
        self.move_player()
        self.game_status = self.termination_check()
        # Used to keep restarting the game once the player dies
        # if self.game_status == -1:
        #    self.reset()
        self.game_loop_observable.notify()

    def game_loop(self):
        self.step()
        if self.game_status == 0:
            threading.Timer(self.game_tick_seconds, self.game_loop).start()

    def start_game(self):
        threading.Timer(self.game_tick_seconds, self.game_loop).start()
