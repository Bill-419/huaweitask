from PySide6.QtWidgets import QMenu, QTextEdit, QTableWidgetItem
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from basic_function.basic_operations import BasicOperations
from basic_function.set_operations import SetOperations
from basic_function.merge_operations import MergeOperations

# MenuOperations 类用于管理表格操作的菜单
class MenuOperations:
    def __init__(self, table):
        self.table = table  # 表格对象
        # 初始化不同的操作类
        self.basic_operations = BasicOperations(table)
        self.set_operations = SetOperations(table)
        self.merge_operations = MergeOperations(table)

        # 连接信号和槽
        self.table.cellDoubleClicked.connect(self.on_cell_double_clicked)
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.open_menu)

        # 用于存储原始和编辑后的文本
        self.original_texts = {}  
        self.edited_texts = {}

    def open_menu(self, position):
        menu = QMenu()  # 创建右键菜单

        # 添加各种操作到菜单
        clear_action = menu.addAction("清空单元格")
        add_menu = menu.addMenu("添加")
        add_row_above_action = add_menu.addAction("在上方添加行")
        add_row_below_action = add_menu.addAction("在下方添加行")
        add_col_left_action = add_menu.addAction("在左侧添加列")
        add_col_right_action = add_menu.addAction("在右侧添加列")
        delete_menu = menu.addMenu("删除")
        delete_row_action = delete_menu.addAction("删除行")
        delete_col_action = delete_menu.addAction("删除列")
        set_menu = menu.addMenu("设置")
        set_color_action = set_menu.addAction("设置单元格颜色")
        set_width_action = set_menu.addAction("设置列宽")
        set_height_action = set_menu.addAction("设置行高")
        set_font_size_action = set_menu.addAction("设置字体大小")
        toggle_bold_action = set_menu.addAction("切换加粗")
        align_menu = menu.addMenu("对齐单元格")
        align_left_action = align_menu.addAction("左对齐")
        align_center_action = align_menu.addAction("居中对齐")
        align_right_action = align_menu.addAction("右对齐")
        merge_action = menu.addAction("合并单元格")
        unmerge_action = menu.addAction("取消合并单元格")

        # 执行选择的操作
        action = menu.exec(self.table.viewport().mapToGlobal(position))

        # 根据用户选择执行相应操作
        if action == clear_action:
            self.basic_operations.clear_cells()
        elif action in [add_row_above_action, add_row_below_action]:
            self.basic_operations.add_rows(above=(action == add_row_above_action))
        elif action in [add_col_left_action, add_col_right_action]:
            self.basic_operations.add_columns(left=(action == add_col_left_action))
        elif action == delete_row_action:
            self.basic_operations.delete_rows()
        elif action == delete_col_action:
            self.basic_operations.delete_columns()
        elif action == set_color_action:
            self.set_operations.set_cell_color()
        elif action == set_width_action:
            self.set_operations.set_col_width()
        elif action == set_height_action:
            self.set_operations.set_row_height()
        elif action in [align_left_action, align_center_action, align_right_action]:
            alignment = {
                align_left_action: Qt.AlignmentFlag.AlignLeft,
                align_center_action: Qt.AlignmentFlag.AlignHCenter,
                align_right_action: Qt.AlignmentFlag.AlignRight
            }[action]
            self.basic_operations.align_cells(alignment, Qt.AlignmentFlag.AlignVCenter)
        elif action == set_font_size_action:
            self.set_operations.set_font_size()
        elif action == toggle_bold_action:
            self.set_operations.toggle_bold()
        elif action == merge_action:
            self.merge_operations.merge_cells()
        elif action == unmerge_action:
            self.merge_operations.unmerge_cells()

    def on_cell_double_clicked(self, row, column):
        # 双击单元格时启动编辑模式
        item = self.table.item(row, column)
        if item:
            self.original_texts[(row, column)] = item.text().replace("\n", " ")
            text_edit = QTextEdit()
            text_edit.setPlainText(item.text().replace("\n", " "))
            self.table.setCellWidget(row, column, text_edit)
            text_edit.setFocus()
            text_edit.setTextInteractionFlags(Qt.TextEditorInteraction)
            text_edit.setAlignment(Qt.Alignment(item.textAlignment()))
            background_color = item.background().color() if item.background().color().isValid() else QColor("#ffffff")
            font = item.font()
            alignment = item.textAlignment()
            text_edit.setStyleSheet(f"background-color: {background_color.name()};")
            text_edit.setFont(font)
            text_edit.setAlignment(Qt.Alignment(item.textAlignment()))
            text_edit.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
            text_edit.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

            def focus_out_event(event):
                # 当焦点离开文本编辑器时，保存并替换文本
                self.save_and_replace(row, column, event, background_color, font, alignment)
                QTextEdit.focusOutEvent(text_edit, event)
            text_edit.focusOutEvent = focus_out_event

    def save_and_replace(self, row, column, event, background_color, font, alignment):
        # 保存和替换文本操作
        text_edit = self.table.cellWidget(row, column)
        if text_edit:
            text = text_edit.toPlainText()
            self.table.removeCellWidget(row, column)
            new_item = QTableWidgetItem(text)
            new_item.setBackground(background_color)
            new_item.setFont(font)
            new_item.setTextAlignment(alignment)
            self.table.setItem(row, column, new_item)
            self.original_texts[(row, column)] = text
            self.edited_texts[(row, column)] = text
