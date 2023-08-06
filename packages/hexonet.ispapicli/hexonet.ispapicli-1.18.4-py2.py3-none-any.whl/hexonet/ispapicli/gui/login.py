from PyQt5.QtWidgets import (
    QApplication,
    QMessageBox,
    QDialog,
    QGridLayout,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QComboBox,
    QLabel,
    QStyleFactory,
    QGroupBox,
    QPushButton,
    QFormLayout,
    QDesktopWidget,
)
from PyQt5.QtCore import Qt
import time
import threading


class LoginWindow(QDialog):
    def __init__(self, parent, coreLogic):
        super(LoginWindow, self).__init__(parent)

        self.coreLogic = coreLogic

        self.originalPalette = QApplication.palette()
        self.createRightGroupBox()

        mainLayout = QGridLayout()
        mainLayout.addWidget(self.rightGroupBox, 0, 0)
        self.setLayout(mainLayout)
        self.setWindowTitle("Login Window")
        QApplication.setStyle(QStyleFactory.create("Fusion"))

    def createRightGroupBox(self):
        self.rightGroupBox = QGroupBox("Login Info:")

        loginBox = QGridLayout()
        self.userIDTxt = QLineEdit()
        self.passTxt = QLineEdit()
        self.passTxt.setEchoMode(QLineEdit.Password)
        self.sysChoice = QComboBox()
        self.sysChoice.addItems(["live", "ote"])
        self.loginMsg = QLabel("")
        self.loginMsg.setAlignment(Qt.AlignCenter)

        self.loginBtn = QPushButton("Login")
        self.loginBtn.clicked.connect(self.login)

        formLayout = QFormLayout()
        formLayout.addRow(self.tr("Your ID:"), self.userIDTxt)
        formLayout.addRow(self.tr("Password:"), self.passTxt)
        formLayout.addRow(self.tr("System:"), self.sysChoice)
        formLayout.addRow(self.tr(""), self.loginBtn)
        formLayout.addRow(self.tr(""), self.loginMsg)
        layout = QGridLayout()
        layout.addLayout(formLayout, 0, 0)

        self.rightGroupBox.setLayout(layout)

    def login(self):
        # disable login button
        self.loginBtn.setEnabled(False)
        self.loginBtn.setText("Please wait...")
        QApplication.processEvents()

        args = {}
        args["userid"] = self.userIDTxt.text()
        args["password"] = self.passTxt.text()
        args["entity"] = self.sysChoice.currentText()

        result, msg = self.coreLogic.login(args)

        if result == True:
            # update the subuser
            self.coreLogic.getSubUsers()
            # update parent window = login and session message
            self.parent().checkLogin()
            self.parent().initialiseSubuserCompleter()
            # show a message
            alert = QMessageBox()
            alert.setText("You have successfully logged in!")
            alert.exec_()
            # close login gui
            self.closingThread = threading.Thread(target=self.__closeGui).start()
            return True

        else:
            self.loginBtn.setEnabled(True)
            self.loginBtn.setText("Login")
            QApplication.processEvents()
            self.loginMsg.setText(msg)
            self.loginMsg.setStyleSheet("color:red")
            return False

    def __closeGui(self):
        # disable login button
        self.loginBtn.setDisabled(True)
        for i in range(2, 0, -1):
            self.loginMsg.setText("Closing the window in " + str(i) + "s")
            time.sleep(1)
        else:
            try:
                self.close()
            except Exception as e:
                pass

    def startGui(self):

        geo = QDesktopWidget().availableGeometry()
        screenWidth = geo.width()
        screenHeight = geo.height()
        width = int(screenWidth * 0.2)
        height = int(screenHeight * 0.2)
        self.resize(width, height)

        frameGeo = self.frameGeometry()
        cp = geo.center()
        frameGeo.moveCenter(cp)
        self.move(frameGeo.topLeft())

        self.show()
