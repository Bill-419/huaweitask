from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QPushButton, QWidget, QFrame, QHBoxLayout, QTextEdit
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from pages.kpi_rules import KPI_RULES_TEXT
from pages.kpi_process_plan import KPIProcessPlan, ReadOnlyKPIProcessPlan
from pages.second_page import SecondPage, ReadOnlySecondPage
from pages.page3_admin import AdminPage3  # 添加此行
from pages.page3_user import ReadOnlyPage3  # 添加此行
from functools import partial

class MainWindow(QMainWindow):
    def __init__(self, is_admin=False):
        super().__init__()
        self.is_admin = is_admin
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Main Page')
        self.setGeometry(100, 100, 800, 600)

        main_layout = QVBoxLayout()
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        self.kpi_frame = QFrame()
        self.kpi_frame.setFrameShape(QFrame.Box)
        self.kpi_frame.setFrameShadow(QFrame.Sunken)
        frame_layout = QVBoxLayout()
        frame_layout.setContentsMargins(10, 10, 10, 10)
        frame_layout.setSpacing(10)
        self.kpi_frame.setLayout(frame_layout)

        self.kpi_label = QLabel('KPI Rules')
        self.kpi_label.setAlignment(Qt.AlignCenter)
        font = QFont()
        font.setPointSize(14)
        self.kpi_label.setFont(font)
        frame_layout.addWidget(self.kpi_label)

        self.kpi_text = QLabel(KPI_RULES_TEXT)
        self.kpi_text.setWordWrap(True)
        font.setPointSize(12)
        self.kpi_text.setFont(font)
        frame_layout.addWidget(self.kpi_text)

        main_layout.addWidget(self.kpi_frame)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)
        for i in range(1, 6):
            button = QPushButton(f'Page {i}')
            font.setPointSize(12)
            button.setFont(font)
            button.setFixedSize(100, 40)
            button.clicked.connect(partial(self.show_page, i))
            button_layout.addWidget(button)
        main_layout.addLayout(button_layout)

    def show_page(self, page_number):
        if page_number == 1:
            if self.is_admin:
                self.page = KPIProcessPlan()
            else:
                self.page = ReadOnlyKPIProcessPlan()
        elif page_number == 2:
            if self.is_admin:
                self.page = SecondPage()
            else:
                self.page = ReadOnlySecondPage()
        elif page_number == 3:
                self.page = AdminPage3(is_admin=self.is_admin) 
        else:
            read_only = not self.is_admin and page_number > 2
            self.page = self.create_text_page(page_number, read_only)

        self.page.show()

    @staticmethod
    def create_text_page(page_number, read_only):
        page = QMainWindow()
        page.setWindowTitle(f"页面 {page_number}")
        page.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        page.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        content_text = QTextEdit()
        content_text.setPlaceholderText(f"这是页面 {page_number} 的内容")
        content_text.setReadOnly(read_only)

        layout.addWidget(content_text)

        return page
