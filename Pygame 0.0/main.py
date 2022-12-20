import pygame


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]

        self.left = 10
        self.top = 10
        self.cell_size = 30

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(screen, (255, 255, 255), (x * self.cell_size + self.left,
                                                           y * self.cell_size + self.top,
                                                           self.cell_size, self.cell_size), 1)

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)

    def get_cell(self, mouse_pos):
        for y in range(self.height):
            for x in range(self.width):
                if mouse_pos[0] in range(x * self.cell_size + self.left, (x + 1) * self.cell_size + self.left) and \
                        mouse_pos[1] in range(y * self.cell_size + self.top, (y + 1) * self.cell_size + self.top):
                    return x, y
        return None

    def on_click(self, cell):
        pass


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
        screen.fill((0, 0, 0))
        board.render(screen)
        pygame.display.flip()
    pygame.quit()


main()
