from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from window.main_window import MainWindow

class LoginPage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """
        初始化用户界面
        """
        self.setWindowTitle('Login Page')  # 设置窗口标题
        self.setGeometry(100, 100, 300, 200)  # 设置窗口位置和大小

        layout = QVBoxLayout()  # 创建一个垂直布局管理器

        self.username_label = QLabel('Username:')  # 创建用户名标签
        self.username_input = QLineEdit()  # 创建用户名输入框
        layout.addWidget(self.username_label)  # 将用户名标签添加到布局中
        layout.addWidget(self.username_input)  # 将用户名输入框添加到布局中

        self.password_label = QLabel('Password:')  # 创建密码标签
        self.password_input = QLineEdit()  # 创建密码输入框
        self.password_input.setEchoMode(QLineEdit.Password)  # 设置密码输入框为密码模式
        layout.addWidget(self.password_label)  # 将密码标签添加到布局中
        layout.addWidget(self.password_input)  # 将密码输入框添加到布局中

        self.login_button = QPushButton('Login')  # 创建登录按钮
        self.login_button.clicked.connect(self.check_login)  # 连接登录按钮的点击信号到检查登录的函数
        layout.addWidget(self.login_button)  # 将登录按钮添加到布局中

        self.setLayout(layout)  # 设置窗口的主布局

    def check_login(self):
        """
        检查用户名和密码
        """
        username = self.username_input.text()  # 获取输入的用户名
        password = self.password_input.text()  # 获取输入的密码
        
        # 预定义的账号信息
        predefined_admin_username = '1'
        predefined_admin_password = '1'
        predefined_user_username = '2'
        predefined_user_password = '2'
        
        # 检查用户名和密码是否匹配
        if username == predefined_admin_username and password == predefined_admin_password:
            self.accept_login(is_admin=True)  # 如果是管理员账号，接受登录并设置为管理员
        elif username == predefined_user_username and password == predefined_user_password:
            self.accept_login(is_admin=False)  # 如果是普通用户账号，接受登录并设置为普通用户
        else:
            QMessageBox.warning(self, 'Error', 'Invalid username or password')  # 弹出警告对话框，提示用户名或密码错误

    def accept_login(self, is_admin):
        """
        接受登录并打开相应的窗口
        """
        self.main_window = MainWindow(is_admin=is_admin)  # 根据用户权限创建主窗口
        self.main_window.show()  # 显示主窗口
        self.close()  # 关闭登录窗口
