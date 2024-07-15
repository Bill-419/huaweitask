from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton
from basic_function.utils import PageUtils
from window.excel_editor import ExcelEditor, ReadOnlyExcelEditor

class KPIProcessPlan(QMainWindow):
    def __init__(self, is_admin=True):
        super().__init__()
        self.is_admin = is_admin  # 设置是否为管理员
        self.utils = PageUtils('kpi_process_plan')  # 创建 PageUtils 实例
        self.init_ui()  # 初始化用户界面

    def init_ui(self):
        self.setWindowTitle('KPI Process Plan')  # 设置窗口标题
        self.setGeometry(100, 100, 800, 600)  # 设置窗口位置和大小

        central_widget = QWidget()  # 创建中央组件
        self.setCentralWidget(central_widget)  # 设置中央组件

        layout = QVBoxLayout()  # 创建垂直布局
        central_widget.setLayout(layout)  # 设置布局

        # 从数据库加载数据
        table_data, colors, fonts, alignments, row_heights, col_widths = self.utils.load_data_from_db()

        # 根据是否为管理员创建相应的编辑器
        if self.is_admin:
            self.excel_editor = ExcelEditor()
        else:
            self.excel_editor = ReadOnlyExcelEditor()
        layout.addWidget(self.excel_editor)  # 将编辑器添加到布局中

        # 加载数据到表格中
        self.utils.set_table_data(self.excel_editor.table, table_data, colors, fonts, alignments, row_heights, col_widths, self.is_admin)

        # 如果是管理员，则添加保存按钮
        if self.is_admin:
            save_button = QPushButton('保存')
            save_button.clicked.connect(self.save_to_db)
            layout.addWidget(save_button)

        # 添加刷新按钮
        refresh_button = QPushButton('刷新')
        refresh_button.clicked.connect(self.refresh_page)
        layout.addWidget(refresh_button)

    def save_to_db(self):
        # 保存数据到数据库
        self.utils.save_to_db(self.excel_editor.table, self.is_admin)

    def refresh_page(self):
        # 从数据库重新加载数据并更新表格
        table_data, colors, fonts, alignments, row_heights, col_widths = self.utils.load_data_from_db()
        self.utils.set_table_data(self.excel_editor.table, table_data, colors, fonts, alignments, row_heights, col_widths, self.is_admin)

class ReadOnlyKPIProcessPlan(QMainWindow):
    def __init__(self):
        super().__init__()
        self.utils = PageUtils('kpi_process_plan')  # 创建 PageUtils 实例
        self.init_ui()  # 初始化用户界面

    def init_ui(self):
        self.setWindowTitle('KPI Process Plan')  # 设置窗口标题
        self.setGeometry(100, 100, 800, 600)  # 设置窗口位置和大小

        central_widget = QWidget()  # 创建中央组件
        self.setCentralWidget(central_widget)  # 设置中央组件

        layout = QVBoxLayout()  # 创建垂直布局
        central_widget.setLayout(layout)  # 设置布局

        # 从数据库加载数据
        table_data, colors, fonts, alignments, row_heights, col_widths = self.utils.load_data_from_db()

        # 创建只读的 Excel 编辑器
        self.excel_editor = ReadOnlyExcelEditor()
        layout.addWidget(self.excel_editor)  # 将编辑器添加到布局中

        # 加载数据到表格中
        self.utils.set_table_data(self.excel_editor.table, table_data, colors, fonts, alignments, row_heights, col_widths, False)

        # 添加刷新按钮
        refresh_button = QPushButton('刷新')
        refresh_button.clicked.connect(self.refresh_page)
        layout.addWidget(refresh_button)

    def refresh_page(self):
        # 从数据库重新加载数据并更新表格
        table_data, colors, fonts, alignments, row_heights, col_widths = self.utils.load_data_from_db()
        self.utils.set_table_data(self.excel_editor.table, table_data, colors, fonts, alignments, row_heights, col_widths, False)
