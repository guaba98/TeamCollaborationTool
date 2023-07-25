from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

from code.front.ui.ui_class_notice_board import Ui_NoticeBoard


class WidgetNoticeBorad(QMainWindow, Ui_NoticeBoard):
    def __init__(self, client_co  ㅍntroller):
        super().__init__()
        self.setupUi(self)
        self.client_controller = client_controller

    def mousePressEvent(self, event):
        self.client_controller.mousePressEvent(self, event)

    def mouseMoveEvent(self, event):
        self.client_controller.mouseMoveEvent(self, event)

    def show(self):  # window widget show

        super().show()
