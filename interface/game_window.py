import pygame
from game_logic.board import Board
from ia_logic.min_max import MinimaxAI
from ia_logic.alpha_beta import AlphaBetaAI
from ia_logic.nega_max import NegaMaxAI
import time

class GameWindow:
    def __init__(self):
        pygame.init()
        self.width, self.height = 1100, 800
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Othello')
        self.board = Board()
        self.ia1 = None
        self.ia2 = None

    def main_menu(self):
        running = True
        algo_menu1 = DropdownMenu(50, 550, 200, 40, ['minmax', 'alphabeta', 'negamax'], "Algo")
        eval_menu1 = DropdownMenu(275, 550, 200, 40, ['absolu', 'positionnel 1', 'positionnel 2', 'mobilité', 'mixte'], "Evaluation")
        algo_menu2 = DropdownMenu(625, 550, 200, 40, ['minmax', 'alphabeta', 'negamax'], "Algo")
        eval_menu2 = DropdownMenu(850, 550, 200, 40, ['absolu', 'positionnel 1', 'positionnel 2', 'mobilité', 'mixte'], "Evaluation")
        input_box1 = InputBox(50, 470, 140, 32, label='Profondeur')
        input_box2 = InputBox(625, 470, 140, 32, label='Profondeur')
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                if event.type == pygame.MOUSEBUTTONUP:
                    x, y = pygame.mouse.get_pos()
                    
                    if 400 < x < 700:
                        if 150 < y < 200:
                            return 'player_vs_player'
                        elif 250 < y < 300:

                            algo_choice1 = algo_menu1.selected_option
                            eval_choice1 = eval_menu1.selected_option
                            depth = input_box1.text

                            if depth == '' or depth == None or not depth.isdigit():
                                depth = 3
                            else:
                                depth = int(depth)
                            
                            if algo_choice1 == 'minmax':
                                self.ia1 = MinimaxAI(depth, eval_choice1)
                            elif algo_choice1 == 'alphabeta':
                                self.ia1 = AlphaBetaAI(depth, eval_choice1)
                            elif algo_choice1 == 'negamax':
                                self.ia1 = NegaMaxAI(depth, eval_choice1)

                            return 'player_vs_ia'
                        elif 350 < y < 400:
                            algo_choice1 = algo_menu1.selected_option
                            eval_choice1 = eval_menu1.selected_option
                            depth1 = input_box1.text
                            depth2 = input_box2.text

                            if depth1 == '' or depth1 == None or not depth1.isdigit():
                                depth1 = 3
                            else:
                                depth1 = int(depth1)

                            if depth2 == '' or depth2 == None or not depth2.isdigit():
                                depth2 = 3
                            else:
                                depth2 = int(depth2)
                            
                            if algo_choice1 == 'minmax':
                                self.ia1 = MinimaxAI(depth1, eval_choice1)
                            elif algo_choice1 == 'alphabeta':
                                self.ia1 = AlphaBetaAI(depth1, eval_choice1)
                            elif algo_choice1 == 'negamax':
                                self.ia1 = NegaMaxAI(depth1, eval_choice1)

                            algo_choice2 = algo_menu2.selected_option
                            eval_choice2 = eval_menu2.selected_option
                          
                            if algo_choice2 == 'minmax':
                                self.ia2 = MinimaxAI(depth2, eval_choice2)
                            elif algo_choice2 == 'alphabeta':
                                self.ia2 = AlphaBetaAI(depth2, eval_choice2)
                            elif algo_choice2 == 'negamax':
                                self.ia2 = NegaMaxAI(depth2, eval_choice2)

                            return 'ia_vs_ia'
                        
                algo_menu1.handle_event(event)
                eval_menu1.handle_event(event)
                algo_menu2.handle_event(event)
                eval_menu2.handle_event(event)
                input_box1.handle_event(event)
                input_box2.handle_event(event)

            self.screen.fill((120, 138, 163))
            pygame.draw.rect(self.screen, (0, 0, 0), (400, 150, 300, 50))
            pygame.draw.rect(self.screen, (0, 0, 0), (400, 250, 300, 50))
            pygame.draw.rect(self.screen, (0, 0, 0), (400, 350, 300, 50))

            font = pygame.font.SysFont(None, 50)
            text= font.render('Othello AI', True, (255, 255, 255))
            self.screen.blit(text, (470, 50))
            font = pygame.font.SysFont(None, 36)
            text = font.render('Joueur vs Joueur', True, (255, 255, 255))
            self.screen.blit(text, (445, 160))
            text = font.render('Joueur vs IA', True, (255, 255, 255))
            self.screen.blit(text, (475, 260))
            text = font.render('IA vs IA', True, (255, 255, 255))
            self.screen.blit(text, (505, 360))

            algo_menu1.draw(self.screen)
            eval_menu1.draw(self.screen)
            algo_menu2.draw(self.screen)
            eval_menu2.draw(self.screen)
            input_box1.draw(self.screen)
            input_box2.draw(self.screen)

            pygame.display.flip()


    def draw(self, mode, color):
        self.screen.fill((0, 200, 0)) 
        pygame.draw.rect(self.screen, (50,50,50), (self.height, 0, self.width - self.height, self.height))
        font = pygame.font.SysFont(None, 36)
        if(mode == 'player_vs_ia'):
            text = font.render('Joueur vs IA', True, (255, 255, 255))
        elif(mode == 'ia_vs_ia'):
            text = font.render('IA vs IA', True, (255, 255, 255))
        else:
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

        if white_count > black_count:
            winner_text = "Le gagnant est Blanc!"
        elif black_count > white_count:
            winner_text = "Le gagnant est Noir!"
        else:
            winner_text = "C'est un match nul!"

        font = pygame.font.SysFont(None, 36)
        text = font.render(winner_text, True, (255, 255, 255))
        self.screen.blit(text, (825, 700))

        while not back_to_menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                if event.type == pygame.MOUSEBUTTONUP:
                    x, y = pygame.mouse.get_pos()
                    if 825 < x < 1075 and 750 < y < 800:
                        back_to_menu = True

            

            # Dessin du bouton "Retour au menu"
            pygame.draw.rect(self.screen, (255, 255, 255), (825, 740, 250, 50))
            small_font = pygame.font.SysFont(None, 36)
            back_text = small_font.render('Retour au menu', True, (0, 0, 0))
            self.screen.blit(back_text, (860, 750))

            pygame.display.flip()

        return 'main_menu'


    def run(self, mode):
        game_over = False
        current_color = "W"  # Commence avec les blancs par exemple

        total_time = 0.0
        total_time_ai1 = 0.0
        total_time_ai2 = 0.0

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
                        self.board.reset()
                        mode = self.main_menu()  # Retour au menu principal
                        self.run(mode)
                        return

                # Dessin du plateau et mise à jour de l'affichage
                self.draw(mode, current_color)
                pygame.display.flip()

        elif mode == "player_vs_ia":
            ai = self.ia1
            while not game_over:

                if not self.board.valid_moves(current_color):
                        current_color = "B" if current_color == "W" else "W"

                if current_color == 'B':  # Supposons que 'B' soit la couleur de l'IA
                        #wait 0.5 second
                        pygame.time.wait(500)

                        bMove = ai.best_move_with_timeout(self.board, 'B')
                        if bMove != None:
                            row, col = bMove
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

                # Dessin du plateau et mise à jour de l'affichage
                self.draw(mode, current_color)
                pygame.display.flip()

                # Vérification de la fin de partie
                if self.board.is_full() or (not self.board.valid_moves("W") and not self.board.valid_moves("B")):
                    game_over = True
                    next_action = self.display_winner()
                    if next_action == 'main_menu':
                        self.board.reset()
                        mode = self.main_menu()  # Retour au menu principal
                        self.run(mode)
                        return

                
           
        elif mode == "ia_vs_ia":
            ai1 = self.ia1
            ai2 = self.ia2
            
            while not game_over:

                if not self.board.valid_moves(current_color):
                        current_color = "B" if current_color == "W" else "W"

                if current_color == 'W':
                    start_time = time.time()
                    bMove = ai1.best_move_with_timeout(self.board, 'W')
                    end_time = time.time()

                    print("Temps de calcul de l'IA 1 :", end_time - start_time)
                    total_time += end_time - start_time
                    total_time_ai1 += end_time - start_time

                    if bMove != None:
                        row, col = bMove
                else:
                    start_time = time.time()
                    bMove = ai2.best_move_with_timeout(self.board, 'B')
                    end_time = time.time()
                    print("Temps de calcul de l'IA 2 :", end_time - start_time)
                    total_time += end_time - start_time
                    total_time_ai2 += end_time - start_time
                    
                    if bMove != None:
                        row, col = bMove
                self.board.make_move(row, col, current_color)
                current_color = "B" if current_color == "W" else "W"

                # Dessin du plateau et mise à jour de l'affichage
                self.draw(mode, current_color)
                pygame.display.flip()

                # Vérification de la fin de partie
                if self.board.is_full() or (not self.board.valid_moves("W") and not self.board.valid_moves("B")):
                    game_over = True
                    print("Temps de calcul total :", total_time)
                    print("Temps de calcul total IA 1 :", total_time_ai1)
                    print("Temps de calcul total IA 2 :", total_time_ai2)
                    next_action = self.display_winner()
                    if next_action == 'main_menu':
                        self.board.reset()
                        mode = self.main_menu()  # Retour au menu principal
                        self.run(mode)
                        return

class DropdownMenu:
    def __init__(self, x, y, w, h, options, label):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.options = options
        self.selected_option = options[0]
        self.is_open = False
        self.font = pygame.font.SysFont(None, 36)
        self.label = label
        self.label_font = pygame.font.SysFont(None, 24)

    def draw(self, screen):
        label_surface = self.label_font.render(self.label, True, (255, 255, 255))
        screen.blit(label_surface, (self.x, self.y - 30))
        pygame.draw.rect(screen, (0, 0, 0), (self.x, self.y, self.w, self.h))
        text = self.font.render(self.selected_option, True, (255, 255, 255))
        screen.blit(text, (self.x + 10, self.y + 10))
        
        if self.is_open:
            for i, option in enumerate(self.options):
                pygame.draw.rect(screen, (0, 0, 0), (self.x, self.y + (i+1)*self.h, self.w, self.h))
                text = self.font.render(option, True, (255, 255, 255))
                screen.blit(text, (self.x + 10, self.y + (i+1)*self.h + 10))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            x, y = pygame.mouse.get_pos()
            if self.x < x < self.x + self.w and self.y < y < self.y + self.h:
                self.is_open = not self.is_open
                return True
            elif self.is_open:
                for i, option in enumerate(self.options):
                    if self.x < x < self.x + self.w and self.y + (i+1)*self.h < y < self.y + (i+2)*self.h:
                        self.selected_option = option
                        self.is_open = False
                        return True
        return False               
                
class InputBox:
    def __init__(self, x, y, w, h, text='', label = ''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = (255, 255, 255)
        self.text = text
        self.font = pygame.font.Font(None, 32)
        self.txt_surface = self.font.render(text, True, self.color)
        self.label = label
        self.label_font = pygame.font.SysFont(None, 24)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.color = (0, 128, 255)
            else:
                self.color = (255, 255, 255)
        elif event.type == pygame.KEYDOWN:
            if self.color == (0, 128, 255):
                if event.key == pygame.K_RETURN:
                    depth = int(self.text)
                    self.text = ''
                    return depth
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = self.font.render(self.text, True, self.color)
        
    def draw(self, screen):
        label_surface = self.label_font.render(self.label, True, (255, 255, 255))
        screen.blit(label_surface, (self.rect.x, self.rect.y - 30))
        pygame.draw.rect(screen, self.color, self.rect, 2)
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))

           