import numpy as np


class Game:
    __slots__ = ("map", "_neighbors")

    def __init__(self, size: int = 100):
        self.map = np.zeros((size, size), dtype=np.int8)
        self._neighbors = np.zeros(self.map.shape, dtype=np.int8)

    def update(self):
        # Reset neighbors
        self._neighbors[:, :] = 0

        # Prepared slices
        same = slice(None)  # Whole axis
        head = slice(0, -1)  # Axis without last row
        tail = slice(1, None)  # Axis without first row
        first = slice(None, 1)  # First row
        last = slice(-1, None)  # Last row

        # Middle
        self._neighbors[same, head] += self.map[same, tail]  # West/East
        self._neighbors[same, tail] += self.map[same, head]  # East/West

        self._neighbors[tail, same] += self.map[head, same]  # South/North
        self._neighbors[head, same] += self.map[tail, same]  # North/South

        self._neighbors[tail, tail] += self.map[head, head]  # South-East/North-West
        self._neighbors[tail, head] += self.map[head, tail]  # South-West/North-East

        self._neighbors[head, tail] += self.map[tail, head]  # North-East/South-West
        self._neighbors[head, head] += self.map[tail, tail]  # North-West/South-East

        # Borders
        self._neighbors[same, first] += self.map[same, last]  # West/East
        self._neighbors[same, last] += self.map[same, first]  # East/West

        self._neighbors[first, same] += self.map[last, same]  # North/South
        self._neighbors[last, same] += self.map[first, same]  # South/North

        # Corners
        self._neighbors[first, first] += self.map[last, last]  # North-West/South-East
        self._neighbors[first, last] += self.map[last, first]  # North=East/South-West

        self._neighbors[last, last] += self.map[first, first]  # South-East/North-West
        self._neighbors[last, first] += self.map[first, last]  # South-West/North=East

        self.map &= self._neighbors == 2
        self.map |= self._neighbors == 3

    def randomize(self):
        self.map = np.random.randint(0, 2, size=self.map.shape, dtype=np.int8)


if __name__ == "__main__":
    import os
    import argparse

    import pygame

    os.environ["SDL_VIDEO_WINDOW_POS"] = "0,35"

    parser = argparse.ArgumentParser(
        description="Game of Life implementation with Numpy."
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
    screen_shape = (args.screen_size, args.screen_size)
    screen = pygame.display.set_mode(screen_shape)
    screen_buffer = np.zeros((tile_count, args.tile_size) * 2, dtype=np.int32)

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
                game.map[x][y] = 1 if game.map[x][y] == 0 else 0

        if running:
            game.update()
        
        screen_buffer[...] = game.map[:, None, :, None]
        screen_buffer[screen_buffer == 1] = 65380
        screen_buffer[screen_buffer == 0] = 11187310

        pygame.surfarray.blit_array(screen, screen_buffer.reshape(screen_shape))

        fps = str(round(clock.get_fps(), 5))
        fps_text = fps_font.render(fps, True, "black")
        screen.blit(fps_text, (10, 0))

        pygame.display.flip()
        clock.tick(args.fps_cap)

    pygame.quit()
