import pygame
import random


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]

        self.left = 10
        self.top = 10
        self.cell_size = 30
        self.colors = [[0 for j in range(height)] for i in range(width)]
        self.flag = True
        self.ribbons = {}  # здесь будут хранится соединения
        self.ribbon_color = (random.choice(range(1, 256)), random.choice(range(1, 256)), random.choice(range(1, 256)))

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        colors = [pygame.Color('black'), pygame.Color('grey')]
        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(screen, colors[self.board[y][x]], (x * self.cell_size + self.left,
                                                                    y * self.cell_size + self.top,
                                                                    self.cell_size, self.cell_size))
                pygame.draw.rect(screen, pygame.Color('white'), (x * self.cell_size + self.left,
                                                                 y * self.cell_size + self.top,
                                                                 self.cell_size,
                                                                 self.cell_size), 1)
                if (x, y) in self.ribbons.keys():  # прорисовка ленточек
                    if self.ribbons[(x, y)] == "left":
                        pygame.draw.rect(screen, self.ribbon_color, ((x - 1) * self.cell_size + self.left + 7,
                                                                     y * self.cell_size + self.top + 5,
                                                                     2 * self.cell_size - 14,
                                                                     self.cell_size - 10))
                    if self.ribbons[(x, y)] == "up":
                        pygame.draw.rect(screen, self.ribbon_color, (x * self.cell_size + self.left + 5,
                                                                     (y - 1) * self.cell_size + self.top + 7,
                                                                     self.cell_size - 10,
                                                                     2 * self.cell_size - 14))

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell:  # проверка, нажали ли на клетку или на пустое пространство
            if self.board[cell[1]][cell[0]] == 1:
                pass
            elif self.flag:
                self.on_click(cell)
                self.first_cell = cell
                self.flag = not self.flag
            else:
                if (abs(self.first_cell[0] - cell[0]) == 1 and self.first_cell[1] == cell[1]) \
                        or (abs(self.first_cell[1] - cell[1]) == 1 and self.first_cell[0] == cell[0]):
                    self.on_click(cell)
                    if self.first_cell[0] - cell[0] == 1:  # проверяем как находятся относительно друг друга клетки
                        self.ribbons[self.first_cell] = "left"
                        self.ribbons[cell] = "right"
                    elif self.first_cell[0] - cell[0] == -1:
                        self.ribbons[self.first_cell] = "right"
                        self.ribbons[cell] = "left"
                    elif self.first_cell[1] - cell[1] == 1:
                        self.ribbons[self.first_cell] = "up"
                        self.ribbons[cell] = "down"
                    else:
                        self.ribbons[self.first_cell] = "down"
                        self.ribbons[cell] = "up"
                else:
                    self.begin(self.first_cell)
                self.flag = not self.flag

    def get_cell(self, mouse_pos):
        for y in range(self.height):
            for x in range(self.width):
                if mouse_pos[0] in range(x * self.cell_size + self.left, (x + 1) * self.cell_size + self.left) and \
                        mouse_pos[1] in range(y * self.cell_size + self.top, (y + 1) * self.cell_size + self.top):
                    return x, y
        return None

    def on_click(self, cell):
        self.board[cell[1]][cell[0]] = 1

    def begin(self, cell):
        self.board[cell[1]][cell[0]] = 0


def main():
    pygame.init()
    size = 500, 550
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Ленточки")

    board = Board(16, 16)
    board.set_view(10, 10, 30)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                board.get_click(event.pos)
        screen.fill((0, 0, 0))
        board.render(screen)
        pygame.display.flip()
    pygame.quit()


main()
