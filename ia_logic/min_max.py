class MinimaxAI:
    def __init__(self, depth):
        self.depth = depth

    def minimax(self, board, depth, maximizing, color):
        if depth == 0 or board.is_full():
            return self.evaluate(board, color)

        if maximizing:
            max_eval = float('-inf')
            for move in board.valid_moves(color):
                board.make_move(move[0], move[1], color)
                eval = self.minimax(board, depth - 1, False, 'W' if color == 'B' else 'B')
                board.undo_move() 
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float('inf')
            for move in board.valid_moves(color):
                board.make_move(move[0], move[1], color)
                eval = self.minimax(board, depth - 1, True, 'W' if color == 'B' else 'B')
                board.undo_move() 
                min_eval = min(min_eval, eval)
            return min_eval

    def best_move(self, board, color):
        max_eval = float('-inf')
        best_move = None
        for move in board.valid_moves(color):
            board.make_move(move[0], move[1], color)
            eval = self.minimax(board, self.depth - 1, False, 'W' if color == 'B' else 'B')
            board.undo_move()  
            if eval > max_eval:
                max_eval = eval
                best_move = move
        return best_move

    def evaluate(self, board, color):
        return sum(cell == color for row in board.grid for cell in row)
