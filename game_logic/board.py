import copy

class Board:
    def __init__(self):
        """
        Initialise le plateau de jeu en plaçant quatre pions au centre.
        La grille est représentée par une liste 8x8 où chaque élément peut être 'B', 'W', ou None.
        Un stack de mouvements est également initialisé pour gérer les annulations de coups.
        """
        self.grid = [[None for _ in range(8)] for _ in range(8)]
        # Initialisation des pions au centre du plateau
        self.grid[3][3], self.grid[3][4], self.grid[4][3], self.grid[4][4] = 'W', 'B', 'B', 'W'
        self.move_stack = []

    def valid_moves(self, color):
        """
        Détermine les mouvements valides pour le joueur de la couleur spécifiée.
        Un mouvement est valide s'il encercle au moins un pion adverse et le transforme.
        :param color: 'B' ou 'W' pour la couleur du joueur.
        :return: Liste de tuples (row, col) où les mouvements sont valides.
        """
        # Directions possibles à vérifier (horizontales, verticales et diagonales)
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        moves = []  # Liste pour stocker les mouvements valides

        # Parcourir chaque cellule de la grille pour trouver les mouvements valides
        for row in range(8):
            for col in range(8):
                # Seulement vérifier les cases vides pour des mouvements potentiels
                if self.grid[row][col] is None:
                    # Vérifier chaque direction à partir de la case vide
                    for dx, dy in directions:
                        x, y = col + dx, row + dy
                        while 0 <= x < 8 and 0 <= y < 8:
                            # Vérifie si la case adjacente contient un pion de la couleur opposée
                            if self.grid[y][x] == ('B' if color == 'W' else 'W'):
                                # Continue à vérifier dans la même direction
                                x, y = x + dx, y + dy
                                while 0 <= x < 8 and 0 <= y < 8 and self.grid[y][x] is not None:
                                    # Si on trouve une pièce de la même couleur, c'est un mouvement valide
                                    if self.grid[y][x] == color:
                                        moves.append((row, col))
                                        break
                                    x, y = x + dx, y + dy
                                break
                            else:
                                break

        return moves

    def make_move(self, row, col, color):
        """
        Effectue un mouvement sur le plateau à la position spécifiée, si elle est valide.
        :param row: Ligne du mouvement.
        :param col: Colonne du mouvement.
        :param color: 'B' ou 'W' pour la couleur du joueur.
        :return: Booléen indiquant si le mouvement a été effectué.
        """
        # Sauvegarde l'état actuel du plateau avant de faire le mouvement
        prev_state = copy.deepcopy(self.grid)
        # Ajoute l'état précédent au stack pour pouvoir annuler le coup plus tard
        self.move_stack.append((row, col, prev_state))
        # Si le mouvement n'est pas valide, retourne False
        if (row, col) not in self.valid_moves(color):
            return False

        # Réalise le mouvement
        self.grid[row][col] = color
        # Liste des directions pour vérifier les pions à retourner
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]

        # Retourne les pions adverses encerclés
        for dx, dy in directions:
            x, y = col + dx, row + dy
            pieces_to_flip = []  # Liste des pions à retourner
            while 0 <= x < 8 and 0 <= y < 8:
                if self.grid[y][x] == ('B' if color == 'W' else 'W'):
                    # Si on trouve un pion adverse, on l'ajoute à la liste des pions à retourner
                    pieces_to_flip.append((x, y))
                    x, y = x + dx, y + dy
                elif self.grid[y][x] == color:
                    # Si on trouve un pion de la même couleur, on retourne tous les pions adverses trouvés
                    for px, py in pieces_to_flip:
                        self.grid[py][px] = color
                    break
                else:
                    break

        return True
    
    def undo_move(self):
        """
        Annule le dernier mouvement effectué sur le plateau.
        :return: None
        """
        # Si le stack de mouvements n'est pas vide, annule le dernier mouvement
        if self.move_stack:
            _, _, prev_state = self.move_stack.pop()
            self.grid = prev_state

    def is_full(self):
        """
        Vérifie si le plateau est complètement rempli de pions.
        :return: Booléen indiquant si le plateau est plein.
        """
        # Parcours chaque cellule du plateau pour vérifier si elle est vide
        for row in self.grid:
            for cell in row:
                if cell is None:
                    return False
        return True
    
    def print_board(self):
        """
        Affiche le plateau dans la console pour le débogage.
        :return: None
        """
        # Affiche chaque ligne du plateau avec des séparateurs
        for row in self.grid:
            row_str = "|".join([" " if cell is None else cell for cell in row])
            print(row_str)
            print("-" * len(row_str))
    
    def reset(self):
        """
        Réinitialise le plateau à son état initial avec quatre pions au centre.
        :return: None
        """
        # Affiche le plateau pour le débogage
        self.print_board()
        # Réinitialise la grille et les pions au centre
        self.grid = [[None for _ in range(8)] for _ in range(8)]
        self.grid[3][3], self.grid[3][4], self.grid[4][3], self.grid[4][4] = 'W', 'B', 'B', 'W'
        # Vide le stack de mouvements
        self.move_stack = []
