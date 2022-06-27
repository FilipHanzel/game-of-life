import random


class Game:
    __slots__ = ("map", "size")

    def __init__(self, size: int = 100):
        self.map = [[0] * size for _ in range(size)]
        self.size = size

    def _count_living_neighbors(self, row_idx: int, col_idx: int) -> int:
        count = 0

        row_prev = row_idx - 1
        col_prev = col_idx - 1
        row_next = (row_idx + 1) % self.size
        col_next = (col_idx + 1) % self.size

        count += self.map[row_prev][col_prev]
        count += self.map[row_prev][col_idx]
        count += self.map[row_prev][col_next]
        count += self.map[row_idx][col_prev]
        count += self.map[row_idx][col_next]
        count += self.map[row_next][col_prev]
        count += self.map[row_next][col_idx]
        count += self.map[row_next][col_next]

        return count

    def _get_new_cell_state(self, row_idx: int, col_idx: int) -> int:
        neighbors = self._count_living_neighbors(row_idx, col_idx)
        current_state = self.map[row_idx][col_idx]

        if current_state == 0 and neighbors == 3:
            return 1
        if current_state == 1 and neighbors not in (2, 3):
            return 0
        return current_state

    def update(self):
        self.map = [
            [self._get_new_cell_state(row_idx, col_idx) for col_idx in range(self.size)]
            for row_idx in range(self.size)
        ]

    def randomize(self):
        self.map = [
            [random.randint(0, 1) for _ in range(self.size)] for _ in range(self.size)
        ]


if __name__ == "__main__":
    import os
    import argparse

    import pygame

    os.environ["SDL_VIDEO_WINDOW_POS"] = "0,35"

    parser = argparse.ArgumentParser(
        description="Pure python Game of Life implementation."
    )
    parser.add_argument("--screen-size", "-s", action="store", type=int, default=800)
    parser.add_argument("--tile-size", "-t", action="store", type=int, default=10)
    parser.add_argument("--fps-cap", "-f", action="store", type=int, default=120)
    parser.add_argument("--empty", "-e", action="store_true", default=False)
    args = parser.parse_args()

    if args.screen_size % args.tile_size != 0:
        raise ValueError("screen size must be divisible by tile size")

    tile_count = args.screen_size // args.tile_size
    print(f"Running the game with {tile_count ** 2} tiles...")

    pygame.init()
    screen = pygame.display.set_mode((args.screen_size, args.screen_size))
    pygame.display.set_caption("Game of Life - paused")

    fps_font = pygame.font.SysFont("Arial", 18)

    game = Game(tile_count)

    if not args.empty:
        game.randomize()

    clock = pygame.time.Clock()

    running = False
    end = False
    while not end:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                end = True

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = not running
                    pygame.display.set_caption(
                        f"Game of Life - {'running' if running else 'paused'}"
                    )

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                x //= args.tile_size
                y //= args.tile_size
                game.map[y][x] = 1 if game.map[y][x] == 0 else 0

        if running:
            game.update()

        screen.fill((170, 180, 110))

        for col_idx in range(game.size):
            for row_idx in range(game.size):
                state = game.map[row_idx][col_idx]
                if state == 1:
                    pygame.draw.rect(
                        surface=screen,
                        color=(0, 255, 100),
                        rect=(
                            col_idx * args.tile_size,
                            row_idx * args.tile_size,
                            args.tile_size,
                            args.tile_size,
                        ),
                    )

        fps = str(round(clock.get_fps(), 5))
        fps_text = fps_font.render(fps, True, "black")
        screen.blit(fps_text, (10, 0))

        pygame.display.flip()
        clock.tick(args.fps_cap)

    pygame.quit()
