import numpy as np

class Chessboard:
    def __init__(self):
        """1D list representation of the chessboard."""
        self.board = [
            'r', 'n', 'b', 'q', 'k', 'b', 'n', 'r',   # Rank 8
            'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p',   # Rank 7
            '.', '.', '.', '.', '.', '.', '.', '.',   # Rank 6
            '.', '.', '.', '.', '.', '.', '.', '.',   # Rank 5
            '.', '.', '.', '.', '.', '.', '.', '.',   # Rank 4
            '.', '.', '.', '.', '.', '.', '.', '.',   # Rank 3
            'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P',   # Rank 2
            'R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'    # Rank 1
        ]
        self.to_move = "white"
        self.castling_rights = "KQkq"  # Both sides can castle kingside and queenside
        self.en_passant = "-"  # No en passant target square initially
        self.halfmove_clock = 0  # Halfmove clock for the 50-move rule
        self.fullmove_number = 1  # Fullmove number starts at 1

    def print_board(self):
        """Print the current board state."""
        for rank in range(8):
            print(self.board[rank * 8:(rank + 1) * 8])

    def make_move(self, start_index, end_index):
        """Move piece from start_index to end_index."""
        self.board[end_index] = self.board[start_index]
        self.board[start_index] = "."

    def get_square(self, index):
        """Get the piece at the given index."""
        return self.board[index]

    def to_tensor(self):
        """Convert the board to an 8x8x12 tensor for neural networks."""
        tensor = np.zeros((12, 8, 8))
        piece_map = {"P": 0, "N": 1, "B": 2, "R": 3, "Q": 4, "K": 5, 
                     "p": 6, "n": 7, "b": 8, "r": 9, "q": 10, "k": 11}
        
        for idx, piece in enumerate(self.board):
            if piece != ".":
                row, col = divmod(idx, 8)  # Convert 1D index to row, col
                channel = piece_map[piece]
                tensor[channel, row, col] = 1
        
        return tensor

    def to_bitboards(self):
        """Convert the board to bitboards (for MCTS or genetic algorithms)."""
        bitboards = {"white_pawns": 0, "black_pawns": 0, "white_rooks": 0, "black_rooks": 0}
        for idx, piece in enumerate(self.board):
            bit = 1 << idx  # Convert index to a bitmask
            if piece == "P":
                bitboards["white_pawns"] |= bit
            elif piece == "p":
                bitboards["black_pawns"] |= bit
            elif piece == "R":
                bitboards["white_rooks"] |= bit
            elif piece == "r":
                bitboards["black_rooks"] |= bit
        return bitboards
    
    def to_fen(self):
        """Convert the board state to a FEN string."""
        fen_rows = []
        for rank in range(8):
            empty_squares = 0
            row_str = ""
            for file in range(8):
                piece = self.board[rank * 8 + file]
                if piece == ".":
                    empty_squares += 1
                else:
                    if empty_squares > 0:
                        row_str += str(empty_squares)
                        empty_squares = 0
                    row_str += piece
            if empty_squares > 0:
                row_str += str(empty_squares)
            fen_rows.append(row_str)
        
        piece_placement = "/".join(fen_rows)
        active_color = "w" if self.to_move == "white" else "b"
        return f"{piece_placement} {active_color} {self.castling_rights} {self.en_passant} {self.halfmove_clock} {self.fullmove_number}"
    
    def update_from_fen(self, fen):
        """Update the board from a FEN string."""
        fen_parts = fen.split()
        piece_placement, active_color, castling_rights, en_passant, halfmove_clock, fullmove_number = fen_parts

        # Update board pieces
        self.board = []
        for rank in piece_placement.split("/"):
            for char in rank:
                if char.isdigit():
                    self.board.extend(["."] * int(char))  # Empty squares
                else:
                    self.board.append(char)

        # Update turn, castling rights, en passant, and clocks
        self.to_move = "white" if active_color == "w" else "black"
        self.castling_rights = castling_rights
        self.en_passant = en_passant
        self.halfmove_clock = int(halfmove_clock)
        self.fullmove_number = int(fullmove_number)
