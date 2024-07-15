from PySide6.QtWidgets import QTableWidgetItem
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor

class MergeOperations:
    def __init__(self, table):
        self.table = table

    def merge_cells(self):
        selected_ranges = self.table.selectedRanges()
        if not selected_ranges:
            return

        top_row = min(selected_range.topRow() for selected_range in selected_ranges)
        bottom_row = max(selected_range.bottomRow() for selected_range in selected_ranges)
        left_col = min(selected_range.leftColumn() for selected_range in selected_ranges)
        right_col = max(selected_range.rightColumn() for selected_range in selected_ranges)

        # 确保选择跨越多行或多列
        if bottom_row == top_row and right_col == left_col:
            return

        # 查找第一个非空单元格的文本、背景颜色和字体
        text = ''
        background_color = QColor("#ffffff")
        font = self.table.font()
        found_non_empty = False
        for col in range(left_col, right_col + 1):
            for row in range(top_row, bottom_row + 1):
                item = self.table.item(row, col)
                if item and item.text().strip():
                    text = item.text()
                    background_color = item.background().color()
                    font = item.font()
                    found_non_empty = True
                    break
            if found_non_empty:
                break

        # 清空所有选中单元格的文本并保留背景颜色和字体，除了第一个单元格
        for row in range(top_row, bottom_row + 1):
            for col in range(left_col, right_col + 1):
                if row == top_row and col == left_col:
                    continue
                item = self.table.item(row, col)
                if not item:
                    item = QTableWidgetItem()
                    self.table.setItem(row, col, item)
                item.setText('')
                item.setBackground(background_color)
                item.setFont(font)

        # 设置跨度和在左上角单元格中设置文本
        self.table.setSpan(top_row, left_col, bottom_row - top_row + 1, right_col - left_col + 1)
        if not self.table.item(top_row, left_col):
            self.table.setItem(top_row, left_col, QTableWidgetItem())
        top_left_item = self.table.item(top_row, left_col)
        top_left_item.setText(text)
        top_left_item.setBackground(background_color)
        top_left_item.setFont(font)

    def unmerge_cells(self):
        selected_ranges = self.table.selectedRanges()
        if not selected_ranges:
            return

        for selected_range in selected_ranges:
            top_row = selected_range.topRow()
            left_col = selected_range.leftColumn()
            bottom_row = selected_range.bottomRow()
            right_col = selected_range.rightColumn()

            merged_item = self.table.item(top_row, left_col)
            merged_text = merged_item.text() if merged_item else ''
            background_color = merged_item.background().color() if merged_item else QColor("#ffffff")
            font = merged_item.font() if merged_item else self.table.font()

            for row in range(top_row, bottom_row + 1):
                for col in range(left_col, right_col + 1):
                    # 只有当单元格是合并的一部分时才取消合并
                    if self.table.rowSpan(row, col) > 1 or self.table.columnSpan(row, col) > 1:
                        self.table.setSpan(row, col, 1, 1)
                    item = self.table.item(row, col)
                    if not item:
                        item = QTableWidgetItem()
                        self.table.setItem(row, col, item)
                    item.setBackground(background_color)
                    item.setFont(font)
                    item.setFlags(item.flags() | Qt.ItemIsEditable)  # 确保单元格可编辑
                    if row == top_row and col == left_col:
                        item.setText(merged_text)
                    else:
                        item.setText('')
