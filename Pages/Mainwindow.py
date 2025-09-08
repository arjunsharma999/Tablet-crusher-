from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1024, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(0, 0, 1024, 601))
        self.widget.setMinimumSize(QtCore.QSize(1024, 600))
        self.widget.setStyleSheet("background-color:#17AEAA;")
        self.widget.setObjectName("widget")
        self.widget_2 = QtWidgets.QWidget(self.widget)
        self.widget_2.setGeometry(QtCore.QRect(45, 32, 931, 531))
        self.widget_2.setMinimumSize(QtCore.QSize(10, 50))
        self.widget_2.setStyleSheet("background-color: #FFF6ED;\n"
"border-radius: 40px;")
        self.widget_2.setObjectName("widget_2")
        self.label = QtWidgets.QLabel(self.widget_2)
        self.label.setGeometry(QtCore.QRect(40, 30, 81, 50))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("C:/Users/Desktop/Desktop/aa-120x120.webp"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(self.widget_2)
        self.lineEdit.setGeometry(QtCore.QRect(380, 220, 113, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.label_5 = QtWidgets.QLabel(self.widget_2)
        self.label_5.setGeometry(QtCore.QRect(50, 460, 51, 41))
        self.label_5.setText("")
        self.label_5.setPixmap(QtGui.QPixmap("C:/Users/Desktop/Downloads/left-arrow (1).png"))
        self.label_5.setScaledContents(True)
        self.label_5.setObjectName("label_5")
        self.dateTimeEdit = QtWidgets.QDateTimeEdit(self.widget_2)
        self.dateTimeEdit.setGeometry(QtCore.QRect(660, 460, 231, 31))
        self.dateTimeEdit.setStyleSheet("font-size: 23px;")
        self.dateTimeEdit.setObjectName("dateTimeEdit")
        self.layoutWidget = QtWidgets.QWidget(self.widget_2)
        self.layoutWidget.setGeometry(QtCore.QRect(170, 130, 611, 301))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setHorizontalSpacing(30)
        self.gridLayout.setVerticalSpacing(20)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton.setMinimumSize(QtCore.QSize(40, 50))
        self.pushButton.setSizeIncrement(QtCore.QSize(0, 0))
        self.pushButton.setStyleSheet("background-color: #17AEAA;\n"
"border-color: rgb(255, 170, 127);\n"
"color: white;\n"
"border-radius:12px;\n"
"font-size: 30px;\n"
"width: 30pt;\n"
"height:20pt;\n"
"font-family: Consolas;")
        self.pushButton.setIconSize(QtCore.QSize(20, 20))
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 0, 0, 1, 1)
        self.pushButton_6 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_6.setMinimumSize(QtCore.QSize(20, 50))
        self.pushButton_6.setStyleSheet("background-color: #17AEAA;\n"
"color:white;\n"
"border-radius: 12px;\n"
"font-size: 30px;\n"
"font-family: Consolas;\n"
"")
        self.pushButton_6.setObjectName("pushButton_6")
        self.gridLayout.addWidget(self.pushButton_6, 0, 2, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_2.setMinimumSize(QtCore.QSize(40, 50))
        self.pushButton_2.setStyleSheet("background-color: #17AEAA;\n"
"border-color: rgb(255, 170, 127);\n"
"color: white;\n"
"border-radius:12px;\n"
"font-size: 30px;\n"
"width: 30pt;\n"
"height:20pt;\n"
"font-family: Consolas;")
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 1, 0, 1, 1)
        self.pushButton_3 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_3.setMinimumSize(QtCore.QSize(40, 50))
        self.pushButton_3.setStyleSheet("background-color: #17AEAA;\n"
"border-color: rgb(255, 170, 127);\n"
"color: white;\n"
"border-radius:12px;\n"
"font-size: 30px;\n"
"width: 30pt;\n"
"height:20pt;\n"
"font-family: Consolas;")
        self.pushButton_3.setObjectName("pushButton_3")
        self.gridLayout.addWidget(self.pushButton_3, 1, 1, 1, 1)
        self.pushButton_5 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_5.setMinimumSize(QtCore.QSize(32, 50))
        self.pushButton_5.setStyleSheet("background-color: #17AEAA;\n"
"color:white;\n"
"border-radius:12px;\n"
"font-size: 30px;\n"
"font-family: Consolas;")
        self.pushButton_5.setObjectName("pushButton_5")
        self.gridLayout.addWidget(self.pushButton_5, 0, 1, 1, 1)
        self.pushButton_4 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_4.setMinimumSize(QtCore.QSize(40, 50))
        self.pushButton_4.setStyleSheet("background-color: #17AEAA;\n"
"border-color: rgb(255, 170, 127);\n"
"color: white;\n"
"border-radius:12px;\n"
"font-size: 30px;\n"
"width: 30pt;\n"
"height:20pt;\n"
"font-family: Consolas;")
        self.pushButton_4.setObjectName("pushButton_4")
        self.gridLayout.addWidget(self.pushButton_4, 1, 2, 1, 1)
        self.pushButton_2.raise_()
        self.pushButton.raise_()
        self.pushButton_5.raise_()
        self.pushButton_6.raise_()
        self.pushButton_3.raise_()
        self.pushButton_4.raise_()
        self.label_2 = QtWidgets.QLabel(self.widget_2)
        self.label_2.setGeometry(QtCore.QRect(790, 40, 31, 31))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("images/report.png"))
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.widget_2)
        self.label_3.setGeometry(QtCore.QRect(830, 40, 31, 31))
        self.label_3.setText("")
        self.label_3.setPixmap(QtGui.QPixmap("images/settings.png"))
        self.label_3.setScaledContents(True)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.widget_2)
        self.label_4.setGeometry(QtCore.QRect(750, 40, 31, 31))
        self.label_4.setText("")
        self.label_4.setPixmap(QtGui.QPixmap("images/user.png"))
        self.label_4.setScaledContents(True)
        self.label_4.setObjectName("label_4")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Start"))
        self.pushButton_6.setText(_translate("MainWindow", "Reports"))
        self.pushButton_2.setText(_translate("MainWindow", "Test"))
        self.pushButton_3.setText(_translate("MainWindow", "Stop"))
        self.pushButton_5.setText(_translate("MainWindow", "Modes"))
        self.pushButton_4.setText(_translate("MainWindow", "Settings"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
