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
        # TODO: Dessiner le plateau et les pièces
        pass

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.draw()
            pygame.display.flip()
        pygame.quit()