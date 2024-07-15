from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt
from basic_function.menu_operations import MenuOperations

class ExcelEditor(QWidget):
    def __init__(self, parent=None, data=None, columns=11, headers=None, enable_context_menu=True, locked_rows=None):
        super().__init__(parent)
        self.data = data if data else []  # 初始化数据
        self.columns = columns  # 初始化列数
        self.headers = headers if headers else []  # 初始化表头
        self.enable_context_menu = enable_context_menu  # 是否启用右键菜单
        self.locked_rows = locked_rows if locked_rows else []  # 初始化锁定行
        self.init_ui()  # 初始化用户界面

    def init_ui(self):
        layout = QVBoxLayout()
        self.table = QTableWidget(10, self.columns)  # 设置表格列数
        layout.addWidget(self.table)
        self.setLayout(layout)

        # 初始化每个单元格的背景颜色为白色
        self.initialize_table_background()

        # 设置表头
        self.table.setHorizontalHeaderLabels(self.headers)

        if self.enable_context_menu:
            # 初始化 MenuOperations 仅当允许右键菜单时
            self.menu_operations = MenuOperations(self.table)
        else:
            # 禁用右键菜单
            self.table.setContextMenuPolicy(Qt.NoContextMenu)

        # 如果有数据则填充表格
        if self.data:
            self.load_data(self.data)

    def initialize_table_background(self):
        for row in range(self.table.rowCount()):
            for column in range(self.table.columnCount()):
                item = self.table.item(row, column)
                if item is None:
                    item = QTableWidgetItem()
                    self.table.setItem(row, column, item)
                item.setBackground(QColor('white'))  # 默认白色背景

    def load_data(self, data):
        self.table.setRowCount(len(data))  # 设置行数
        for row in range(len(data)):
            for column in range(len(data[row])):
                item = self.table.item(row, column)
                if not item:
                    item = QTableWidgetItem()
                    self.table.setItem(row, column, item)
                item.setText(data[row][column])
                # 如果该行被锁定，则设置单元格为只读，并禁用右键菜单
                if row in self.locked_rows:
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                    self.table.setContextMenuPolicy(Qt.NoContextMenu)

    def get_data(self):
        data = []
        for row in range(self.table.rowCount()):
            row_data = []
            for column in range(self.table.columnCount()):
                item = self.table.item(row, column)
                row_data.append(item.text() if item else '')
            data.append(row_data)
        return data

class ReadOnlyExcelEditor(ExcelEditor):
    def __init__(self, parent=None, data=None, columns=11, headers=None):
        super().__init__(parent, data, columns, headers, enable_context_menu=False)  # 禁用右键菜单
        self.set_table_read_only()

    def set_table_read_only(self):
        for row in range(self.table.rowCount()):
            for column in range(self.table.columnCount()):
                item = self.table.item(row, column)
                if item:
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)  # 禁止编辑
