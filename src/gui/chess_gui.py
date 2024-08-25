# gui/chess_gui.py

import sys
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QGridLayout, QVBoxLayout, QSizePolicy
from PyQt5.QtGui import QPixmap, QColor, QPainter, QBrush, QPen
from PyQt5.QtCore import Qt

class ChessGUI(QWidget):
    def __init__(self, return_to_menu_callback, parent=None):
        super().__init__(parent)
        self.return_to_menu_callback = return_to_menu_callback
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
        """Initializes the chessboard with alternating colors, pieces, and border labels."""
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

        # Dictionary to hold the initial positions with the corresponding image filenames
        self.positions = {
            (0, 0): 'Chess_rdt60.png', (0, 1): 'Chess_ndt60.png', (0, 2): 'Chess_bdt60.png',
            (0, 3): 'Chess_qdt60.png', (0, 4): 'Chess_kdt60.png', (0, 5): 'Chess_bdt60.png',
            (0, 6): 'Chess_ndt60.png', (0, 7): 'Chess_rdt60.png',
            (1, 0): 'Chess_pdt60.png', (1, 1): 'Chess_pdt60.png', (1, 2): 'Chess_pdt60.png',
            (1, 3): 'Chess_pdt60.png', (1, 4): 'Chess_pdt60.png', (1, 5): 'Chess_pdt60.png',
            (1, 6): 'Chess_pdt60.png', (1, 7): 'Chess_pdt60.png',
            (6, 0): 'Chess_plt60.png', (6, 1): 'Chess_plt60.png', (6, 2): 'Chess_plt60.png',
            (6, 3): 'Chess_plt60.png', (6, 4): 'Chess_plt60.png', (6, 5): 'Chess_plt60.png',
            (6, 6): 'Chess_plt60.png', (6, 7): 'Chess_plt60.png',
            (7, 0): 'Chess_rlt60.png', (7, 1): 'Chess_nlt60.png', (7, 2): 'Chess_blt60.png',
            (7, 3): 'Chess_qlt60.png', (7, 4): 'Chess_klt60.png', (7, 5): 'Chess_blt60.png',
            (7, 6): 'Chess_nlt60.png', (7, 7): 'Chess_rlt60.png'
        }

        # Add the chess pieces to the grid
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

                # Check if there is a piece at the current position
                if (row, col) in self.positions:
                    pixmap = QPixmap(f'src/gui/chess_pieces/{self.positions[(row, col)]}')
                    if pixmap.isNull():
                        print(f"Failed to load {self.positions[(row, col)]}")
                    label.setPixmap(pixmap)

                self.grid_layout.addWidget(label, row + 1, col + 1)
                self.labels[(row, col)] = label

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
        """Handle the mouse click event to highlight the clicked piece."""
        x_offset = 20  # Rank labels width
        y_offset = 20  # File labels height

        grid_widget_width = self.grid_layout_widget.width() - 2 * x_offset
        grid_widget_height = self.grid_layout_widget.height() - 2 * y_offset
        new_size = min(grid_widget_width, grid_widget_height) // 8

        x = (event.x() - self.grid_layout_widget.x() - x_offset) // new_size
        y = (event.y() - self.grid_layout_widget.y() - y_offset) // new_size

        # Check if the click is within the valid chessboard area
        if 0 <= x < 8 and 0 <= y < 8:
            if (y, x) in self.positions:
                if self.last_clicked == (y, x):
                    # If the same square is clicked again, remove the highlight and redraw the piece
                    self.reset_highlight(y, x)
                    self.last_clicked = None  # Reset the last clicked square
                else:
                    # Reset the last clicked square highlight
                    if self.last_clicked:
                        self.reset_highlight(*self.last_clicked)

                    # Highlight the current piece
                    self.apply_highlight(y, x)

                    # Store the current position as the last clicked
                    self.last_clicked = (y, x)

        print(f"Clicked on cell: ({y}, {x})")

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
        pixmap = QPixmap(f'src/gui/chess_pieces/{self.positions[(row, col)]}')
        new_size = min(self.grid_layout_widget.width(), self.grid_layout_widget.height() - 40) // 8
        self.labels[(row, col)].setPixmap(pixmap.scaled(new_size, new_size, Qt.KeepAspectRatio, Qt.SmoothTransformation))
