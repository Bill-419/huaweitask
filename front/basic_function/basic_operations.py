# 从 PySide6.QtWidgets 导入 QTableWidgetItem 类来创建表格单元格，从 PySide6.QtCore 导入 Qt 用于使用常量
from PySide6.QtWidgets import QTableWidgetItem
from PySide6.QtCore import Qt

# 定义一个名为 BasicOperations 的类，用于执行表格操作
class BasicOperations:
    # 构造函数：初始化实例并传入一个表格控件的引用
    def __init__(self, table):
        self.table = table  # 保存对表格控件的引用

    # 方法：清除表格中选中单元格的文本
    def clear_cells(self):
        for item in self.table.selectedItems():  # 遍历表格中每个选中的单元格
            item.setText("")  # 将选中单元格的文本设置为空字符串

    # 方法：在选中的行上方或下方添加行
    def add_rows(self, above):
        rows = sorted(set(index.row() for index in self.table.selectedIndexes()))  # 获取所有选中单元格的行号，并去重、排序
        count = len(rows)  # 计算选中行的数量
        insert_at = rows[0] if above else rows[-1] + 1  # 判断是在上方还是下方添加行，并确定插入位置
        for _ in range(count):  # 根据选中行的数量重复添加行
            self.table.insertRow(insert_at)  # 在指定位置插入行
            for column in range(self.table.columnCount()):  # 遍历所有列
                item = QTableWidgetItem()  # 创建新的单元格项
                item.setBackground(Qt.white)  # 设置单元格背景为白色
                self.table.setItem(insert_at, column, item)  # 将新的单元格项添加到表格中

    # 方法：在选中的列左侧或右侧添加列
    def add_columns(self, left):
        columns = sorted(set(index.column() for index in self.table.selectedIndexes()))  # 获取所有选中单元格的列号，并去重、排序
        count = len(columns)  # 计算选中列的数量
        insert_at = columns[0] if left else columns[-1] + 1  # 判断是在左侧还是右侧添加列，并确定插入位置
        for _ in range(count):  # 根据选中列的数量重复添加列
            self.table.insertColumn(insert_at)  # 在指定位置插入列
            for row in range(self.table.rowCount()):  # 遍历所有行
                item = QTableWidgetItem()  # 创建新的单元格项
                item.setBackground(Qt.white)  # 设置单元格背景为白色
                self.table.setItem(row, insert_at, item)  # 将新的单元格项添加到表格中

    # 方法：删除选中的行
    def delete_rows(self):
        rows = sorted(set(index.row() for index in self.table.selectedIndexes()), reverse=True)  # 获取所有选中行的行号，并去重、倒序排序
        for row in rows:  # 遍历所有选中的行
            self.table.removeRow(row)  # 删除行

    # 方法：删除选中的列
    def delete_columns(self):
        columns = sorted(set(index.column() for index in self.table.selectedIndexes()), reverse=True)  # 获取所有选中列的列号，并去重、倒序排序
        for col in columns:  # 遍历所有选中的列
            self.table.removeColumn(col)  # 删除列

    # 方法：设置选中单元格的对齐方式
    def align_cells(self, horizontal_alignment, vertical_alignment):
        for index in self.table.selectedIndexes():  # 遍历所有选中的单元格
            item = self.table.item(index.row(), index.column())  # 获取单元格项
            if not item:
                item = QTableWidgetItem()  # 如果单元格项不存在，则创建新的单元格项
                self.table.setItem(index.row(), index.column(), item)  # 将新的单元格项添加到表格中
            item.setTextAlignment(horizontal_alignment | vertical_alignment)  # 设置单元格的文本对齐方式
