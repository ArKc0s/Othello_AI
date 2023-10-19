import threading

class MinimaxAI:
    def __init__(self, depth, timeout=5):
        self.depth = depth
        self.timeout = timeout
        self.best_move_so_far = None
        self.position_weights = [
            [ 4, -3,  2,  2,  2,  2, -3,  4],
            [-3, -4, -1, -1, -1, -1, -4, -3],
            [ 2, -1,  1,  0,  0,  1, -1,  2],
            [ 2, -1,  0,  1,  1,  0, -1,  2],
            [ 2, -1,  0,  1,  1,  0, -1,  2],
            [ 2, -1,  1,  0,  0,  1, -1,  2],
            [-3, -4, -1, -1, -1, -1, -4, -3],
            [ 4, -3,  2,  2,  2,  2, -3,  4],
        ]

    def timed_minmax(self, board, color):
        self.best_move_so_far = None
        self.best_move(board, color)

    def best_move_with_timeout(self, board, color):
        minimax_thread = threading.Thread(target=self.timed_minmax, args=(board, color))
        minimax_thread.start()
        minimax_thread.join(timeout=self.timeout)
        
        if minimax_thread.is_alive():
            print("Timeout, picking best move so far")
            minimax_thread.join() 
        
        return self.best_move_so_far


    def minmax(self, board, depth, maximizing, color):
        if depth == 0 or board.is_full():
            return self.evaluate_pos(board, color)

        if maximizing:
            max_eval = float('-inf')
            for move in board.valid_moves(color):
                board.make_move(move[0], move[1], color)
                eval = self.minmax(board, depth - 1, False, 'W' if color == 'B' else 'B')
                board.undo_move() 
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float('inf')
            for move in board.valid_moves(color):
                board.make_move(move[0], move[1], color)
                eval = self.minmax(board, depth - 1, True, 'W' if color == 'B' else 'B')
                board.undo_move() 
                min_eval = min(min_eval, eval)
            return min_eval

    def best_move(self, board, color):
        max_eval = float('-inf')
        best_move = None
        for move in board.valid_moves(color):
            board.make_move(move[0], move[1], color)
            eval = self.minmax(board, self.depth - 1, False, 'W' if color == 'B' else 'B')
            board.undo_move()
            
            if eval > max_eval:
                max_eval = eval
                best_move = move
            self.best_move_so_far = best_move 
        return best_move

    def evaluate(self, board, color):
        return sum(cell == color for row in board.grid for cell in row)
    
    def evaluate_pos(self, board, color):
        score = 0
        for i in range(8):
            for j in range(8):
                if board.grid[i][j] == color:
                    score += self.position_weights[i][j]
        return score
