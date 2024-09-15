from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize

class GameSelector(QWidget):
    def __init__(self, choose_side_callback, return_to_menu_callback, parent=None):
        super().__init__(parent)
        self.choose_side_callback = choose_side_callback
        self.return_to_menu_callback = return_to_menu_callback
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Horizontal layout for the side selection buttons
        button_layout = QHBoxLayout()

        # Create buttons for selecting White or Black, and add icons
        white_button = QPushButton('Play as White')
        white_button.setIcon(QIcon('src/gui/chess_pieces/Chess_plt60.png'))  # Add white knight icon
        black_button = QPushButton('Play as Black')
        black_button.setIcon(QIcon('src/gui/chess_pieces/Chess_pdt60.png'))  # Add black knight icon

        white_button.setIconSize(QSize(128, 128))
        black_button.setIconSize(QSize(128, 128))

        # Connect buttons to the callback with the respective side
        white_button.clicked.connect(lambda: self.choose_side_callback('white'))
        black_button.clicked.connect(lambda: self.choose_side_callback('black'))

        # Add the buttons to the horizontal layout
        button_layout.addWidget(white_button)
        button_layout.addWidget(black_button)

        # Add the horizontal layout to the main layout
        layout.addLayout(button_layout)

        # Add a "Return to Main Menu" button
        return_button = QPushButton('Return to Main Menu')
        return_button.clicked.connect(self.return_to_menu_callback)
        layout.addWidget(return_button)

        # Set the main layout for the widget
        self.setLayout(layout)
