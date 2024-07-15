from PySide6.QtWidgets import QApplication
from login import LoginPage
import sys

if __name__ == "__main__":
    # 创建应用程序对象
    app = QApplication(sys.argv)

    # 创建登录页面对象
    login_page = LoginPage()

    # 显示登录页面
    login_page.show()

    # 进入应用程序的主循环，等待事件处理
    sys.exit(app.exec())
