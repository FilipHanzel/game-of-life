import argparse

import pygame

from game import Game


def main():
    parser = argparse.ArgumentParser(
        description="Pure python Game of Life implementation."
    )
    parser.add_argument(
        "--screen-size", "-s", action="store", type=int, default=800, dest="screen_size"
    )
    parser.add_argument(
        "--tile-size", "-t", action="store", type=int, default=10, dest="tile_size"
    )
    parser.add_argument(
        "--fps-cap", "-f", action="store", type=int, default=120, dest="fps_cap"
    )
    parser.add_argument(
        "--empty", "-e", action="store_true", default=False, dest="empty"
    )
    args = parser.parse_args()

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


if __name__ == "__main__":
    main()
