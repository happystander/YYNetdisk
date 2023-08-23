from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import  time
# 引入线程和自定义信号
from PyQt5.QtCore import QThread,pyqtSignal
import sys

app = QApplication(sys.argv)

class LoginThread(QThread):
    # 创建接受信号
    loginSignal = pyqtSignal(bool)

    def __init__(self,pwd,account,flagRadioBtn_stu,flagRadioBtn_adm):
        super(LoginThread, self).__init__()
        self.pwd, self.account, self.flagRadioBtn_stu, self.flagRadioBtn_adm =  pwd, account, flagRadioBtn_stu, flagRadioBtn_adm

    def run(self):
        # 定义线程来进行登录,具体处理逻辑将放到服务器
        flag = False
        if self.flagRadioBtn_stu:
            if self.pwd == "111111" and self.account == "student":
                print("login in")
                flag = True
            else:
                print("login out")

        elif self.flagRadioBtn_adm:
            if self.pwd == "111111" and self.account == "admin":
                print("login in")
                flag = True
            else:
                print("login out")
        self.loginSignal.emit(flag)

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
            if flag:
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



loadWin = LoadingUI()
loadWin.show()
sys.exit(app.exec_())
