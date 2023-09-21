import pygame
from game_logic.board import Board

class GameWindow:
    def __init__(self):
        pygame.init()
        self.width, self.height = 800, 800
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Othello')
        self.board = Board()
        # TODO: Charger des assets, initialiser d'autres éléments d'interface

    def draw(self):
        self.screen.fill((0, 200, 0)) 
        cell_size = self.width // 8
        for x in range(8):
            for y in range(8):
                pygame.draw.rect(self.screen, (0, 255, 0), (x*cell_size, y*cell_size, cell_size, cell_size), 1)  # Dessine les bordures de chaque cellule
                if self.board.grid[y][x] == 'black':
                    pygame.draw.circle(self.screen, (0, 0, 0), (int((x+0.5)*cell_size), int((y+0.5)*cell_size)), cell_size//2 - 5)
                elif self.board.grid[y][x] == 'white':
                    pygame.draw.circle(self.screen, (255, 255, 255), (int((x+0.5)*cell_size), int((y+0.5)*cell_size)), cell_size//2 - 5)


    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.draw()
            pygame.display.flip()
        pygame.quit()