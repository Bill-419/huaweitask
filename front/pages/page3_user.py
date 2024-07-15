from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QTableWidget, QPushButton
from basic_function.utils_with_page3 import PageUtils
from window.excel_editor import ExcelEditor

class AdminDisplayPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.utils = PageUtils('page3_display')
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('管理员展示栏')
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # 从数据库加载数据
        self.load_display_data()

        save_button = QPushButton('保存')
        save_button.clicked.connect(self.save_to_db)
        layout.addWidget(save_button)

        refresh_button = QPushButton('刷新')
        refresh_button.clicked.connect(self.load_display_data)
        layout.addWidget(refresh_button)

    def load_display_data(self):
        table_data, colors, fonts, alignments, row_heights, col_widths = self.utils.load_data_from_db()
        self.excel_editor = ExcelEditor()  # 使用可编辑的 Excel 编辑器
        self.centralWidget().layout().addWidget(self.excel_editor)
        self.utils.set_table_data(self.excel_editor.table, table_data, colors, fonts, alignments, row_heights, col_widths, True)

    def save_to_db(self):
        self.utils.save_to_db(self.excel_editor.table, True)

class ReadOnlyPage3(QMainWindow):
    def __init__(self):
        super().__init__()
        self.utils = PageUtils('page3_display')
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('用户展示栏')
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # 从数据库加载数据
        table_data, colors, fonts, alignments, row_heights, col_widths = self.utils.load_data_from_db()

        # 创建只读的 Excel 编辑器
        self.excel_editor = ReadOnlyExcelEditor()
        layout.addWidget(self.excel_editor)

        refresh_button = QPushButton('刷新')
        refresh_button.clicked.connect(self.refresh_page)
        layout.addWidget(refresh_button)

        # 加载数据到表格中
        self.utils.set_table_data(self.excel_editor.table, table_data, colors, fonts, alignments, row_heights, col_widths, False)

    def refresh_page(self):
        table_data, colors, fonts, alignments, row_heights, col_widths = self.utils.load_data_from_db()
        self.utils.set_table_data(self.excel_editor.table, table_data, colors, fonts, alignments, row_heights, col_widths, False)
