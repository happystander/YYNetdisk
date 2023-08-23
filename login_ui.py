from itertools import count
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import requests
import time
# 引入线程和自定义信号
from PyQt5.QtCore import QThread,pyqtSignal
import sys

app = QApplication(sys.argv)
mIP = "http://127.0.0.1:5000/"


class LoginThread(QThread):
    # 创建接受信号
    loginSignal = pyqtSignal(str)

    def __init__(self,pwd,account,flagRadioBtn_stu,flagRadioBtn_adm):
        super(LoginThread, self).__init__()
        self.pwd, self.account, self.flagRadioBtn_stu, \
            self.flagRadioBtn_adm =  pwd, account, flagRadioBtn_stu, flagRadioBtn_adm
        self.loginURL = mIP + 'login'
        self.data = {
            "account":self.account,
            "password":self.pwd,
            "identityFlag":self.flagRadioBtn_stu,
            "cookie":"dasdacusahdcajksdfuasgd23197ehdasdyuaiscgasdtsuhdbfgutyauiwegryfcsdhfgyuaw"
        }
        self._limitTry = 5
        self._countTry = 0

    def run(self):
        #  需要使用线程管理
        # TODO

        if self._countTry < self._limitTry:
            try:
                self._countTry += 1
                response = requests.post(self.loginURL,data=self.data,timeout=10)
                if response.status_code == 200:
                    if DEBUG:
                        print(response.text)
                    flag = response.text
                    self.loginSignal.emit(flag)
            except Exception as e:
                time.sleep(0.5)
                self.run()
        else:
            # 结束线程
            print("Connect error!")

class LoadingUI(QWidget):

        def __init__(self):
            super(LoadingUI, self).__init__()
            self.init_ui()
            self.init_connection()
            # self.loadImg()

        # 进行页面初始化
        def init_ui(self):
            self.loadingWin = uic.loadUi("./loading.ui")
            self.loadBtn = self.loadingWin.pushButton
            self.exitBtn = self.loadingWin.pushButton_2
            self.accountLabel = self.loadingWin.lineEdit
            self.pwdLabel = self.loadingWin.lineEdit_2
            # self.imgView  = self.loadingWin.label_3
            self.radioBtn_stu = self.loadingWin.radioButton
            self.radioBtn_adm = self.loadingWin.radioButton_2

            # 设置样式
            self.accountLabel.setPlaceholderText("Please enter your account")
            self.pwdLabel.setPlaceholderText("Please enter your password")
            self.pwdLabel.setEchoMode(QLineEdit.Password)
            # self.imgView.resize(231, 291)

        # 初始化绑定
        def init_connection(self):
            self.loadBtn.clicked.connect(self.login)
            self.exitBtn.clicked.connect(self.exit)

        # # 载入图片
        # def loadImg(self,path = r"D:\makedownNote\python\PyQt5\Code\img\1.jpg"):
        #     self.pixmap = QPixmap(path)  # 按指定路径找到图片
        #     proportion = self.pixmap.height() / self.height()
        #     self.pixmap.setDevicePixelRatio(proportion)
        #     self.imgView.setScaledContents(True)
        #     self.imgView.setPixmap(self.pixmap)


        def login(self):
            pwd = self.pwdLabel.text().strip()
            account = self.accountLabel.text().strip()
            self.pwdLabel.setText("")
            self.accountLabel.setText("")
            flagRadioBtn_stu = self.radioBtn_stu.isChecked()
            flagRadioBtn_adm = self.radioBtn_adm.isChecked()
            # 创建登录线程
            self.loginThread =LoginThread(pwd,account,flagRadioBtn_stu,flagRadioBtn_adm)
            # 绑定槽函数
            self.loginThread.loginSignal.connect(self.login_succ)
            self.loginThread.start()

        def login_succ(self,flag):
            self.flag = flag
            if flag == "True":
                msg_box = QMessageBox(QMessageBox.Information, 'sign!', '登录成功')
                print("login successfully!")
            else:
                msg_box = QMessageBox(QMessageBox.Information, 'sign!', '登录失败')
                print("failed")
            msg_box.exec_()

        def exit(self):
            QApplication.quit()

        # 重写父类的展示
        def show(self):
            self.loadingWin.show()

if __name__ == "__main__":
    DEBUG= 1
    loadWin = LoadingUI()
    loadWin.show()
    sys.exit(app.exec_())
