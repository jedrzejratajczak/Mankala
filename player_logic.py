import math
from random import choice
from typing import Callable
from game_engine import Game


def __get_random_move(engine: Game):
    return choice(engine.houses[(engine.current_player - 1)])


def __get_possible_houses(engine: Game) -> list[str]:
    possible_houses = []
    for i in range(len(engine.houses[engine.current_player - 1])):
        if engine.houses[engine.current_player - 1][i] != 0:
            possible_houses.append(str(i + 1))
    return possible_houses


def player_movement(engine: Game) -> int:
    if engine.round_number == 0:
        house_number = __get_random_move(engine)
        print("Player " + str(engine.current_player))
        print("Moved house -> " + str(house_number))
    else:
        possible_houses = __get_possible_houses(engine)

        house_number = -1
        while house_number not in possible_houses:
            print("Player " + str(engine.current_player))
            house_number = input("Type house number [" + ', '.join(possible_houses) + "]: ")

    return int(house_number)


def subtracting_stores_heuristics(engine: Game, player: int) -> int:
    my_store = engine.stores[player - 1]
    opponent_store = engine.stores[engine.get_next_player_number(player) - 1]
    return my_store - opponent_store


def knock_first_then_substracting_stores_heuristics(engine: Game, player: int) -> int:
    return subtracting_stores_heuristics(engine, player) + 5 if engine.knocked else 0


def __minimax(engine: Game, depth: int, is_maximizing: bool, static_eval_fun: Callable, player: int = None) -> (int, int):
    if player is None:
        player = engine.current_player
    if depth == 0 or engine.check_game_end():
        return static_eval_fun(engine, player), 0

    if is_maximizing:
        max_eval = -math.inf
        movement = 0
        for possible_house in __get_possible_houses(engine):
            next_move_engine = engine.copy_engine()
            next_move_engine.execute_move(int(possible_house))
            (evaluated_value, _) = __minimax(
                next_move_engine,
                depth - 1,
                True if engine.current_player == next_move_engine.current_player else False,
                static_eval_fun,
                player
            )
            if max_eval < evaluated_value:
                max_eval = evaluated_value
                movement = possible_house
        return max_eval, movement
    else:
        min_eval = math.inf
        movement = 0
        for possible_house in __get_possible_houses(engine):
            next_move_engine = engine.copy_engine()
            next_move_engine.execute_move(int(possible_house))
            (evaluated_value, _) = __minimax(
                next_move_engine,
                depth - 1,
                False if engine.current_player == next_move_engine.current_player else True,
                static_eval_fun,
                player
            )
            if min_eval > evaluated_value:
                min_eval = evaluated_value
                movement = possible_house
        return min_eval, movement


def __minimax_alfa_beta(engine: Game, depth: int, is_maximizing: bool, static_eval_fun: Callable, alpha: float, beta: float, player: int = None) -> (int, int):
    if player is None:
        player = engine.current_player
    if depth == 0 or engine.check_game_end():
        return static_eval_fun(engine, player), 0

    if is_maximizing:
        max_eval = -math.inf
        movement = 0
        for possible_house in __get_possible_houses(engine):
            next_move_engine = engine.copy_engine()
            next_move_engine.execute_move(int(possible_house))
            (evaluated_value, _) = __minimax_alfa_beta(
                next_move_engine,
                depth - 1,
                True if engine.current_player == next_move_engine.current_player else False,
                static_eval_fun,
                alpha,
                beta,
                player
            )
            if max_eval < evaluated_value:
                max_eval = evaluated_value
                movement = possible_house
            alpha = max(alpha, evaluated_value)
            if beta <= alpha:
                break
        return max_eval, movement
    else:
        min_eval = math.inf
        movement = 0
        for possible_house in __get_possible_houses(engine):
            next_move_engine = engine.copy_engine()
            next_move_engine.execute_move(int(possible_house))
            (evaluated_value, _) = __minimax_alfa_beta(
                next_move_engine,
                depth - 1,
                False if engine.current_player == next_move_engine.current_player else True,
                static_eval_fun,
                alpha,
                beta,
                player
            )
            if min_eval > evaluated_value:
                min_eval = evaluated_value
                movement = possible_house
            beta = min(beta, evaluated_value)
            if beta <= alpha:
                break
        return min_eval, movement


def minimax_wrapper(engine: Game, depth: int, static_eval_fun: Callable) -> int:
    if engine.round_number == 0:
        move = __get_random_move(engine)
    else:
        move = int(__minimax(engine, depth, True, static_eval_fun)[1])
    print("Player " + str(engine.current_player))
    print("Moved house -> " + str(move))
    return move


def minimax_alfa_beta_wrapper(engine: Game, depth: int, static_eval_fun: Callable) -> int:
    if engine.round_number == 0:
        move = __get_random_move(engine)
    else:
        move = int(__minimax_alfa_beta(engine, depth, True, static_eval_fun, -math.inf, math.inf)[1])
    print("Player " + str(engine.current_player))
    print("Moved house -> " + str(move))
    return move
