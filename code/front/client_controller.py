import random
import sys

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QPoint, Qt, pyqtSignal

from class_client.class_client import ClientApp
# from code.front.class_custom_message_box import NoFrameMessageBox

# ui 임풜트 예아
from code.front.main_window import WidgetNoticeBorad

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
        # ui 인슬퉐트화
        self.main_window = WidgetNoticeBorad(self)
        # ui 동작 관련 변수
        self.list_widget_geometry_x = None
        self.list_widget_geometry_y = None
        self.drag_start_position = QPoint(0, 0)



    # 클라이언트에 send메시지 보내기======================================================================
    def controller_send_message(self, message):
        self.client_app.client_send_message(message)
    def controller_send_chat_message(self, input_chat):
        self.client_app.client_send_chat_message(input_chat)
    def controller_send_json_message(self, message):
        self.client_app.client_send_json_message(message)

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

    #런처 실행시 나오는 window ===========================================================================
    def run(self): # 시작화면 show
        self.main_window.show()

    # 로그인 ===============================================================

    def emit_login(self, p):
        print('로그인 결과:',p)

    # 회원가입 ============================================================
    def emit_duple(self, result):
        print('[client_controller]-emit_duple', result)
        self.main_window.reg_id_lab_signal.emit(result)
        # if result == False:
        #     self.main_window.reg_id_lab_signal.emit(False)
        # else:
        #     self.main_window.reg_id_lab_signal.emit(True)
    def emit_insertuser(self, result):
        print('[client_controller]-emit_duple', result)
        self.main_window.recv_emit_insertuser.emit(result)

    def send_register_user_info(self):
        pass

    # 채팅=====================================================================
    def emit_recv_chat(self, result):
        self.main_window.emit_recv_chat_signal.emit(result)
        pass