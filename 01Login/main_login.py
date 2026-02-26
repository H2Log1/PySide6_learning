from PySide6.QtWidgets import QApplication, QWidget, QPushButton
from PySide6.QtCore import Qt
from Ui_登录框 import Ui_Form

class MyWindow(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.pushButton.clicked.connect(self.loginFunc)

    
    def loginFunc(self):
        account = self.lineEdit.text()
        password = self.lineEdit_2.text()

        if account == "admin" and password == "123456":
            print("登录成功！")
        else:
            print("登录失败！")


if __name__ == "__main__":
    app = QApplication([])
    window = MyWindow()
    window.show()
    app.exec()