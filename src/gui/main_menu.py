from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QApplication

class MainMenu(QWidget):
    def __init__(self, start_game_callback, parent=None):
        super().__init__(parent)
        self.start_game_callback = start_game_callback
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Play button
        play_button = QPushButton('Play')
        play_button.clicked.connect(self.start_game_callback)
        layout.addWidget(play_button)

        # Settings button (you can implement this later)
        settings_button = QPushButton('Settings')
        layout.addWidget(settings_button)

        # Exit button
        exit_button = QPushButton('Exit')
        exit_button.clicked.connect(QApplication.instance().quit)
        layout.addWidget(exit_button)

        self.setLayout(layout)

    def close_application(self):
        self.parentWidget().close()
