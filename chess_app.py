import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QStackedWidget
from src.gui.chess_gui import ChessGUI
from src.gui.main_menu import MainMenu
from src.gui.game_selector import GameSelector
from PyQt5.QtGui import QIcon

class ChessApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Chess')
        self.setWindowIcon(QIcon('src/gui/icons/icon.png'))
        self.setGeometry(300, 100, 800, 800)
        self.setStyleSheet("QMainWindow {background-image: url('src/gui/background/background.png'); background-position: center; background-repeat: no-repeat;}")

        # Central widget to hold multiple screens
        self.central_widget = QStackedWidget(self)
        self.setCentralWidget(self.central_widget)

        # Initialize Main Menu
        self.main_menu = MainMenu(self.go_to_game_selector)
        self.central_widget.addWidget(self.main_menu)

        # Initialize Side Selection Page with callbacks for choosing a side and returning to the menu
        self.game_selector = GameSelector(self.start_game, self.show_main_menu)
        self.central_widget.addWidget(self.game_selector)

        # Placeholder for Chess GUI
        self.chess_gui = None

    def go_to_game_selector(self):
        """Switch to the side selection screen."""
        self.central_widget.setCurrentWidget(self.game_selector)

    def start_game(self, side):
        if self.chess_gui is None:
            # Create the Chess GUI and add a callback to return to the main menu
            self.chess_gui = ChessGUI(self.show_main_menu, player_side=side)
            self.central_widget.addWidget(self.chess_gui)

        # Pass the selected side (white or black) to the chess GUI
        self.chess_gui.chessboard.to_move = side

        # Switch to the Chess GUI screen
        self.central_widget.setCurrentWidget(self.chess_gui)
        self.setStyleSheet("background: none;")

    def show_main_menu(self):
        self.chess_gui = None
        # Switch back to the main menu screen
        self.central_widget.setCurrentWidget(self.main_menu)
        self.setStyleSheet("QMainWindow {background-image: url('src/gui/background/background.png'); background-position: center; background-repeat: no-repeat;}")

def main():
    app = QApplication(sys.argv)
    main_window = ChessApp()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
