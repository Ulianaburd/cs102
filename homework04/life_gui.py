import pygame
from life import GameOfLife
from ui import UI


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        super().__init__(life)
        self.cell_size = cell_size
        self.speed = speed
        self.width = self.life.cols * self.cell_size
        self.height = self.life.rows * self.cell_size
        self.screen_size = self.width, self.height
        self.screen = pygame.display.set_mode(self.screen_size)
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

    def draw_lines(self) -> None:
        for x in range(0, self.screen_size[0], self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.screen_size[1]))
        for y in range(0, self.screen_size[1], self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.screen_size[0], y))

    def draw_grid(self) -> None:
        for y in range(0,self.life.rows):
            for x in range(0,self.life.cols):
                if self.life.curr_generation[y][x] == 1:
                    color = pygame.Color("green")
                else:
                    color = pygame.Color("white")
                height = length = self.cell_size
                xx = x * self.cell_size
                yy = y * self.cell_size
                rect = (xx, yy, height, length)
                pygame.draw.rect(self.screen, color, rect=rect)

    def run(self) -> None:
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))
        is_playing = True
        is_paused = False
        while self.life.is_changing and not self.life.is_max_generations_exceeded and is_playing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_playing = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    is_paused = not is_paused
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    xx, yy = pygame.mouse.get_pos()
                    xx = (xx // self.cell_size) % self.life.cols
                    yy = (yy // self.cell_size) % self.life.rows
                    if self.life.curr_generation[yy][xx] == 0:
                        self.life.curr_generation[yy][xx] = 1
                    else:
                        self.life.curr_generation[yy][xx] = 0
                    self.draw_grid()
                    self.draw_lines()
                    pygame.display.flip()
            if not is_paused:
                self.life.step()
                self.draw_grid()
                self.draw_lines()
                pygame.display.flip()
                clock.tick(self.speed)
        pygame.quit()


if __name__ == "__main__":
    life = GameOfLife((10, 10), max_gen=10)
    game = GUI(life, cell_size=40)
    game.run()
