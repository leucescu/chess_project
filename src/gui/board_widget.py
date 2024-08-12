import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QVBoxLayout, QSizePolicy
from PyQt5.QtGui import QPixmap, QColor, QPainter, QBrush, QPen
from PyQt5.QtCore import Qt

class ChessGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Chess GUI')

        # Set the size of the ChessGUI window
        self.setGeometry(100, 100, 640, 640)  # Initial size

        # Create a main layout
        main_layout = QVBoxLayout(self)
        self.setLayout(main_layout)

        # Create a widget to hold the chessboard (grid layout)
        self.board_widget = QWidget(self)
        self.board_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Explicitly set the size of the chessboard
        self.board_widget.setMinimumSize(400, 400)  # Minimum size
        self.board_widget.setMaximumSize(800, 800)  # Maximum size

        # Create the grid layout
        self.grid = QGridLayout(self.board_widget)
        self.board_widget.setLayout(self.grid)
        main_layout.addWidget(self.board_widget)

        # Define the colors for the chessboard
        self.light_color = QColor(106, 30, 29)  # Light square color
        self.dark_color = QColor(188, 120, 121) # Dark square color

        self.last_clicked = None  # To store the last clicked square

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

        # Initialize the chessboard with pieces
        self.initialize_board()

    def initialize_board(self):
        """Initializes the chessboard with alternating colors and pieces."""
        self.labels = {}  # Dictionary to store the labels for each square
        for row in range(8):
            for col in range(8):
                label = QLabel(self.board_widget)
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

                self.grid.addWidget(label, row, col)
                self.labels[(row, col)] = label

    def resizeEvent(self, event):
        """Handle the window resize event to dynamically adjust the size of the chessboard and pieces."""
        # Calculate the new size for each square based on the smallest dimension
        new_size = min(self.board_widget.width(), self.board_widget.height()) // 8

        for row in range(8):
            for col in range(8):
                item = self.grid.itemAtPosition(row, col)
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
        x = event.x() // (self.board_widget.width() // 8)  # Calculate grid position based on current cell size
        y = event.y() // (self.board_widget.height() // 8)

        # Check if the clicked square contains a piece
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
        new_size = min(self.board_widget.width(), self.board_widget.height()) // 8
        self.labels[(row, col)].setPixmap(pixmap.scaled(new_size, new_size, Qt.KeepAspectRatio, Qt.SmoothTransformation))

def main():
    app = QApplication(sys.argv)
    ex = ChessGUI()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
