# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'message_label_left.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_LeftMessage(object):
    def setupUi(self, LeftMessage):
        LeftMessage.setObjectName("LeftMessage")
        LeftMessage.resize(439, 45)
        LeftMessage.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(LeftMessage)
        self.horizontalLayout_2.setContentsMargins(40, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.widget = QtWidgets.QWidget(LeftMessage)
        self.widget.setMaximumSize(QtCore.QSize(400, 16777215))
        self.widget.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"    border-top-right-radius: 20px;\n"
"    border-bottom-left-radius: 20px;\n"
"    border-bottom-right-radius:20px;")
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout_2.addWidget(self.widget)

        self.retranslateUi(LeftMessage)
        QtCore.QMetaObject.connectSlotsByName(LeftMessage)

    def retranslateUi(self, LeftMessage):
        _translate = QtCore.QCoreApplication.translate
        LeftMessage.setWindowTitle(_translate("LeftMessage", "Form"))
        self.label.setText(_translate("LeftMessage", "여기는 타인의 메세지 메세지"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    LeftMessage = QtWidgets.QWidget()
    ui = Ui_LeftMessage()
    ui.setupUi(LeftMessage)
    LeftMessage.show()
    sys.exit(app.exec_())
