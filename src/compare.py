from game_numpy import Game as GameNp
from game_cupy import Game as GameCp
from game import Game as Game


import time


def measure(game_class, size: int, iterations: int) -> str:
    start = time.time()

    game = game_class(size)

    mid = time.time()

    for _ in range(iterations):
        game.update()

    stop = time.time()

    init = mid - start
    loop = stop - mid

    print(
        f"Init time: {round(init, 5):.5f}[s]",
        f"Total loop time: {round(loop, 5):.5f}[s], {iterations} iterations, "
        f"{round(loop / iterations, 5):.5f}[s] per iteration",
    )


if __name__ == "__main__":
    size = 5000

    print("Runnig vanilla python implementation...")
    measure(Game, size, 5)

    print("\nRunnig np python implementation...")
    measure(GameNp, size, 50)

    print("\nRunnig cp python implementation...")
    measure(GameCp, size, 50)
