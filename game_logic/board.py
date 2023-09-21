class Board:
    def __init__(self):
        self.grid = [[None for _ in range(8)] for _ in range(8)]
        # Initialiser les pièces au centre
        self.grid[3][3], self.grid[3][4], self.grid[4][3], self.grid[4][4] = 'W', 'B', 'B', 'W'

    def valid_moves(self, color):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        moves = []

        for row in range(8):
            for col in range(8):
                if self.grid[row][col] is None:  # Seulement vérifier les cases vides
                    for dx, dy in directions:
                        x, y = col + dx, row + dy
                        while 0 <= x < 8 and 0 <= y < 8:
                            # Si la case adjacente est de la couleur opposée
                            if self.grid[y][x] == ('B' if color == 'W' else 'W'):
                                x, y = x + dx, y + dy
                                while 0 <= x < 8 and 0 <= y < 8 and self.grid[y][x] is not None:
                                    if self.grid[y][x] == color:  # On trouve une pièce de notre couleur pour enfermer l'adversaire
                                        moves.append((row, col))
                                        break
                                    x, y = x + dx, y + dy
                                break
                            else:
                                break

        return moves

    def make_move(self, row, col, color):
        if (row, col) not in self.valid_moves(color):
            return False  # Mouvement non valide

        self.grid[row][col] = color
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]

        for dx, dy in directions:
            x, y = col + dx, row + dy
            pieces_to_flip = []
            while 0 <= x < 8 and 0 <= y < 8:
                if self.grid[y][x] == ('B' if color == 'W' else 'W'):
                    pieces_to_flip.append((x, y))
                    x, y = x + dx, y + dy
                elif self.grid[y][x] == color:
                    for px, py in pieces_to_flip:
                        self.grid[py][px] = color  # On retourne les pièces
                    break
                else:
                    break

        return True