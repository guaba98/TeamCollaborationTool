import random
import sys

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QPoint, Qt, pyqtSignal

from class_client.class_client_1 import ClientApp
# from code.front.class_custom_message_box import NoFrameMessageBox

header_split = chr(1)
list_split_1 = chr(2)
list_split_2 = chr(3)
BUFFER = 50000
FORMAT = "utf-8"

class ClientController(QtWidgets.QWidget):

    def __init__(self, client_app=ClientApp):
        super().__init__()
        self.client_app = ClientApp(self)
        # self.client_app.set_widget(self)
        # ui 동작 관련 변수
        self.list_widget_geometry_x = None
        self.list_widget_geometry_y = None
        self.drag_start_position = QPoint(0, 0)

    # 클라이언트에 send ======================================================================
    def send_message(self, message):
        print(message)
        self.client_object.send_message(message)

    # widget 이동 함수============================================================
    def mousePressEvent(self, widget, event):
        self.drag_start_position = QPoint(widget.x(), widget.y())
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.globalPos() - widget.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, widget, event):
        if event.buttons() == Qt.LeftButton:
            widget.move(event.globalPos() - self.drag_start_position)
            event.accept()
    #===========================================================================
    # 시작화면 show
    def run(self):
        print('클라이언트 시작')
        # self.widget_screen.show()