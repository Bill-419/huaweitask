from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton, QTableWidgetItem, QTableWidget
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt
from basic_function.utils_with_page3 import PageUtils  # 确保导入新的PageUtils
from window.excel_editor import ExcelEditor  # 确保导入 ExcelEditor
import logging  # 添加导入 logging

# 配置日志
logging.basicConfig(level=logging.DEBUG)

class AdminPage3(QMainWindow):
    def __init__(self, is_admin=True):
        super().__init__()
        self.is_admin = is_admin
        self.utils = PageUtils('page3')
        self.display_utils = PageUtils('page3_display')
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Page 3')
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # 从数据库加载数据
        table_data, colors, fonts, alignments, row_heights, col_widths = self.utils.load_data_from_db()

        # 创建表格编辑器
        self.excel_editor = ExcelEditor()
        view_button = QPushButton('进入展示栏')
        view_button.clicked.connect(self.open_display_view)
        layout.addWidget(view_button)

        layout.addWidget(self.excel_editor)

        # 加载数据到表格中
        try:
            self.utils.set_table_data(self.excel_editor.table, table_data, colors, fonts, alignments, row_heights, col_widths, True)
        except IndexError as e:
            logging.error(f"Error setting table data: {e}")

        save_button = QPushButton('保存')
        save_button.clicked.connect(self.save_to_db)
        layout.addWidget(save_button)

        add_row_button = QPushButton('增加行')
        add_row_button.clicked.connect(self.add_row)
        layout.addWidget(add_row_button)

        refresh_button = QPushButton('刷新')
        refresh_button.clicked.connect(self.refresh_page)
        layout.addWidget(refresh_button)

        add_to_display_button = QPushButton('添加到展示栏')
        add_to_display_button.clicked.connect(self.add_selected_to_display)
        layout.addWidget(add_to_display_button)

    def add_row(self):
        row_position = self.excel_editor.table.rowCount()
        self.excel_editor.table.insertRow(row_position)

    def add_selected_to_display(self):
        selected_row = self.excel_editor.table.currentRow()
        if selected_row != -1:
            row_data = []
            for col in range(self.excel_editor.table.columnCount()):
                item = self.excel_editor.table.item(selected_row, col)
                row_data.append(item.text() if item else '')

            logging.debug(f"Selected row data to add to display: {row_data}")

            # Load current display table data
            display_data, display_colors, display_fonts, display_alignments, display_row_heights, display_col_widths = self.display_utils.load_data_from_db()

            logging.debug(f"Current display data before adding new row: {display_data}")

            # Add selected row data to display table data
            display_data.append(row_data)

            # Save updated display table data
            temp_table = QTableWidget()
            temp_table.setRowCount(len(display_data))
            temp_table.setColumnCount(self.excel_editor.table.columnCount())
            self.display_utils.set_table_data(temp_table, display_data, display_colors, display_fonts, display_alignments, display_row_heights, display_col_widths, True)
            self.display_utils.save_to_db(temp_table, True)

            logging.debug("Display data saved successfully.")
            self.refresh_page()

    def save_to_db(self):
        self.utils.save_to_db(self.excel_editor.table, True)
        logging.debug("Table data saved successfully.")

    def refresh_page(self):
        self.excel_editor.table.clear()  # 清除表格内容
        self.excel_editor.table.setRowCount(0)  # 重设行数
        self.excel_editor.table.setColumnCount(0)  # 重设列数
        table_data, colors, fonts, alignments, row_heights, col_widths = self.utils.load_data_from_db()
        try:
            self.utils.set_table_data(self.excel_editor.table, table_data, colors, fonts, alignments, row_heights, col_widths, True)
        except IndexError as e:
            logging.error(f"Error setting table data: {e}")

    def open_display_view(self):
        self.display_page = AdminDisplayPage()
        self.display_page.show()

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

        # 创建表格编辑器
        self.excel_editor = ExcelEditor()
        layout.addWidget(self.excel_editor)

        # 从数据库加载数据
        self.load_display_data()

        save_button = QPushButton('保存')
        save_button.clicked.connect(self.save_to_db)
        layout.addWidget(save_button)

        refresh_button = QPushButton('刷新')
        refresh_button.clicked.connect(self.load_display_data)
        layout.addWidget(refresh_button)

    def load_display_data(self):
        self.excel_editor.table.clear()  # 清除表格内容
        self.excel_editor.table.setRowCount(0)  # 重设行数
        self.excel_editor.table.setColumnCount(0)  # 重设列数
        table_data, colors, fonts, alignments, row_heights, col_widths = self.utils.load_data_from_db()
        try:
            self.utils.set_table_data(self.excel_editor.table, table_data, colors, fonts, alignments, row_heights, col_widths, True)
        except IndexError as e:
            logging.error(f"Error setting table data: {e}")

    def save_to_db(self):
        self.utils.save_to_db(self.excel_editor.table, True)
        logging.debug("Display table data saved successfully.")
