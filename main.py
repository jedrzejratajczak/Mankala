from typing import Callable
from game_engine import Game
from player_logic import player_movement, minimax_wrapper, subtracting_stores_heuristics, minimax_alfa_beta_wrapper, knock_first_then_substracting_stores_heuristics
from config import DEPTH_1, DEPTH_2


def choose_heuristics(engine: Game, depth: int, player_number: int) -> Callable:
    print("Available heuristics:")
    print("1 - Play by yourself")
    print("2 - Minimax with substracting stores")
    print("3 - Minimax with knock first then substracting stores")
    print("4 - Minimax alfa beta with substracting stores")
    print("5 - Minimax alfa beta with knock first then substracting stores")
    print("Choose heuristics for player " + str(player_number) + ":")
    chosen_heuristic = int(input())
    if chosen_heuristic == 1:
        return lambda: player_movement(engine)
    elif chosen_heuristic == 2:
        return lambda: minimax_wrapper(engine, depth, subtracting_stores_heuristics)
    elif chosen_heuristic == 3:
        return lambda: minimax_wrapper(engine, depth, knock_first_then_substracting_stores_heuristics)
    elif chosen_heuristic == 4:
        return lambda: minimax_alfa_beta_wrapper(engine, depth, subtracting_stores_heuristics)
    elif chosen_heuristic == 5:
        return lambda: minimax_alfa_beta_wrapper(engine, depth, knock_first_then_substracting_stores_heuristics)


if __name__ == '__main__':
    engine = Game()
    engine.game_loop(choose_heuristics(engine, DEPTH_1, 1), choose_heuristics(engine, DEPTH_2, 2))
