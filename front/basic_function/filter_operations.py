import pandas as pd  # 引入pandas库处理数据框
from PySide6.QtWidgets import QCheckBox, QDialog, QVBoxLayout, QDialogButtonBox, QTableWidgetItem  # 引入PySide6相关组件
from PySide6.QtGui import QColor, QFont  # 引入颜色和字体相关的类

# 定义筛选对话框类，用于创建和管理筛选对话框
class FilterDialog(QDialog):
    def __init__(self, column, data, selected_items, parent=None):
        super().__init__(parent)  # 初始化父类
        self.column = column  # 要筛选的列编号
        self.data = data  # 数据列表
        self.selected_items = selected_items  # 已选择的筛选项
        self.init_ui()  # 初始化用户界面

    def init_ui(self):
        self.setWindowTitle(f"筛选 列 {self.column + 1}")  # 设置窗口标题
        layout = QVBoxLayout()  # 使用垂直布局
        self.checkboxes = []  # 复选框列表

        # 生成数据中的唯一项，过滤空白选项，并排序
        unique_items = list(set(self.data))
        unique_items = [item for item in unique_items if item]
        unique_items.sort()

        # 为每个唯一项创建一个复选框，并设置是否选中
        for item in unique_items:
            checkbox = QCheckBox(item)
            checkbox.setChecked(item in self.selected_items)
            layout.addWidget(checkbox)
            self.checkboxes.append(checkbox)

        # 添加确定和取消按钮
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)  # 连接确认按钮的信号
        button_box.rejected.connect(self.reject)  # 连接取消按钮的信号
        layout.addWidget(button_box)

        self.setLayout(layout)  # 设置布局

    def get_selected_items(self):
        # 返回选中的项
        return [checkbox.text() for checkbox in self.checkboxes if checkbox.isChecked()]

# 应用筛选条件并排序
def apply_filters(df, filter_conditions, sort_conditions):
    filtered_df = df.copy()  # 复制数据框以避免在原数据上进行修改
    # 根据筛选条件过滤数据
    for col, selected_items in filter_conditions.items():
        if selected_items:
            filtered_df = filtered_df[filtered_df.iloc[:, col].isin(selected_items)]
    # 根据排序条件排序数据
    for col, ascending in sort_conditions.items():
        filtered_df = filtered_df.sort_values(by=filtered_df.columns[col], ascending=ascending)
    return filtered_df

# 从表格转换数据到 DataFrame
def table_to_dataframe(table, headers, is_admin):
    data = []
    start_row = 1 if not is_admin else 0  # 管理员从第0行开始，非管理员从第1行开始
    # 遍历表格行
    for row in range(start_row, table.rowCount()):
        row_data = []
        # 遍历表格列，读取数据
        for column in range(table.columnCount()):
            item = table.item(row, column)
            row_data.append(item.text() if item else '')
        data.append(row_data)
    return pd.DataFrame(data, columns=headers)  # 返回DataFrame格式的数据

# 从表格中读取样式并保存到字典
def table_styles_to_dict(table, start_row):
    styles = {'colors': {}, 'fonts': {}, 'alignments': {}}
    for row in range(start_row, table.rowCount()):
        for col in range(table.columnCount()):
            item = table.item(row, col)
            if item:
                text = item.text()
                # 保存非白色背景的颜色
                if item.background().color().name() == '#000000':
                    styles['colors'][text] = '#ffffff'
                font = item.font()
                styles['fonts'][text] = {'bold': font.bold(), 'size': font.pointSize()}
                styles['alignments'][text] = item.textAlignment()
    return styles

# 将DataFrame加载回表格，应用样式
def load_dataframe_to_table(df, table, headers, is_admin, styles):
    table.setRowCount(len(df) + (1 if not is_admin else 0))
    start_row = 1 if not is_admin else 0
    for row in range(len(df)):
        for col in range(len(df.columns)):
            item = QTableWidgetItem(df.iloc[row, col])
            table.setItem(row + start_row, col, item)
            cell_text = df.iloc[row, col]
            # 应用保存的样式
            if cell_text in styles['colors']:
                item.setBackground(QColor(styles['colors'][cell_text]))
            else:
                item.setBackground(QColor('#ffffff'))
            if cell_text in styles['fonts']:
                font = QFont()
                font.setBold(styles['fonts'][cell_text]['bold'])
                font.setPointSize(styles['fonts'][cell_text]['size'])
                item.setFont(font)
            if cell_text in styles['alignments']:
                item.setTextAlignment(styles['alignments'][cell_text])
    table.setHorizontalHeaderLabels(headers)  # 设置表头
