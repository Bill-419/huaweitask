import pandas as pd  # 引入pandas库，用于数据处理
from PySide6.QtWidgets import QTableWidgetItem  # 引入Qt的表格单元项
from PySide6.QtGui import QColor, QFont  # 引入颜色和字体处理工具
from window.database import MongoDBClient  # 从项目的database模块引入MongoDBClient类

# 设置默认行数、列数和表头
DEFAULT_ROWS = 10
DEFAULT_COLUMNS = 11
DEFAULT_HEADERS = [str(i+1) for i in range(DEFAULT_COLUMNS)]  # 生成从1开始的列编号作为表头

# 定义PageUtils类，用于页面数据的加载和存储
class PageUtils:
    def __init__(self, collection_name):
        self.db_client = MongoDBClient()  # 实例化数据库客户端
        self.collection_name = collection_name  # 设置要操作的集合名称
        self.rows = DEFAULT_ROWS  # 初始化行数
        self.columns = DEFAULT_COLUMNS  # 初始化列数
        self.headers = DEFAULT_HEADERS  # 初始化表头
        self.spans = []  # 初始化单元格合并信息列表

    def load_data_from_db(self):
        # 从数据库加载数据
        data = self.db_client.get_data(self.collection_name)
        if not data:
            # 如果没有数据，则返回空的数据结构
            return (
                [['' for _ in range(self.columns)] for _ in range(self.rows)],
                {'': '#ffffff'},  # 默认颜色为白色
                {'': {'bold': False, 'size': 10}},  # 默认字体为非粗体，大小为10
                {'': Qt.AlignCenter},  # 默认居中对齐
                [],  # 默认行高
                []   # 默认列宽
            )

        # 加载各种数据属性
        self.rows = data.get('rows', DEFAULT_ROWS)
        self.columns = data.get('columns', DEFAULT_COLUMNS)
        self.headers = data.get('headers', DEFAULT_HEADERS)
        self.spans = data.get('spans', [])

        # 转换数据为更易于处理的格式
        table_data = data.get("data", [['' for _ in range(self.columns)] for _ in range(self.rows)])
        colors = {(color['row'], color['column']): color['color'] for color in data.get("colors", [])}
        fonts = {(font['row'], font['column']): font for font in data.get("fonts", [])}
        alignments = {(alignment['row'], alignment['column']): alignment['alignment'] for alignment in data.get("alignments", [])}
        row_heights = data.get("row_heights", [])
        col_widths = data.get("col_widths", [])

        return table_data, colors, fonts, alignments, row_heights, col_widths

    def set_table_data(self, table, data, colors, fonts, alignments, row_heights, col_widths, is_admin):
        # 根据加载的数据设置表格
        self.columns = len(data[0])  # 根据数据更新列数
        table.setRowCount(self.rows + 1 if not is_admin else self.rows)  # 设置行数，管理员视图可能不同
        table.setColumnCount(self.columns)  # 设置列数
        self.set_headers(table, is_admin)  # 设置表头

        if is_admin:
            # 如果是管理员，直接加载数据和格式
            for row in range(len(data)):
                for col in range(len(data[row])):
                    item = table.item(row, col)
                    if not item:
                        item = QTableWidgetItem()
                        table.setItem(row, col, item)
                    item.setText(data[row][col])
        else:
            # 如果不是管理员，首行数据用作表头
            for col in range(self.columns):
                header_item = QTableWidgetItem(data[0][col])
                table.setHorizontalHeaderItem(col, header_item)
            # 从第二行开始加载数据
            for row in range(1, len(data)):
                for col in range(len(data[row])):
                    item = table.item(row, col)
                    if not item:
                        item = QTableWidgetItem()
                        table.setItem(row, col, item)
                    item.setText(data[row][col])

        # 应用各种格式设置
        for (row, col), color in colors.items():
            item = table.item(row, col)
            if not item:
                item = QTableWidgetItem()
                table.setItem(row, col, item)
            if QColor.isValidColor(color):
                item.setBackground(QColor(color))
            else:
                item.setBackground(QColor('#ffffff'))  # 默认白色

        for (row, col), font_info in fonts.items():
            item = table.item(row, col)
            if not item:
                item = QTableWidgetItem()
                table.setItem(row, col, item)
            font = QFont()
            font.setBold(font_info['bold'])
            font.setPointSize(font_info['size'])
            item.setFont(font)

        for (row, col), alignment in alignments.items():
            item = table.item(row, col)
            if not item:
                item = QTableWidgetItem()
                table.setItem(row, col, item)
            item.setTextAlignment(alignment)

        # 设置行高和列宽
        for row_height in row_heights:
            table.setRowHeight(row_height['row'], row_height['height'])

        for col_width in col_widths:
            table.setColumnWidth(col_width['col'], col_width['width'])

        # 清除和设置单元格的跨度
        for row in range(self.rows):
            for col in range(self.columns):
                if table.rowSpan(row, col) > 1 or table.columnSpan(row, col) > 1:
                    table.setSpan(row, col, 1, 1)

        for span in self.spans:
            if span['row_span'] > 1 or span['column_span'] > 1:
                table.setSpan(span['row'], span['column'], span['row_span'], span['column_span'])

    def set_headers(self, table, is_admin):
        # 设置表头，管理员模式下从1开始，否则使用已有表头
        if is_admin:
            headers = [str(i+1) for i in range(table.columnCount())]
        else:
            headers = [table.horizontalHeaderItem(i).text() if table.horizontalHeaderItem(i) else str(i+1) for i in range(table.columnCount())]
        table.setHorizontalHeaderLabels(headers)

    def save_to_db(self, table, is_admin):
        # 将表格数据保存回数据库
        spans = []
        colors = []
        fonts = []
        alignments = []
        row_heights = []
        col_widths = []

        # 遍历表格，收集各项数据
        for row in range(table.rowCount()):
            row_height = table.rowHeight(row)
            row_heights.append({'row': row, 'height': row_height})

            for col in range(table.columnCount()):
                col_width = table.columnWidth(col)
                col_widths.append({'col': col, 'width': col_width})

                row_span = table.rowSpan(row, col)
                col_span = table.columnSpan(row, col)
                if row_span > 1 or col_span > 1:
                    spans.append({'row': row, 'column': col, 'row_span': row_span, 'column_span': col_span})
                item = table.item(row, col)
                if item:
                    if item.background().color() != QColor('white'):
                        colors.append({'row': row, 'column': col, 'color': item.background().color().name()})
                    font = item.font()
                    fonts.append({'row': row, 'column': col, 'bold': font.bold(), 'size': font.pointSize()})
                    alignments.append({'row': row, 'column': col, 'alignment': item.textAlignment()})

        # 构建保存数据结构
        data = {
            "rows": table.rowCount() - 1 if not is_admin else table.rowCount(),
            "columns": table.columnCount(),
            "headers": [table.horizontalHeaderItem(i).text() if table.horizontalHeaderItem(i) else '' for i in range(table.columnCount())],
            "data": [[table.item(row, col).text() if table.item(row, col) else '' for col in range(table.columnCount())] for row in range(1 if not is_admin else 0, table.rowCount())],
            "spans": spans,
            "colors": colors,
            "fonts": fonts,
            "alignments": alignments,
            "row_heights": row_heights,
            "col_widths": col_widths
        }
        self.db_client.insert_data(self.collection_name, data)  # 调用数据库客户端的插入数据方法
