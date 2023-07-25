import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
# from code.front.client_controller import ClientController
from code.front.ui.ui_class_notice_board import Ui_NoticeBoard

header_split = chr(1)
list_split_1 = chr(2)
list_split_2 = chr(3)
BUFFER = 50000
FORMAT = "utf-8"


class WidgetNoticeBorad(QMainWindow, Ui_NoticeBoard):

    def __init__(self, client_controller):
        super().__init__()
        self.setupUi(self)
        self.client_controller = client_controller

        # window frame 설정
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        # self.setWindowFlags(Qt.FramelessWindowHint)

        # 버튼 트리거 함수 호출
        self.set_btn_trigger()

    #  widget 이동 함수=======================================================================
    def mousePressEvent(self, event):
        self.client_controller.mousePressEvent(self, event)

    def mouseMoveEvent(self, event):
        self.client_controller.mouseMoveEvent(self, event)

    # set_btn_trigger
    def set_btn_trigger(self):
        self.login_btn.clicked.connect(lambda state: self.click_login_btn())
        self.register_btn.clicked.connect(lambda state: self.click_register_btn())
        self.reg_register_btn.clicked.connect(lambda state: self.click_reg_register_btn())

    # window widget show=======================================================================
    def show(self):
        super().show()

    # 로그인 함수=======================================================================
    def click_login_btn(self):
        user_input_id = self.login_id_edit.text()  # 유저가 입력한 id
        user_input_pw = self.login_pw_edit.text()  # 유저가 입력한 pw

        # 유저가 입력한 로그인 정보 encode
        message = f"{f'login{header_split}{user_input_id}{list_split_1}{user_input_pw}':{BUFFER}}".encode(
            FORMAT)
        self.client_controller.controller_send_message(message)

    # 회원 가입 함수=======================================================================
    # 회원 가입 화면 으로 이동 하는 함수
    def click_register_btn(self):
        self.stackedWidget.setCurrentWidget(self.register_page)
        # 가입 버튼 눌렀을 때 이벤트 발생 시키는 함수

    def click_reg_register_btn(self):
        self.send_duple()
        pass

    def send_duple(self):
        input_reg_id = self.reg_id_edit.text()
        message = f"{f'duple{header_split}{input_reg_id}':{BUFFER}}".encode(
            FORMAT)
        self.client_controller.controller_send_message(message)
