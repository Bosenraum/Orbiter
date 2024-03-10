import pygame
import numpy as np

# Constants
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 5
ROWS, COLS = HEIGHT // CELL_SIZE, WIDTH // CELL_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SAND_COLOR = (194, 178, 128)  # Sand color

# Create grid
grid = np.zeros((ROWS, COLS))

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

def update_grid():
    global grid
    new_grid = np.zeros_like(grid)
    for y in range(1, ROWS):
        for x in range(COLS):
            if grid[y][x] == 1 and grid[y-1][x] == 0:  # If sand particle is falling
                new_grid[y][x] = 1
            elif grid[y][x] == 0 and grid[y-1][x] == 1:  # If space is empty below, sand falls
                new_grid[y][x] = 1
    grid = new_grid

def draw_grid():
    screen.fill(WHITE)
    for y in range(ROWS):
        for x in range(COLS):
            if grid[y][x] == 1:
                pygame.draw.rect(screen, SAND_COLOR, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

def main():
    global grid
    while True:
        handle_events()
        update_grid()
        draw_grid()
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
