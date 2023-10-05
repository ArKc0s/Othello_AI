import pygame
from game_logic.board import Board
from ia_logic.min_max import MinimaxAI

class GameWindow:
    def __init__(self):
        pygame.init()
        self.width, self.height = 1100, 800
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


    def draw(self, color):
        self.screen.fill((0, 200, 0)) 
        pygame.draw.rect(self.screen, (50,50,50), (self.height, 0, self.width - self.height, self.height))
        font = pygame.font.SysFont(None, 36)
        text = font.render('Joueur vs Joueur', True, (255, 255, 255))
        self.screen.blit(text, (820, 50))
        if color == 'W':
            colorLabel = 'Blanc'
        else:
            colorLabel = 'Noir'
        text = font.render('Tour de jeu : ' + colorLabel, True, (255, 255, 255))
        self.screen.blit(text, (820, 75))
        cell_size = self.height // 8
        for x in range(8):
            for y in range(8):
                pygame.draw.rect(self.screen, (0, 255, 0), (x*cell_size, y*cell_size, cell_size, cell_size), 1)  # Dessine les bordures de chaque cellule
                if self.board.grid[y][x] == 'B':
                    pygame.draw.circle(self.screen, (0, 0, 0), (int((x+0.5)*cell_size), int((y+0.5)*cell_size)), cell_size//2 - 5)
                elif self.board.grid[y][x] == 'W':
                    pygame.draw.circle(self.screen, (255, 255, 255), (int((x+0.5)*cell_size), int((y+0.5)*cell_size)), cell_size//2 - 5)

    def get_grid_position(self, x, y):
        row = y // (self.height / 8)
        col = x // (self.height / 8)
        return int(row), int(col)

    def display_winner(self):
        white_count = 0
        black_count = 0
        back_to_menu = False

        for row in self.board.grid:
            for cell in row:
                if cell == 'W':
                    white_count += 1
                elif cell == 'B':
                    black_count += 1

        font = pygame.font.SysFont(None, 72)
        if white_count > black_count:
            winner_text = "Le gagnant est Blanc!"
        elif black_count > white_count:
            winner_text = "Le gagnant est Noir!"
        else:
            winner_text = "C'est un match nul!"

        text = font.render(winner_text, True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.width // 2, self.height // 2))

        while not back_to_menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                if event.type == pygame.MOUSEBUTTONUP:
                    x, y = pygame.mouse.get_pos()
                    if 400 < x < 700 and 600 < y < 650:
                        back_to_menu = True

            self.screen.blit(text, text_rect)

            # Dessin du bouton "Retour au menu"
            pygame.draw.rect(self.screen, (255, 255, 255), (400, 600, 300, 50))
            small_font = pygame.font.SysFont(None, 36)
            back_text = small_font.render('Retour au menu', True, (0, 0, 0))
            self.screen.blit(back_text, (450, 610))

            pygame.display.flip()

        return 'main_menu'


    def run(self, mode):
        game_over = False
        current_color = "W"  # Commence avec les blancs par exemple

        if mode == "player_vs_player":
            while not game_over:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        game_over = True
                        break

                    if not self.board.valid_moves(current_color):
                        current_color = "B" if current_color == "W" else "W"

                    if event.type == pygame.MOUSEBUTTONUP:
                        x, y = pygame.mouse.get_pos()
                        row, col = self.get_grid_position(x, y)

                        if (row, col) in self.board.valid_moves(current_color):
                            self.board.make_move(row, col, current_color)
                            current_color = "B" if current_color == "W" else "W"

                # Vérification de la fin de partie
                if self.board.is_full() or (not self.board.valid_moves("W") and not self.board.valid_moves("B")):
                    game_over = True
                    next_action = self.display_winner()
                    if next_action == 'main_menu':
                        self.main_menu()  # Retour au menu principal
                        return

                # Dessin du plateau et mise à jour de l'affichage
                self.draw(current_color)
                pygame.display.flip()

        elif mode == "player_vs_ia":
            ai = MinimaxAI(depth=3)
            while not game_over:

                if not self.board.valid_moves(current_color):
                        current_color = "B" if current_color == "W" else "W"

                if current_color == 'B':  # Supposons que 'B' soit la couleur de l'IA
                        row, col = ai.best_move(self.board, 'B')  # Trouve le meilleur mouvement
                        self.board.make_move(row, col, 'B')  # Fait le mouvement
                        current_color = "W"

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        game_over = True
                        break

                    elif event.type == pygame.MOUSEBUTTONUP:
                        x, y = pygame.mouse.get_pos()
                        row, col = self.get_grid_position(x, y)

                        if (row, col) in self.board.valid_moves(current_color):
                            self.board.make_move(row, col, current_color)
                            current_color = "B" if current_color == "W" else "W"

                # Vérification de la fin de partie
                if self.board.is_full() or (not self.board.valid_moves("W") and not self.board.valid_moves("B")):
                    game_over = True
                    next_action = self.display_winner()
                    if next_action == 'main_menu':
                        self.main_menu()  # Retour au menu principal
                        return

                # Dessin du plateau et mise à jour de l'affichage
                self.draw(current_color)
                pygame.display.flip()
           
        elif mode == "ia_vs_ia":
            ai1 = MinimaxAI(depth=3)
            ai2 = MinimaxAI(depth=3)
            
            while not game_over:

                if not self.board.valid_moves(current_color):
                        current_color = "B" if current_color == "W" else "W"

                if current_color == 'W':
                    row, col = ai1.best_move(self.board, 'W')
                else:
                    row, col = ai2.best_move(self.board, 'B')
                self.board.make_move(row, col, current_color)
                current_color = "B" if current_color == "W" else "W"

                # Vérification de la fin de partie
                if self.board.is_full() or (not self.board.valid_moves("W") and not self.board.valid_moves("B")):
                    game_over = True
                    next_action = self.display_winner()
                    if next_action == 'main_menu':
                        self.main_menu()  # Retour au menu principal
                        return

                # Dessin du plateau et mise à jour de l'affichage
                self.draw(current_color)
                pygame.display.flip()

           