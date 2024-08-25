import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QStackedWidget
from src.gui.chess_gui import ChessGUI
from src.gui.main_menu import MainMenu

class ChessApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Chess GUI Application')
        self.setGeometry(300, 100, 800, 800)

        # Central widget to hold multiple screens
        self.central_widget = QStackedWidget(self)
        self.setCentralWidget(self.central_widget)

        # Initialize Main Menu
        self.main_menu = MainMenu(self.start_game)
        self.central_widget.addWidget(self.main_menu)

        # Placeholder for Chess GUI
        self.chess_gui = None

    def start_game(self):
        if self.chess_gui is None:
            # Create the Chess GUI and add a callback to return to the main menu
            self.chess_gui = ChessGUI(self.show_main_menu)
            self.central_widget.addWidget(self.chess_gui)
        
        # Switch to the Chess GUI screen
        self.central_widget.setCurrentWidget(self.chess_gui)

    def show_main_menu(self):
        # Switch back to the main menu screen
        self.central_widget.setCurrentWidget(self.main_menu)

def main():
    app = QApplication(sys.argv)
    main_window = ChessApp()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
