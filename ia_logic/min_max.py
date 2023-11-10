import threading

class MinimaxAI:
    """
    Classe implémentant l'algorithme de recherche Min-Max pour le jeu Othello.
    """
    def __init__(self, depth, eval, timeout=5):
        """
        Initialisation de l'IA avec la profondeur de recherche, la méthode d'évaluation,
        et le temps maximum de recherche pour chaque coup.
        """
        # Paramètres de configuration de l'IA
        self.depth = depth
        self.eval = eval
        self.timeout = timeout
        self.best_move_so_far = None

        # Matrices de poids pour l'évaluation de la stratégie positionnelle
        self.position_weights = [
            [ 500, -150,  30,  10,  10,  30, -150,  500],
            [-150, -250, 0, 0, 0, 0, -250, -150],
            [ 30, 0,  1,  2,  2,  1, 0,  30],
            [ 10, 0,  2,  16,  16,  2, 0,  10],
            [ 10, 0,  2,  16,  16,  2, 0,  10],
            [ 30, 0,  1,  2,  2,  1, 0,  30],
            [-150, -250, 0, 0, 0, 0, -250, -150],
            [ 500, -150,  30,  10,  10,  30, -150,  500],
        ]
        self.position_weights2 = [
            [ 100, -20,  10,  5,  5,  10, -20,  100],
            [-20, -50, -2, -2, -2, -2, -50, -20],
            [ 10, -2,  -1,  -1,  -1,  -1, -2,  10],
            [ 5, -2,  -1,  -1,  -1,  -1, -2,  5],
            [ 5, -2,  -1,  -1,  -1,  -1, -2,  5],
            [ 10, -2,  -1,  -1,  -1,  -1, -2,  10],
            [-20, -50, -2, -2, -2, -2, -50, -20],
            [ 100, -20,  10,  5,  5,  10, -20,  100],
        ]
        self.visited_states = {}  # Un dictionnaire pour stocker les états visités et leurs évaluations

        print("Minimax AI initialized with depth", depth)

    def timed_minmax(self, board, color):
        """
        Lance une recherche minmax avec un contrôle de temps.
        """
        self.best_move_so_far = None
        self.best_move(board, color)

    def best_move_with_timeout(self, board, color):
        """
        Détermine le meilleur coup avec le contrôle du temps d'exécution.
        Si le temps imparti est dépassé, le meilleur coup trouvé jusqu'à présent est retourné.
        """
        # Exécution de la recherche minmax dans un thread séparé pour respecter le timeout
        minimax_thread = threading.Thread(target=self.timed_minmax, args=(board, color))
        minimax_thread.start()
        minimax_thread.join(timeout=self.timeout)
        
        if minimax_thread.is_alive():
            print("Timeout, picking best move so far")
            minimax_thread.join() 
        
        return self.best_move_so_far


    def minmax(self, board, depth, maximizing, color):
         """
        Implémentation de l'algorithme de recherche minmax.
        """
        # Base de récursivité : si la profondeur est nulle ou le plateau est plein
        if depth == 0 or board.is_full():
            return self.evaluate_pos(board, color)

        # Traitement récursif des mouvements
        board_state = tuple(tuple(row) for row in board.grid)
        if board_state in self.visited_states:
            return self.visited_states[board_state]

        if maximizing:
            max_eval = float('-inf')
            for move in board.valid_moves(color):
                board.make_move(move[0], move[1], color)
                eval = self.minmax(board, depth - 1, False, 'W' if color == 'B' else 'B')
                board.undo_move() 
                max_eval = max(max_eval, eval)
                self.visited_states[board_state] = max_eval 
            return max_eval
        else:
            min_eval = float('inf')
            for move in board.valid_moves(color):
                board.make_move(move[0], move[1], color)
                eval = self.minmax(board, depth - 1, True, 'W' if color == 'B' else 'B')
                board.undo_move() 
                min_eval = min(min_eval, eval)
                self.visited_states[board_state] = min_eval
            return min_eval

    def best_move(self, board, color):
         """
        Trouve le meilleur coup à jouer pour la couleur donnée.
        """
        # Recherche du coup offrant la meilleure évaluation
        max_eval = float('-inf')
        best_move = None
        board_state = tuple(tuple(row) for row in board.grid)
        for move in board.valid_moves(color):
            board.make_move(move[0], move[1], color)
            eval = self.minmax(board, self.depth - 1, False, 'W' if color == 'B' else 'B')
            board.undo_move()
            
            if eval > max_eval:
                max_eval = eval
                best_move = move
            self.best_move_so_far = best_move
        self.visited_states[board_state] = max_eval 
        return best_move

    # Les méthodes d'évaluation utilisées pour estimer la valeur d'un plateau de jeu
    def absolu(self, board, color):
        return sum(cell == color for row in board.grid for cell in row)
    
    def positionnel(self, board, color, int):
        if int == 1:
            score = 0
            for i in range(8):
                for j in range(8):
                    if board.grid[i][j] == color:
                        score += self.position_weights[i][j]
            return score
        else: 
            score = 0
            for i in range(8):
                for j in range(8):
                    if board.grid[i][j] == color:
                        score += self.position_weights2[i][j]
            return score
        
    def mobilite(self, board, color):
        opponent_color = 'W' if color == 'B' else 'B'
            
        my_moves = len(board.valid_moves(color))
        opponent_moves = len(board.valid_moves(opponent_color))
        
        # Attribue des poids élevés aux coins
        corners = [(0,0), (0,7), (7,0), (7,7)]
        corner_score = 0
        for x, y in corners:
            if board.grid[x][y] == color:
                corner_score += 1000
            elif board.grid[x][y] == opponent_color:
                corner_score -= 1000
        
        return (my_moves - opponent_moves) + corner_score
    
    def mixte(self, board, color):
        num_empty_cells = sum(cell is None for row in board.grid for cell in row)
        num_total_cells = 8 * 8  # pour un plateau 8x8
        num_played_cells = num_total_cells - num_empty_cells

        if num_played_cells <= 25:  # Début de partie
            return self.positionnel(board, color, 1)  # Utiliser "1" ou "2" selon la stratégie de positionnement que tu veux
        elif 25 < num_played_cells <= (num_total_cells - 16):  # Milieu de partie
            return self.mobilite(board, color)
        else:  # Fin de partie
            return self.absolu(board, color)

    
    def evaluate_pos(self, board, color):
        """
        Sélectionne et applique la méthode d'évaluation en fonction de la configuration choisie.
        """
        # Appel de la méthode d'évaluation en fonction du choix de stratégie
        if(self.eval == "absolu"):
            return self.absolu(board, color)
        elif(self.eval == "positionnel 1"):
            return self.positionnel(board, color, 1)
        elif(self.eval == "positionnel 2"):
            return self.positionnel(board, color, 2)
        elif self.eval == "mobilité":
            return self.mobilite(board, color)
        elif self.eval == "mixte":
            return self.mixte(board, color)
