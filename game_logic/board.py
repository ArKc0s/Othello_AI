class Board:
    def __init__(self):
        self.grid = [[None for _ in range(8)] for _ in range(8)]
        # Initialiser les pièces au centre
        self.grid[3][3], self.grid[3][4], self.grid[4][3], self.grid[4][4] = 'white', 'black', 'black', 'white'

    def valid_moves(self, color):
        # TODO: retourne une liste de mouvements valides pour une couleur donnée
        pass

    def make_move(self, row, col, color):
        # TODO: effectue un mouvement et met à jour le plateau
        pass