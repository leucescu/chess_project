from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QGridLayout, QVBoxLayout, QSizePolicy
from PyQt5.QtGui import QPixmap, QColor, QPainter, QBrush, QPen
from PyQt5.QtCore import Qt
from src.chessboard.chessboard import Chessboard


class ChessGUI(QWidget):
    def __init__(self, return_to_menu_callback, parent=None):
        super().__init__(parent)
        self.return_to_menu_callback = return_to_menu_callback
        self.chessboard = Chessboard()
        self.selected_piece = None  # To store the selected piece's position
        self.selected_piece_label = None  # To store the label for the selected piece
        # Create a mapping of FEN characters to piece image filenames
        self.fen_to_image = {
            'P': 'Chess_plt60.png', 'N': 'Chess_nlt60.png', 'B': 'Chess_blt60.png', 'R': 'Chess_rlt60.png', 'Q': 'Chess_qlt60.png', 'K': 'Chess_klt60.png',
            'p': 'Chess_pdt60.png', 'n': 'Chess_ndt60.png', 'b': 'Chess_bdt60.png', 'r': 'Chess_rdt60.png', 'q': 'Chess_qdt60.png', 'k': 'Chess_kdt60.png'
        }
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Chess GUI')

        # Set the size of the ChessGUI window
        self.setGeometry(560, 140, 800, 800)  # Initial size

        # Create a main layout
        main_layout = QVBoxLayout(self)
        self.setLayout(main_layout)

        # Create a grid layout for the board and labels
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(0)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)

        # Create a widget to hold the grid layout
        self.grid_layout_widget = QWidget()
        self.grid_layout_widget.setLayout(self.grid_layout)

        # Add the grid layout widget to the main layout
        main_layout.addWidget(self.grid_layout_widget, alignment=Qt.AlignCenter)

        # Add the return to menu button
        return_button = QPushButton('Return to Main Menu')
        return_button.clicked.connect(self.return_to_menu_callback)
        main_layout.addWidget(return_button)

        # Set a fixed maximum size for the chessboard to prevent excessive expansion
        self.grid_layout_widget.setMaximumSize(800, 800)

        # Define the colors for the chessboard
        self.light_color = QColor(240, 217, 181)  # Light square color
        self.dark_color = QColor(181, 136, 99)    # Dark square color

        self.last_clicked = None  # To store the last clicked square

        # Initialize the chessboard with labels and pieces
        self.initialize_board()

    def initialize_board(self):
        """Initializes the chessboard with alternating colors and FEN-based pieces."""
        self.labels = {}  # Dictionary to store the labels for each square

        # Letters for files (columns)
        files = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        # Numbers for ranks (rows)
        ranks = ['8', '7', '6', '5', '4', '3', '2', '1']

        # Add rank labels (numbers) on left and right
        for row in range(8):
            rank_label_left = QLabel(ranks[row])
            rank_label_left.setAlignment(Qt.AlignCenter)
            rank_label_left.setFixedSize(20, 80)  # Set fixed size for labels
            self.grid_layout.addWidget(rank_label_left, row + 1, 0)

            rank_label_right = QLabel(ranks[row])
            rank_label_right.setAlignment(Qt.AlignCenter)
            rank_label_right.setFixedSize(20, 80)  # Set fixed size for labels
            self.grid_layout.addWidget(rank_label_right, row + 1, 9)

        # Add file labels (letters) on top and bottom
        for col in range(8):
            file_label_top = QLabel(files[col])
            file_label_top.setAlignment(Qt.AlignCenter)
            file_label_top.setFixedSize(80, 20)  # Set fixed size for labels
            self.grid_layout.addWidget(file_label_top, 0, col + 1)

            file_label_bottom = QLabel(files[col])
            file_label_bottom.setAlignment(Qt.AlignCenter)
            file_label_bottom.setFixedSize(80, 20)  # Set fixed size for labels
            self.grid_layout.addWidget(file_label_bottom, 9, col + 1)

        # Initialize empty labels for all squares
        for row in range(8):
            for col in range(8):
                label = QLabel()
                label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                label.setAlignment(Qt.AlignCenter)

                # Set the background color of the square
                if (row + col) % 2 == 0:
                    label.setStyleSheet(f"background-color: {self.light_color.name()};")
                else:
                    label.setStyleSheet(f"background-color: {self.dark_color.name()};")

                self.grid_layout.addWidget(label, row + 1, col + 1)
                self.labels[(row, col)] = label

        # Load the initial board position using FEN from Chessboard
        self.load_fen(self.chessboard.to_fen())

    def resizeEvent(self, event):
        """Handle the window resize event to dynamically adjust the size of the chessboard and pieces."""
        grid_widget_width = self.grid_layout_widget.width()
        grid_widget_height = self.grid_layout_widget.height()
        new_size = min(grid_widget_width, grid_widget_height - 40) // 8  # Adjust for labels

        for row in range(8):
            for col in range(8):
                item = self.grid_layout.itemAtPosition(row + 1, col + 1)
                if item is not None:
                    label = item.widget()
                    label.setFixedSize(new_size, new_size)

                    # Resize the pixmap if there is a piece on this square
                    if (row, col) in self.positions:
                        pixmap = QPixmap(f'src/gui/chess_pieces/{self.positions[(row, col)]}')
                        label.setPixmap(pixmap.scaled(new_size, new_size, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        super().resizeEvent(event)

    def mousePressEvent(self, event):
        """Handle the mouse click event to highlight the clicked piece or move it."""
        x_offset = 20  # Rank labels width
        y_offset = 20  # File labels height

        grid_widget_width = self.grid_layout_widget.width() - 2 * x_offset
        grid_widget_height = self.grid_layout_widget.height() - 2 * y_offset
        new_size = min(grid_widget_width, grid_widget_height) // 8

        # Get the clicked square coordinates (x, y)
        x = (event.x() - self.grid_layout_widget.x() - x_offset) // new_size
        y = (event.y() - self.grid_layout_widget.y() - y_offset) // new_size

        # Check if the click is within the valid chessboard area
        if 0 <= x < 8 and 0 <= y < 8:
            clicked_square = (y, x)

            if self.selected_piece is None:
                # First click: selecting a piece
                if clicked_square in self.positions:
                    # Highlight the selected piece
                    self.apply_highlight(y, x)
                    self.selected_piece = clicked_square  # Store the selected piece position
                    self.selected_piece_label = self.labels[clicked_square]  # Store the label for the selected piece
                    print(f"Piece selected at: {self.selected_piece}")
            else:
                # Second click: Check if clicked on the same square
                if self.selected_piece == clicked_square:
                    self.reset_highlight(*self.selected_piece)
                    self.selected_piece = None 
                    # The same square was clicked; don't reset the highlight, just ignore
                    print(f"Same piece selected at: {self.selected_piece}. No action taken.")
                else:
                    # Second click: moving the piece to the target square
                    print(f"Move to: {clicked_square}")

                    # Move the piece and update the board
                    self.make_move(self.selected_piece, clicked_square)

                    # Reset the highlight after the move
                    self.reset_highlight(*self.selected_piece)
                    self.selected_piece = None  # Reset after move
                    self.selected_piece_label = None  # Clear the selected label


    def make_move(self, start_square, end_square):
        """Handle the movement of the piece on the board."""
        start_row, start_col = start_square
        end_row, end_col = end_square

        # Convert (row, col) into 1D index for your Chessboard class
        start_index = start_row * 8 + start_col
        end_index = end_row * 8 + end_col

        # Call the Chessboard class to make the move
        self.chessboard.make_move(start_index, end_index)

        # After the move is made, update the GUI
        self.load_fen(self.chessboard.to_fen())

    def apply_highlight(self, row, col):
        """Apply a highlight effect directly to the piece."""
        pixmap = QPixmap(f'src/gui/chess_pieces/{self.positions[(row, col)]}')
        highlighted_pixmap = QPixmap(pixmap.size())
        highlighted_pixmap.fill(Qt.transparent)

        painter = QPainter(highlighted_pixmap)
        painter.drawPixmap(0, 0, pixmap)
        painter.setCompositionMode(QPainter.CompositionMode_SourceAtop)
        painter.setBrush(QBrush(QColor(255, 255, 0, 127)))  # Semi-transparent yellow highlight
        painter.setPen(QPen(Qt.NoPen))
        painter.drawRect(highlighted_pixmap.rect())
        painter.end()

        self.labels[(row, col)].setPixmap(highlighted_pixmap)

    def reset_highlight(self, row, col):
        """Resets the highlight of a piece by reloading and redrawing the original image."""
        if (row, col) in self.positions:  # Check if there is a piece at this location
            pixmap = QPixmap(f'src/gui/chess_pieces/{self.positions[(row, col)]}')
            new_size = min(self.grid_layout_widget.width(), self.grid_layout_widget.height() - 40) // 8
            self.labels[(row, col)].setPixmap(pixmap.scaled(new_size, new_size, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            # If no piece is there, clear the label
            self.labels[(row, col)].clear()

    def load_fen(self, fen):
        """Load the board pieces from a FEN string and update the GUI."""
        # Split the FEN string into its components
        fen_rows = fen.split(" ")[0].split("/")  # Extract only the piece placement part of FEN
        
        # Clear existing pieces
        self.positions = {}

        # Iterate over each rank in the FEN string
        for row, fen_row in enumerate(fen_rows):
            col = 0  # Reset column for each row
            for char in fen_row:
                if char.isdigit():
                    # Empty squares (represented by numbers)
                    col += int(char)
                else:
                    # Place piece on the board
                    self.positions[(row, col)] = self.fen_to_image[char]
                    col += 1  # Move to the next column

        # Refresh the board display
        self.update_board_display()


    def update_board_display(self):
        """Update the board display based on the self.positions dictionary."""
        new_size = min(self.grid_layout_widget.width(), self.grid_layout_widget.height() - 40) // 8  # Consistent piece size calculation

        for row in range(8):
            for col in range(8):
                label = self.labels[(row, col)]

                # Set the background color of the square
                if (row + col) % 2 == 0:
                    label.setStyleSheet(f"background-color: {self.light_color.name()};")
                else:
                    label.setStyleSheet(f"background-color: {self.dark_color.name()};")

                # Check if there is a piece at the current position
                if (row, col) in self.positions:
                    pixmap = QPixmap(f'src/gui/chess_pieces/{self.positions[(row, col)]}')
                    # Scale the pixmap to fit the current square size
                    label.setPixmap(pixmap.scaled(new_size, new_size, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                else:
                    label.clear()  # Clear the label if there's no piece

