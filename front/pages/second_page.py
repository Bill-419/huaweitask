import pandas as pd
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton, QTableWidget, QToolButton, QMenu, QTableWidgetItem
from PySide6.QtGui import QAction, QColor, QFont
from basic_function.utils import PageUtils
from basic_function.filter_operations import FilterDialog, apply_filters, table_to_dataframe, load_dataframe_to_table, table_styles_to_dict
from window.excel_editor import ExcelEditor, ReadOnlyExcelEditor
from PySide6.QtCore import Qt
from functools import partial

class SecondPage(QMainWindow):
    def __init__(self, is_admin=True):
        super().__init__()
        self.is_admin = is_admin  # 确定用户是否为管理员
        self.utils = PageUtils('second_page')  # 创建 PageUtils 实例，用于处理与第二页相关的数据库操作
        self.initial_df = None  # 保存初始加载的 DataFrame
        self.filter_conditions = {}  # 保存筛选条件
        self.sort_conditions = {}  # 保存排序条件
        self.styles = {}  # 保存样式信息
        self.init_ui()  # 初始化用户界面

    def init_ui(self):
        self.setWindowTitle('第二页')  # 设置窗口标题
        self.setGeometry(100, 100, 800, 600)  # 设置窗口位置和大小

        central_widget = QWidget()
        self.setCentralWidget(central_widget)  # 创建中央组件并设置为中央部件

        layout = QVBoxLayout()
        central_widget.setLayout(layout)  # 创建垂直布局并设置为中央组件的布局

        # 从数据库加载数据
        table_data, colors, fonts, alignments, row_heights, col_widths = self.utils.load_data_from_db()
        self.styles = {'colors': colors, 'fonts': fonts, 'alignments': alignments}  # 保存样式信息

        # 更新列数和表头
        self.columns = len(table_data[0])  # 确定表格的列数
        headers = [str(i+1) for i in range(self.columns)]  # 生成表头

        # 创建ExcelEditor或ReadOnlyExcelEditor
        if self.is_admin:
            self.excel_editor = ExcelEditor(columns=self.columns, headers=headers)  # 创建可编辑的 Excel 编辑器
            view_button = QPushButton('进入用户页面查看')
            view_button.clicked.connect(self.open_readonly_view)  # 连接按钮点击事件
            layout.addWidget(view_button)  # 添加按钮到布局中
        else:
            self.excel_editor = ReadOnlyExcelEditor(columns=self.columns, headers=headers)  # 创建只读的 Excel 编辑器
        layout.addWidget(self.excel_editor)  # 将编辑器添加到布局中

        # 加载数据到表格中
        self.utils.set_table_data(self.excel_editor.table, table_data, self.styles['colors'], self.styles['fonts'], self.styles['alignments'], row_heights, col_widths, self.is_admin)

        # 将表格数据转换为 DataFrame 并保存
        self.initial_df = table_to_dataframe(self.excel_editor.table, headers, self.is_admin)  # 转换为 DataFrame 并保存
        self.styles = table_styles_to_dict(self.excel_editor.table, 1 if not self.is_admin else 0)  # 保存样式信息

        # 如果是用户模式，添加筛选行
        if not self.is_admin:
            self.add_filter_row()

        # 添加保存按钮
        if self.is_admin:
            save_button = QPushButton('保存')
            save_button.clicked.connect(self.save_to_db)  # 连接按钮点击事件
            layout.addWidget(save_button)  # 添加按钮到布局中

        # 添加刷新按钮
        self.refresh_button = QPushButton('刷新')
        self.refresh_button.clicked.connect(self.refresh_page)  # 连接按钮点击事件
        layout.addWidget(self.refresh_button)  # 添加按钮到布局中

    def add_filter_row(self):
        self.excel_editor.table.insertRow(0)  # 在表格顶部插入一行
        for col in range(self.excel_editor.table.columnCount()):
            header_item = self.excel_editor.table.item(0, col)
            if header_item:
                self.excel_editor.table.setHorizontalHeaderItem(col, QTableWidgetItem(header_item.text()))  # 设置表头项目
            button = QToolButton(self)
            button.setText("▼")  # 使用 Unicode 字符作为下拉箭头
            button.setStyleSheet("""
                QToolButton {
                    border: 1px solid #d4d4d4;
                    background-color: #f0f0f0;
                    padding: 5px;
                    font-size: 12px;
                }
                QToolButton:hover {
                    background-color: #e6e6e6;
                }
                QToolButton:pressed {
                    background-color: #cccccc;
                }
            """)  # 设置按钮样式
            button.setPopupMode(QToolButton.InstantPopup)  # 设置弹出模式
            menu = QMenu(self)
            filter_action = QAction("筛选", self)
            sort_asc_action = QAction("升序", self)
            sort_desc_action = QAction("降序", self)
            menu.addAction(filter_action)
            menu.addAction(sort_asc_action)
            menu.addAction(sort_desc_action)  # 添加菜单项
            button.setMenu(menu)  # 设置按钮菜单
            filter_action.triggered.connect(partial(self.show_filter_dialog, col))  # 连接筛选操作
            sort_asc_action.triggered.connect(partial(self.sort_column, col, True))  # 连接升序操作
            sort_desc_action.triggered.connect(partial(self.sort_column, col, False))  # 连接降序操作
            self.excel_editor.table.setCellWidget(0, col, button)  # 将按钮设置为单元格小部件

    def show_filter_dialog(self, col):
        data = self.initial_df.iloc[:, col].tolist()  # 获取列数据
        selected_items = self.filter_conditions.get(col, [])  # 获取当前筛选条件
        dialog = FilterDialog(col, data, selected_items, self)
        if dialog.exec():
            selected_items = dialog.get_selected_items()  # 获取选择的筛选项目
            self.filter_conditions[col] = selected_items  # 更新筛选条件
            self.apply_filters()

    def sort_column(self, col, ascending):
        self.sort_conditions[col] = ascending  # 更新排序条件
        self.apply_filters()

    def apply_filters(self):
        filtered_df = apply_filters(self.initial_df, self.filter_conditions, self.sort_conditions)  # 应用筛选和排序
        load_dataframe_to_table(filtered_df, self.excel_editor.table, [str(i+1) for i in range(self.columns)], self.is_admin, self.styles)  # 将 DataFrame 加载到表格中

    def save_to_db(self):
        self.utils.save_to_db(self.excel_editor.table, self.is_admin)  # 保存数据到数据库

    def refresh_page(self):
        table_data, colors, fonts, alignments, row_heights, col_widths = self.utils.load_data_from_db()
        self.utils.set_table_data(self.excel_editor.table, table_data, colors, fonts, alignments, row_heights, col_widths, self.is_admin)  # 从数据库加载数据并更新表格
        self.initial_df = table_to_dataframe(self.excel_editor.table, [str(i+1) for i in range(self.columns)], self.is_admin)  # 更新初始 DataFrame
        self.filter_conditions.clear()  # 清空筛选条件
        self.styles = table_styles_to_dict(self.excel_editor.table, 1 if not self.is_admin else 0)  # 更新样式信息

    def open_readonly_view(self):
        self.readonly_page = ReadOnlySecondPage()  # 创建只读页面实例
        self.readonly_page.show()  # 显示只读页面

class ReadOnlySecondPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.utils = PageUtils('second_page')  # 创建 PageUtils 实例，用于处理与第二页相关的数据库操作
        self.initial_df = None  # 保存初始加载的 DataFrame
        self.filter_conditions = {}  # 保存筛选条件
        self.sort_conditions = {}  # 保存排序条件
        self.styles = {}  # 保存样式信息
        self.init_ui()  # 初始化用户界面

    def init_ui(self):
        self.setWindowTitle('第二页（只读）')  # 设置窗口标题
        self.setGeometry(100, 100, 800, 600)  # 设置窗口位置和大小

        central_widget = QWidget()
        self.setCentralWidget(central_widget)  # 创建中央组件并设置为中央部件

        layout = QVBoxLayout()
        central_widget.setLayout(layout)  # 创建垂直布局并设置为中央组件的布局

        # 从数据库加载数据
        table_data, colors, fonts, alignments, row_heights, col_widths = self.utils.load_data_from_db()
        self.styles = {'colors': colors, 'fonts': fonts, 'alignments': alignments}  # 保存样式信息

        # 更新列数和表头
        self.columns = len(table_data[0])  # 确定表格的列数
        headers = [str(i+1) for i in range(self.columns)]  # 生成表头

        # 创建ReadOnlyExcelEditor
        self.excel_editor = ReadOnlyExcelEditor(columns=self.columns, headers=headers)  # 创建只读的 Excel 编辑器
        layout.addWidget(self.excel_editor)  # 将编辑器添加到布局中

        # 加载数据到表格中
        self.utils.set_table_data(self.excel_editor.table, table_data, self.styles['colors'], self.styles['fonts'], self.styles['alignments'], row_heights, col_widths, False)

        # 将表格数据转换为 DataFrame 并保存
        self.initial_df = table_to_dataframe(self.excel_editor.table, headers, False)  # 转换为 DataFrame 并保存
        self.styles = table_styles_to_dict(self.excel_editor.table, 1)  # 保存样式信息

        self.add_filter_row()  # 添加筛选行

        # 添加刷新按钮
        refresh_button = QPushButton('刷新')
        refresh_button.clicked.connect(self.refresh_page)  # 连接按钮点击事件
        layout.addWidget(refresh_button)  # 添加按钮到布局中

        self.refresh_page()  # 处理完数据后调用刷新方法

    def add_filter_row(self):
        for col in range(self.excel_editor.table.columnCount()):
            header_item = self.excel_editor.table.item(0, col)
            if header_item:
                self.excel_editor.table.setHorizontalHeaderItem(col, QTableWidgetItem(header_item.text()))  # 设置表头项目
            button = QToolButton(self)
            button.setText("▼")  # 使用 Unicode 字符作为下拉箭头
            button.setStyleSheet("""
                QToolButton {
                    border: 1px solid #d4d4d4;
                    background-color: #f0f0f0;
                    padding: 5px;
                    font-size: 12px;
                }
                QToolButton:hover {
                    background-color: #e6e6e6;
                }
                QToolButton:pressed {
                    background-color: #cccccc;
                }
            """)  # 设置按钮样式
            button.setPopupMode(QToolButton.InstantPopup)  # 设置弹出模式
            menu = QMenu(self)
            filter_action = QAction("筛选", self)
            sort_asc_action = QAction("升序", self)
            sort_desc_action = QAction("降序", self)
            menu.addAction(filter_action)
            menu.addAction(sort_asc_action)
            menu.addAction(sort_desc_action)  # 添加菜单项
            button.setMenu(menu)  # 设置按钮菜单
            filter_action.triggered.connect(partial(self.show_filter_dialog, col))  # 连接筛选操作
            sort_asc_action.triggered.connect(partial(self.sort_column, col, True))  # 连接升序操作
            sort_desc_action.triggered.connect(partial(self.sort_column, col, False))  # 连接降序操作
            self.excel_editor.table.setCellWidget(0, col, button)  # 将按钮设置为单元格小部件

    def show_filter_dialog(self, col):
        data = self.initial_df.iloc[:, col].tolist()  # 获取列数据
        selected_items = self.filter_conditions.get(col, [])  # 获取当前筛选条件
        dialog = FilterDialog(col, data, selected_items, self)
        if dialog.exec():
            selected_items = dialog.get_selected_items()  # 获取选择的筛选项目
            self.filter_conditions[col] = selected_items  # 更新筛选条件
            self.apply_filters()

    def sort_column(self, col, ascending):
        self.sort_conditions[col] = ascending  # 更新排序条件
        self.apply_filters()

    def apply_filters(self):
        filtered_df = apply_filters(self.initial_df, self.filter_conditions, self.sort_conditions)  # 应用筛选和排序
        load_dataframe_to_table(filtered_df, self.excel_editor.table, [str(i+1) for i in range(self.columns)], False, self.styles)  # 将 DataFrame 加载到表格中

    def refresh_page(self):
        table_data, colors, fonts, alignments, row_heights, col_widths = self.utils.load_data_from_db()
        self.utils.set_table_data(self.excel_editor.table, table_data, colors, fonts, alignments, row_heights, col_widths, False)  # 从数据库加载数据并更新表格
        self.initial_df = table_to_dataframe(self.excel_editor.table, [str(i+1) for i in range(self.columns)], False)  # 更新初始 DataFrame
        self.filter_conditions.clear()  # 清空筛选条件
        self.styles = table_styles_to_dict(self.excel_editor.table, 1)  # 更新样式信息
