import threading

class NegaMaxAI:
    def __init__(self, depth, eval, timeout=5):
        self.depth = depth
        self.eval = eval
        self.timeout = timeout
        self.best_move_so_far = None
        self.visited_states = {}
        print("NegaMax AI initialized with depth", depth)

    def timed_negamax(self, board, color):
        self.best_move_so_far = None
        self.best_move(board, color)

    def best_move_with_timeout(self, board, color):
        negamax_thread = threading.Thread(target=self.timed_negamax, args=(board, color))
        negamax_thread.start()
        negamax_thread.join(timeout=self.timeout)

        if negamax_thread.is_alive():
            print("Timeout, picking best move so far")
            negamax_thread.join()

        return self.best_move_so_far

    def negamax(self, board, depth, alpha, beta, color):
        if depth == 0 or board.is_full():
            return self.evaluate_pos(board, color)

        board_state = tuple(tuple(row) for row in board.grid)
        if board_state in self.visited_states:
            return self.visited_states[board_state]

        max_eval = float('-inf')

        for move in board.valid_moves(color):
            board.make_move(move[0], move[1], color)
            eval = -self.negamax(board, depth - 1, -beta, -alpha, 'W' if color == 'B' else 'B')
            board.undo_move()

            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if alpha >= beta:
                break

        self.visited_states[board_state] = max_eval
        return max_eval

    def best_move(self, board, color):
        max_eval = float('-inf')
        best_move = None
        alpha = float('-inf')
        beta = float('inf')

        for move in board.valid_moves(color):
            board.make_move(move[0], move[1], color)
            eval = -self.negamax(board, self.depth - 1, -beta, -alpha, 'W' if color == 'B' else 'B')
            board.undo_move()

            if eval > max_eval:
                max_eval = eval
                best_move = move
                alpha = max(alpha, eval)

            self.best_move_so_far = best_move

        return best_move

    def evaluate_pos(self, board, color):
        if(self.eval == "absolu"):
            return sum(cell == color for row in board.grid for cell in row)
        elif(self.eval == "positionnel 1"):
            score = 0
            for i in range(8):
                for j in range(8):
                    if board.grid[i][j] == color:
                        score += self.position_weights[i][j]
            return score
        elif(self.eval == "positionnel 2"):
            score = 0
            for i in range(8):
                for j in range(8):
                    if board.grid[i][j] == color:
                        score += self.position_weights2[i][j]
            return score