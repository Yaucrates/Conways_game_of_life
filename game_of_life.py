import pygame
import numpy as np

# Define some constants
CELL_SIZE = 10
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class GameOfLife:
    def __init__(self, width=800, height=600):
        pygame.init()
        self.screen_size = (width, height)
        self.screen = pygame.display.set_mode(self.screen_size, pygame.RESIZABLE)
        self.clock = pygame.time.Clock()

        self.cell_width = width // CELL_SIZE
        self.cell_height = height // CELL_SIZE

        self.grid = np.zeros((self.cell_height, self.cell_width))
        self.paused = True

    def draw_grid(self):
        for x in range(0, self.cell_width):
            for y in range(0, self.cell_height):
                if self.grid[y][x]:
                    pygame.draw.rect(self.screen, WHITE, (x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE))

    def update(self):
        new_grid = self.grid.copy()
        for y in range(self.cell_height):
            for x in range(self.cell_width):
                state = self.grid[y][x]
                neighbours = self.get_neighbours(x, y)
                if state and not (2 <= neighbours <= 3):
                    new_grid[y][x] = 0
                elif not state and neighbours == 3:
                    new_grid[y][x] = 1
        self.grid = new_grid

    def get_neighbours(self, x, y):
        total = 0
        for i in range(max(0, y - 1), min(self.cell_height, y + 2)):
            for j in range(max(0, x - 1), min(self.cell_width, x + 2)):
                total += self.grid[i][j]
        total -= self.grid[y][x]
        return total

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.paused = not self.paused
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.paused:
                    x, y = pygame.mouse.get_pos()
                    x //= CELL_SIZE
                    y //= CELL_SIZE
                    self.grid[y][x] = not self.grid[y][x]
            if event.type == pygame.VIDEORESIZE:
                self.screen = pygame.display.set_mode(event.dict['size'], pygame.RESIZABLE)
                self.screen_size = event.dict['size']
                self.cell_width = self.screen_size[0] // CELL_SIZE
                self.cell_height = self.screen_size[1] // CELL_SIZE
                new_grid = np.zeros((self.cell_height, self.cell_width))
                new_grid[:self.grid.shape[0], :self.grid.shape[1]] = self.grid
                self.grid = new_grid
        return True

    def run(self):
        while True:
            self.screen.fill(BLACK)
            self.draw_grid()
            if not self.paused:
                self.update()
            else:
                font = pygame.font.Font(None, 24)
                text = font.render("Paused", 1, WHITE)
                text_pos = text.get_rect(centerx=self.screen_size[0] - 50, centery=self.screen_size[1] - 20)
                self.screen.blit(text, text_pos)

            pygame.display.flip()
            self.clock.tick(10)

            if not self.handle_events():
                pygame.quit()
                break


if __name__ == '__main__':
    game = GameOfLife()
    game.run()

