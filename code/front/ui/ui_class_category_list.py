# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'category_list.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_CtgWidget(object):
    def setupUi(self, CtgWidget):
        CtgWidget.setObjectName("CtgWidget")
        CtgWidget.resize(240, 44)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(CtgWidget)
        self.horizontalLayout_2.setContentsMargins(35, 0, 35, 16)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.h_lay = QtWidgets.QHBoxLayout()
        self.h_lay.setObjectName("h_lay")
        self.img_lab = QtWidgets.QLabel(CtgWidget)
        self.img_lab.setMinimumSize(QtCore.QSize(24, 24))
        self.img_lab.setMaximumSize(QtCore.QSize(24, 24))
        self.img_lab.setScaledContents(True)
        self.img_lab.setObjectName("img_lab")
        self.h_lay.addWidget(self.img_lab)
        spacerItem = QtWidgets.QSpacerItem(18, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.h_lay.addItem(spacerItem)
        self.ctg_name_lab = QtWidgets.QLabel(CtgWidget)
        self.ctg_name_lab.setObjectName("ctg_name_lab")
        self.h_lay.addWidget(self.ctg_name_lab)
        self.horizontalLayout_2.addLayout(self.h_lay)

        self.retranslateUi(CtgWidget)
        QtCore.QMetaObject.connectSlotsByName(CtgWidget)

    def retranslateUi(self, CtgWidget):
        _translate = QtCore.QCoreApplication.translate
        CtgWidget.setWindowTitle(_translate("CtgWidget", "Form"))
        self.img_lab.setText(_translate("CtgWidget", "사진"))
        self.ctg_name_lab.setText(_translate("CtgWidget", "카테고리이름"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    CtgWidget = QtWidgets.QWidget()
    ui = Ui_CtgWidget()
    ui.setupUi(CtgWidget)
    CtgWidget.show()
    sys.exit(app.exec_())
