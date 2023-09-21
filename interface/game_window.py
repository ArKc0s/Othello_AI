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

    def main_menu(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                if event.type == pygame.MOUSEBUTTONUP:
                    x, y = pygame.mouse.get_pos()
                    
                    if 100 < x < 300:
                        if 200 < y < 250:
                            return 'player_vs_player'
                        elif 300 < y < 350:
                            return 'player_vs_ia'
                        elif 400 < y < 450:
                            return 'ia_vs_ia'

            self.screen.fill((144, 238, 144))
            pygame.draw.rect(self.screen, (0, 0, 0), (100, 200, 200, 50))
            pygame.draw.rect(self.screen, (0, 0, 0), (100, 300, 200, 50))
            pygame.draw.rect(self.screen, (0, 0, 0), (100, 400, 200, 50))

            font = pygame.font.SysFont(None, 36)
            text = font.render('Joueur vs Joueur', True, (255, 255, 255))
            self.screen.blit(text, (110, 210))
            text = font.render('Joueur vs IA', True, (255, 255, 255))
            self.screen.blit(text, (110, 310))
            text = font.render('IA vs IA', True, (255, 255, 255))
            self.screen.blit(text, (110, 410))

            pygame.display.flip()


    def draw(self):
        self.screen.fill((0, 200, 0)) 
        cell_size = self.width // 8
        for x in range(8):
            for y in range(8):
                pygame.draw.rect(self.screen, (0, 255, 0), (x*cell_size, y*cell_size, cell_size, cell_size), 1)  # Dessine les bordures de chaque cellule
                if self.board.grid[y][x] == 'B':
                    pygame.draw.circle(self.screen, (0, 0, 0), (int((x+0.5)*cell_size), int((y+0.5)*cell_size)), cell_size//2 - 5)
                elif self.board.grid[y][x] == 'W':
                    pygame.draw.circle(self.screen, (255, 255, 255), (int((x+0.5)*cell_size), int((y+0.5)*cell_size)), cell_size//2 - 5)


    def run(self, mode):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.draw()
            pygame.display.flip()
        pygame.quit()