import random
import sys

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QPoint, Qt, pyqtSignal

from class_client.class_client import ClientApp

# ui 임풜트 예아
from main_code.front.main_window import NoticeBorad

header_split = chr(1)
list_split_1 = chr(2)
list_split_2 = chr(3)
BUFFER = 50000
FORMAT = "utf-8"


def set_main_window(clientcontroller):
    main_window = NoticeBorad(clientcontroller)
    return main_window


class ClientController(QtWidgets.QWidget):

    def __init__(self, client_app=ClientApp):
        super().__init__()
        self.client_app = ClientApp(self)
        # self.client_app.set_widget(self)
        # ui 인슬퉐트화
        self.main_window = NoticeBorad(self)
        # ui 동작 관련 변수
        self.list_widget_geometry_x = None
        self.list_widget_geometry_y = None
        self.drag_start_position = QPoint(0, 0)
        self.main_window = None

    # 좌상단 프로필
    def emit_update_user_message(self):
        self.main_window.update_user_message_signal.emit()

    def emit_get_team_member(self, p):
        self.main_window.get_team_member_signal.emit(p)

    # 그래프
    def emit_set_matplotlib(self, p):
        self.main_window.set_matplotlib_signal.emit(p)

    # 투두 ==============================
    def emit_recv_get_todolist(self, p):
        self.main_window.recv_get_todolist_signal.emit(p)

    def emit_member_todo_list_for_admin(self, p):
        self.main_window.member_todo_list_for_admin_signal.emit(p)

    def emit_member_todo_list_for_admin2(self, p):
        self.main_window.member_todo_list_for_admin_signal2.emit(p)

    def emit_refresh_todolist(self):
        self.main_window.refresh_todolist_signal.emit()

    # 공지 ==============================
    def emit_recv_get_notice(self, p):
        self.main_window.recv_get_notice_signal.emit(p)

    def emit_refresh_notice(self):
        self.main_window.refresh_notice_signal.emit()

    # 클라이언트에 send메시지 보내기======================================================================
    # main_window에서 만든 구분자 send
    def controller_send_message(self, message):
        self.client_app.client_send_message(message)

    # 메시지 send
    def controller_send_chat_message(self, input_chat):
        self.client_app.client_send_chat_message(input_chat)

    def controller_send_get_todolist(self):
        self.client_app.client_send_get_todolist()

    # 데이터가 많아 list로 보낼때
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

    # 런처 실행시 나오는 window ===========================================================================
    def run(self):  # 시작화면 show
        self.main_window = set_main_window(self)
        # self.main_window.show()
        self.main_window.show()

    def re_(self):
        self.main_window = set_main_window(self)
        self.main_window.show()
        # self.main_window.show()

    # 로그인 ===============================================================

    def emit_login(self, p):
        # 로그인 결과값 main에 전달 False면 실패창 True면 성공창 main화면 전환
        if p:
            self.main_window.recv_login_signal.emit(p)
        else:
            self.main_window.recv_login_signal.emit(p)

    def emit_admin_login(self, p):
        self.main_window.admin_login_signal.emit(p)

    # 회원가입 ============================================================
    def emit_duple(self, result):  # 아이디 중복 확인 결과 보내기
        self.main_window.reg_id_lab_signal.emit(result)

    def emit_set_combobox(self, result):
        self.main_window.set_combobox_signal.emit(result)

    def emit_insertuser(self, result):  # 회원가입 성공 결과 보내기
        self.main_window.recv_emit_insertuser.emit(result)

    def send_register_user_info(self):
        pass

    # 채팅=====================================================================

    # 서버에서 받은 메시지을 누가 보낸것 인지 구분
    def emit_recv_chat(self, result):
        user_no, team_no, name, chat = result
        if user_no == str(self.client_app.user_no):  # 본인이 보낸 메시지면
            self.main_window.emit_signal_my_chat.emit(result)
        else:  # 다른 유저가 보낸 메시지면
            self.main_window.emit_signal_chat.emit(result)

    def emit_get_chatin_log(self, result):
        for i in result:
            self.main_window.emit_signal_chat.emit(i)
