from PySide6.QtWidgets import QColorDialog, QInputDialog, QTableWidgetItem
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

# SetOperations 类用于设置表格单元格的颜色、行高、列宽和字体样式
class SetOperations:
    # 构造函数初始化类，接收表格对象
    def __init__(self, table):
        self.table = table

    # 设置选中单元格的颜色
    def set_cell_color(self):
        color = QColorDialog.getColor()  # 打开颜色选择对话框
        if color.isValid():  # 如果选中的颜色有效
            for index in self.table.selectedIndexes():  # 遍历所有选中的单元格
                item = self.table.item(index.row(), index.column())
                if not item:  # 如果单元格不存在，创建新的单元格
                    item = QTableWidgetItem()
                    self.table.setItem(index.row(), index.column(), item)
                    item.setBackground(QColor('white'))  # 设置默认的白色背景
                item.setBackground(color)  # 设置单元格的背景颜色

    # 设置选中行的高度
    def set_row_height(self):
        rows = set(index.row() for index in self.table.selectedIndexes())  # 获取所有选中的行
        height, ok = QInputDialog.getInt(self.table, "Set Row Height", "Enter new row height:", 30, 10, 500, 1)  # 打开输入对话框获取新的行高
        if ok:  # 如果用户点击确认
            for row in rows:
                self.table.setRowHeight(row, height)  # 设置行高

    # 设置选中列的宽度
    def set_col_width(self):
        cols = set(index.column() for index in self.table.selectedIndexes())  # 获取所有选中的列
        width, ok = QInputDialog.getInt(self.table, "Set Column Width", "Enter new column width:", 100, 10, 500, 1)  # 打开输入对话框获取新的列宽
        if ok:  # 如果用户点击确认
            for col in cols:
                self.table.setColumnWidth(col, width)  # 设置列宽

    # 设置选中单元格的字体大小
    def set_font_size(self):
        size, ok = QInputDialog.getInt(self.table, "Set Font Size", "Enter new font size:", 10, 1, 100, 1)  # 打开输入对话框获取新的字体大小
        if ok:  # 如果用户点击确认
            for index in self.table.selectedIndexes():  # 遍历所有选中的单元格
                item = self.table.item(index.row(), index.column())
                if item is None:  # 如果单元格不存在，创建新的单元格
                    item = QTableWidgetItem()
                    self.table.setItem(index.row(), index.column(), item)
                widget = self.table.cellWidget(index.row(), index.column())
                if widget:  # 如果单元格是一个特殊控件
                    font = widget.font()  # 获取控件的字体
                    font.setPointSize(size)  # 设置字体大小
                    widget.setFont(font)
                else:
                    font = item.font()  # 获取单元格字体
                    font.setPointSize(size)  # 设置字体大小
                    item.setFont(font)

    # 切换选中单元格的字体粗体状态
    def toggle_bold(self):
        for index in self.table.selectedIndexes():  # 遍历所有选中的单元格
            item = self.table.item(index.row(), index.column())
            if item is None:  # 如果单元格不存在，创建新的单元格
                item = QTableWidgetItem()
                self.table.setItem(index.row(), index.column(), item)
            widget = self.table.cellWidget(index.row(), index.column())
            if widget:  # 如果单元格是一个特殊控件
                font = widget.font()  # 获取控件的字体
                font.setBold(not font.bold())  # 切换字体粗体状态
                widget.setFont(font)
            else:
                font = item.font()  # 获取单元格字体
                font.setBold(not font.bold())  # 切换字体粗体状态
                item.setFont(font)
