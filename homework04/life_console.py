import curses
from time import sleep

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        screen.border()

    def draw_grid(self, screen) -> None:
        for num, row in enumerate(self.life.curr_generation):
            arr=[]
            for i in row:
                if i:
                    arr.append("*")
                else:
                    arr.append(" ")
            s = "".join(arr)
            try:
                screen.addstr(num + 1, 1, s)
            except Exception:
                pass

    def run(self) -> None:
        screen = curses.initscr()
        while self.life.is_changing and not self.life.is_max_generations_exceeded:
            self.draw_borders(screen)
            self.draw_grid(screen)
            screen.refresh()
            self.life.step()
            sleep(2)
        curses.endwin()

if __name__ == "__main__":
    life = GameOfLife((24, 102), max_gen=10)
    game = Console(life)
    game.run()
