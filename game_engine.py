import time
from copy import deepcopy
from math import floor
from random import random
from typing import List, Callable


class Game:
    houses: [List[int], List[int]]
    stores: [int, int]
    round_number: int
    current_player: int
    knocked: bool

    def __init__(self, houses=None, stores=None, round_number=None, current_player=None, knocked=None):
        if [houses, stores, round_number, current_player, knocked] != [None, None, None, None, None]:
            self.houses = deepcopy(houses)
            self.stores = deepcopy(stores)
            self.round_number = round_number
            self.current_player = current_player
            self.knocked = knocked
        else:
            self.houses = [[4 for _ in range(6)], [4 for _ in range(6)]]
            self.stores = [0, 0]
            self.round_number = 0
            self.current_player = floor(random() * 2) + 1
            self.knocked = False

    def copy_engine(self):
        return Game(self.houses, self.stores, self.round_number, self.current_player, self.knocked)

    def game_loop(self, first_player_choose_func: Callable, second_player_choose_func: Callable) -> None:
        while not all(house == 0 for house in self.houses[0]) and not all(house == 0 for house in self.houses[1]):
            self.draw_board()

            start_time = time.time()
            chosen_house_number = first_player_choose_func() if self.current_player == 1 else second_player_choose_func()

            if not type(chosen_house_number) == int or not 7 > chosen_house_number > 0 or self.houses[self.current_player - 1][chosen_house_number - 1] == 0:
                raise Exception("Invalid choosing function. House number has to be int between 1 and 6. Cannot choose empty house.")

            self.execute_move(chosen_house_number)

        self.draw_board()
        winner_number = 1 if self.stores[0] > self.stores[1] else 2
        if self.stores[0] == self.stores[1]:
            print("It's a tie")
        else:
            print("Congratulations Player " + str(winner_number))
        print("Player 1 - " + str(self.stores[0]))
        print("Player 2 - " + str(self.stores[1]))

    def draw_board(self) -> None:
        x = [str(house) for house in self.houses[0]]
        x.append(str(self.stores[0]))
        y = [str(house) for house in self.houses[1]]
        y.append(str(self.stores[1]))
        for i in range(len(x)):
            if len(x[i]) == 1:
                x[i] = " " + x[i]
        for i in range(len(y)):
            if len(y[i]) == 1:
                y[i] = " " + y[i]
        print("\n")
        print("┌────┬────┬────┬────┬────┬────┬────┬────┐")
        print("│    │ " + y[5] + " │ " + y[4] + " │ " + y[3] + " │ " + y[2] + " │ " + y[1] + " │ " + y[0] + " │    │")
        print("│ " + y[6] + " ├────┼────┼────┼────┼────┼────┤ " + x[6] + " │")
        print("│    │ " + x[0] + " │ " + x[1] + " │ " + x[2] + " │ " + x[3] + " │ " + x[4] + " │ " + x[5] + " │    │")
        print("└────┴────┴────┴────┴────┴────┴────┴────┘")

    def execute_move(self, house_number: int) -> None:
        self.knocked = False
        beans = self.__get_chosen_house_beans(house_number)
        self.__clear_chosen_house_beans(house_number)
        current_player = self.current_player
        current_house_number = house_number

        additional_move_flag = False
        while beans != 0:
            current_house_number += 1

            if current_house_number == 7:
                beans = self.__add_bean_to_store(current_player, beans)
                current_player = self.get_next_player_number(current_player)
                current_house_number = 0
                if beans == 0:
                    additional_move_flag = True
            else:
                self.__add_bean_to_house(current_house_number, current_player)
                beans -= 1
                if beans == 0 and self.current_player == current_player and self.houses[current_player - 1][current_house_number - 1] == 1:
                    self.knocked = True
                    self.stores[self.current_player - 1] += 1 + self.houses[self.get_next_player_number(current_player) - 1][6 - current_house_number]
                    self.houses[current_player - 1][current_house_number - 1] = 0
                    self.houses[self.get_next_player_number(current_player) - 1][6 - current_house_number] = 0

        if self.check_game_end():
            self.__set_game_end_points()
        self.__set_next_round(additional_move_flag)

    def __get_chosen_house_beans(self, house_number: int) -> int:
        return self.houses[self.current_player - 1][house_number - 1]

    def __clear_chosen_house_beans(self, house_number: int) -> None:
        self.houses[self.current_player - 1][house_number - 1] = 0

    def __add_bean_to_store(self, current_player: int, beans: int) -> int:
        if current_player != self.current_player:
            return beans

        self.stores[self.current_player - 1] += 1
        return beans - 1

    @staticmethod
    def get_next_player_number(current_player_number: int) -> int:
        return current_player_number % 2 + 1

    def __add_bean_to_house(self, house_number: int, current_player: int) -> None:
        self.houses[current_player - 1][house_number - 1] += 1

    def check_game_end(self) -> bool:
        if all(house == 0 for house in self.houses[0]) or all(house == 0 for house in self.houses[1]):
            return True
        return False

    def __set_game_end_points(self) -> None:
        for i in range(len(self.houses)):
            if not all(house == 0 for house in self.houses[i]):
                self.stores[i] += sum(self.houses[self.get_next_player_number(i) - 1])
                for ii in range(len(self.houses[self.get_next_player_number(i) - 1])):
                    self.houses[self.get_next_player_number(i) - 1][ii] = 0

    def __set_next_round(self, additional_move_flag: bool) -> None:
        self.round_number += 1
        if not additional_move_flag:
            self.current_player = self.get_next_player_number(self.current_player)
