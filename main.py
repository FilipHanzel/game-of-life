import pygame

from game import Game


def main():
    screen_size = 1200
    tile_size = 5
    tile_count = screen_size // tile_size

    pygame.init()
    screen = pygame.display.set_mode((screen_size, screen_size))
    pygame.display.set_caption("Game of Life")

    clock = pygame.time.Clock()

    game = Game(tile_count)
    game.randomize()

    running = False
    end = False
    while not end:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                end = True

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = not running

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                x //= tile_size
                y //= tile_size
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
                            col_idx * tile_size,
                            row_idx * tile_size,
                            tile_size,
                            tile_size,
                        ),
                    )

        pygame.display.flip()
        clock.tick(120)  # 120 fps cap

    pygame.quit()


if __name__ == "__main__":
    main()
