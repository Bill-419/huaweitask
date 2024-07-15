import pandas as pd
from PySide6.QtWidgets import QTableWidgetItem
from PySide6.QtGui import QColor, QFont
from PySide6.QtCore import Qt
from window.database import MongoDBClient

DEFAULT_ROWS = 10
DEFAULT_COLUMNS = 11
DEFAULT_HEADERS = [str(i + 1) for i in range(DEFAULT_COLUMNS)]

class PageUtils:
    def __init__(self, collection_name):
        self.db_client = MongoDBClient()
        self.collection_name = collection_name
        self.rows = DEFAULT_ROWS
        self.columns = DEFAULT_COLUMNS
        self.headers = DEFAULT_HEADERS
        self.spans = []

    def load_data_from_db(self):
        try:
            data = self.db_client.get_data(self.collection_name)
            if not data:
                return (
                    [['' for _ in range(self.columns)] for _ in range(self.rows)],
                    {},
                    {},
                    {},
                    [],
                    []
                )

            self.rows = data.get('rows', DEFAULT_ROWS)
            self.columns = data.get('columns', DEFAULT_COLUMNS)
            self.headers = data.get('headers', DEFAULT_HEADERS)
            self.spans = data.get('spans', [])

            table_data = data.get("data", [['' for _ in range(self.columns)] for _ in range(self.rows)])
            colors = {(color['row'], color['column']): color['color'] for color in data.get("colors", []) if 'row' in color and 'column' in color}
            fonts = {(font['row'], font['column']): font for font in data.get("fonts", []) if 'row' in font and 'column' in font}
            alignments = {(alignment['row'], alignment['column']): alignment['alignment'] for alignment in data.get("alignments", []) if 'row' in alignment and 'column' in alignment}
            row_heights = data.get("row_heights", [])
            col_widths = data.get("col_widths", [])

            return table_data, colors, fonts, alignments, row_heights, col_widths
        except Exception as e:
            print(f"Error loading data from database: {e}")
            return (
                [['' for _ in range(self.columns)] for _ in range(self.rows)],
                {},
                {},
                {},
                [],
                []
            )

    def set_table_data(self, table, data, colors, fonts, alignments, row_heights, col_widths, is_admin):
        try:
            self.columns = len(data[0])
            table.setRowCount(self.rows + 1 if not is_admin else self.rows)
            table.setColumnCount(self.columns)
            self.set_headers(table, is_admin)

            if is_admin:
                for row in range(len(data)):
                    for col in range(len(data[row])):
                        item = table.item(row, col)
                        if not item:
                            item = QTableWidgetItem()
                            table.setItem(row, col, item)
                        item.setText(data[row][col])
            else:
                for col in range(self.columns):
                    header_item = QTableWidgetItem(data[0][col])
                    table.setHorizontalHeaderItem(col, header_item)
                for row in range(1, len(data)):
                    for col in range(len(data[row])):
                        item = table.item(row, col)
                        if not item:
                            item = QTableWidgetItem()
                            table.setItem(row, col, item)
                        item.setText(data[row][col])

            for (row, col), color in colors.items():
                item = table.item(row, col)
                if not item:
                    item = QTableWidgetItem()
                    table.setItem(row, col, item)
                if QColor.isValidColor(color):
                    item.setBackground(QColor(color))

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

            for row_height in row_heights:
                table.setRowHeight(row_height['row'], row_height['height'])

            for col_width in col_widths:
                table.setColumnWidth(col_width['col'], col_width['width'])

            for row in range(self.rows):
                for col in range(self.columns):
                    if table.rowSpan(row, col) > 1 or table.columnSpan(row, col) > 1:
                        table.setSpan(row, col, 1, 1)

            for span in self.spans:
                if span['row_span'] > 1 or span['column_span'] > 1:
                    table.setSpan(span['row'], span['column'], span['row_span'], span['column_span'])
        except Exception as e:
            print(f"Error setting table data: {e}")

    def set_headers(self, table, is_admin):
        if is_admin:
            headers = [str(i + 1) for i in range(table.columnCount())]
        else:
            headers = [table.horizontalHeaderItem(i).text() if table.horizontalHeaderItem(i) else str(i + 1) for i in range(table.columnCount())]
        table.setHorizontalHeaderLabels(headers)

    def save_to_db(self, table, is_admin):
        try:
            spans = []
            colors = []
            fonts = []
            alignments = []
            row_heights = []
            col_widths = []

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
            self.db_client.insert_data(self.collection_name, data)
        except Exception as e:
            print(f"Error saving data to database: {e}")
