from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QPushButton, QMessageBox, QWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

class UserWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('User Page')
        self.setGeometry(100, 100, 800, 600)  # 调整窗口大小

        main_layout = QVBoxLayout()
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        welcome_label = QLabel('Welcome, User!')
        welcome_label.setAlignment(Qt.AlignCenter)
        font = QFont()
        font.setPointSize(14)  # 设置字体大小
        welcome_label.setFont(font)
        main_layout.addWidget(welcome_label)

        # 添加其他用户界面的控件
        button = QPushButton('User Button')
        button.clicked.connect(self.user_button_clicked)
        main_layout.addWidget(button)

    def user_button_clicked(self):
        QMessageBox.information(self, 'Info', 'User Button Clicked')
