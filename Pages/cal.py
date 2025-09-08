from PyQt5 import QtCore, QtGui, QtWidgets
from mysql.connector import Error
from Middleware.Connect_db import get_connection


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1024, 600)
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(0, 0, 1024, 600))
        self.widget.setMinimumSize(QtCore.QSize(1024, 600))
        self.widget.setStyleSheet("background-color: #17AEAA;")
        self.widget.setObjectName("widget")
        self.widget_2 = QtWidgets.QWidget(self.widget)
        self.widget_2.setGeometry(QtCore.QRect(45, 32, 931, 532))
        self.widget_2.setMinimumSize(QtCore.QSize(931, 532))
        self.widget_2.setStyleSheet("background-color: #FFF6ED;\n"
"border-radius: 40px;")
        self.widget_2.setObjectName("widget_2")
        self.label_4 = QtWidgets.QLabel(self.widget_2)
        self.label_4.setGeometry(QtCore.QRect(40, 30, 81, 50))
        self.label_4.setText("")
        self.label_4.setPixmap(QtGui.QPixmap("C:/Users/Desktop/Desktop/aa-120x120.webp"))
        self.label_4.setScaledContents(True)
        self.label_4.setObjectName("label_4")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.widget_2)
        self.lineEdit_2.setGeometry(QtCore.QRect(380, 120, 180, 52))
        self.lineEdit_2.setMinimumSize(QtCore.QSize(90, 46))
        self.lineEdit_2.setStyleSheet("background-color: #D9D9D9;\n"
"border-radius: 18px;\n"
"font-size:14px;\n"
"")
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.pushButton = QtWidgets.QPushButton(self.widget_2)
        self.pushButton.setGeometry(QtCore.QRect(160, 370, 111, 41))
        self.pushButton.setStyleSheet("background-color: #FEC04D;\n"
"border-radius: 18px;\n"
"font-size: 21px;")
        self.pushButton.setObjectName("pushButton")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.widget_2)
        self.lineEdit_3.setGeometry(QtCore.QRect(610, 120, 180, 52))
        self.lineEdit_3.setMinimumSize(QtCore.QSize(90, 46))
        self.lineEdit_3.setStyleSheet("background-color: #D9D9D9;\n"
"border-radius: 18px;\n"
"font-size: 14px;\n"
"")
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.lineEdit_4 = QtWidgets.QLineEdit(self.widget_2)
        self.lineEdit_4.setGeometry(QtCore.QRect(150, 120, 180, 52))
        self.lineEdit_4.setMinimumSize(QtCore.QSize(90, 46))
        self.lineEdit_4.setStyleSheet("background-color: #D9D9D9;\n"
"border-radius: 18px;\n"
"font-size: 14px;")
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.lineEdit_5 = QtWidgets.QLineEdit(self.widget_2)
        self.lineEdit_5.setGeometry(QtCore.QRect(150, 220, 180, 52))
        self.lineEdit_5.setMinimumSize(QtCore.QSize(90, 46))
        self.lineEdit_5.setStyleSheet("background-color: #D9D9D9;\n"
"border-radius: 18px;\n"
"font-size: 14px")
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.label_5 = QtWidgets.QLabel(self.widget_2)
        self.label_5.setGeometry(QtCore.QRect(50, 460, 51, 41))
        self.label_5.setText("")
        self.label_5.setPixmap(QtGui.QPixmap("C:/Users/Desktop/Downloads/left-arrow (1).png"))
        self.label_5.setScaledContents(True)
        self.label_5.setObjectName("label_5")
        self.label = QtWidgets.QLabel(self.widget_2)
        self.label.setGeometry(QtCore.QRect(830, 40, 31, 31))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("images/settings.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.widget_2)
        self.label_2.setGeometry(QtCore.QRect(750, 40, 31, 31))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("images/user.png"))
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.widget_2)
        self.label_3.setGeometry(QtCore.QRect(790, 40, 31, 31))
        self.label_3.setText("")
        self.label_3.setPixmap(QtGui.QPixmap("images/report.png"))
        self.label_3.setScaledContents(True)
        self.label_3.setObjectName("label_3")


        self.lineEdit_6 = QtWidgets.QLineEdit(self.widget_2)
        self.lineEdit_6.setGeometry(QtCore.QRect(380, 220, 180, 52))  # Adjust x,y to place it properly
        self.lineEdit_6.setMinimumSize(QtCore.QSize(90, 46))
        self.lineEdit_6.setStyleSheet("background-color: #D9D9D9;\n"
        "border-radius: 18px;\n"
        "font-size: 14px")
        self.lineEdit_6.setObjectName("lineEdit_6")


        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.lineEdit_2.setText(_translate("Form", "              Batch No"))
        self.pushButton.setText(_translate("Form", "Next"))
        self.lineEdit_3.setText(_translate("Form", "            Sensitivity"))
        self.lineEdit_4.setText(_translate("Form", "         Customer Name"))
        self.lineEdit_5.setText(_translate("Form", "             Paper gsm"))
        self.lineEdit_6.setText(_translate("Form", "             Roll no"))



    def save_to_db(self):
        customer_name = self.lineEdit_4.text().strip() if hasattr(self, "lineEdit_4") else ""
        batch_no = self.lineEdit_2.text().strip() if hasattr(self, "lineEdit_2") else ""
        paper_gsm_text = self.lineEdit_5.text().strip() if hasattr(self, "lineEdit_5") else ""
        roll_no = self.lineEdit_6.text().strip() if hasattr(self, "lineEdit_6") else ""
        sensitivity = self.lineEdit_3.text().strip() if hasattr(self, "lineEdit_3") else ""

        # Basic validation
        if not customer_name:
            QtWidgets.QMessageBox.warning(None, "Validation", "Customer name is required.")
            return False

        paper_gsm = None
        if paper_gsm_text:
            try:
                paper_gsm = int(paper_gsm_text)
            except ValueError:
                QtWidgets.QMessageBox.warning(None, "Validation", "Paper GSM must be a number.")
                return False

        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = connection.cursor()
            sql = (
                "INSERT INTO customer_data (customer_name, batch_no, paper_gsm, roll_no, sensitivity) "
                "VALUES (%s, %s, %s, %s, %s)"
            )
            values = (customer_name, batch_no or None, paper_gsm, roll_no or None, sensitivity or None)
            cursor.execute(sql, values)
            connection.commit()
            QtWidgets.QMessageBox.information(None, "Success", "Data inserted successfully!")
            return True
        except Error as e:
            QtWidgets.QMessageBox.warning(None, "Error", f"Database error: {e}")
            return False
        except Exception as e:
            QtWidgets.QMessageBox.warning(None, "Error", f"Unexpected error: {e}")
            return False
        finally:
            try:
                if cursor is not None:
                    cursor.close()
                if connection is not None and connection.is_connected():
                    connection.close()
            except Exception:
                pass
  

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
