# 모듈
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSignal

# UI
# from code.front.client_controller import ClientController
from code.front.ui.ui_class_notice_board import Ui_NoticeBoard


# 클래스
from code.front.category_list import CtgList # 카테고리 리스트

header_split = chr(1)
list_split_1 = chr(2)
list_split_2 = chr(3)
BUFFER = 50000
FORMAT = "utf-8"


class WidgetNoticeBorad(QMainWindow, Ui_NoticeBoard):

    reg_id_lab_signal = pyqtSignal(bool)
    recv_emit_insertuser = pyqtSignal(bool)

    def __init__(self, client_controller):
        super().__init__()
        self.setupUi(self)
        self.client_controller = client_controller

        # window frame 설정
        # self.setAttribute(Qt.WA_TranslucentBackground, True)
        # self.setWindowFlags(Qt.FramelessWindowHint)

        # 버튼 트리거 함수 호출
        self.set_btn_trigger()
        self.init_func()

        # 캐럿셀 테스트 중
        # 1. 카테고리 위젯
        self.stackedWidget.setCurrentWidget(self.register_page)
        img_path = '../front/src_img/bell.png'
        for i in range(10):
            ctg = CtgList(img_path=img_path, c_name='공지', parent=self)
            self.category_v_lay.addWidget(ctg)


    #  widget 이동 함수=======================================================================
    # def mousePressEvent(self, event):
    #     self.client_controller.mousePressEvent(self, event)
    #
    # def mouseMoveEvent(self, event):
    #     self.client_controller.mouseMoveEvent(self, event)

    # 시그날
    def init_func(self):
        self.reg_id_lab_signal.connect(self.set_reg_id_lab)
        self.recv_emit_insertuser.connect(self.insertuser)
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

    def insertuser(self, result):
        if result:
            print('회원가입 성공')
        else:
            print('회원가입 실패')
    # 회원 가입 화면 으로 이동 하는 함수
    def click_register_btn(self):
        self.stackedWidget.setCurrentWidget(self.register_page)

    # 아이디 중복 검사
    def click_reg_register_btn(self):
        self.send_duple()

    # 아이디 중복검사후 pw name nickname 검사
    def click_reg_register_btn2(self):
        if self.register():
            self.register_user()

    def send_duple(self):
        input_reg_id = self.reg_id_edit.text()
        message = f"{f'duple{header_split}{input_reg_id}':{BUFFER}}".encode(
            FORMAT)
        self.client_controller.controller_send_message(message)

    def register_user(self):
        input_reg_id = self.reg_id_edit.text()
        input_reg_pw = self.reg_pw_edit.text()
        input_reg_name = self.reg_name_edit.text()
        input_reg_nn = self.reg_nn_edit.text()
        result =  input_reg_id, input_reg_pw, input_reg_name, input_reg_nn
        print('[widget_notice]-register_user',result)

        user_info = json.dumps(result)
        message = f"{f'insertuser{header_split}{input_reg_id}':{BUFFER}}".encode(
            FORMAT)
        self.client_controller.controller_send_json_message(message)

    def set_reg_id_lab(self, result):
        if result is True:
            self.reg_id_lab.setText('ID 사용가능')
            self.click_reg_register_btn2()
        else:
            self.reg_id_lab.setText('ID 사용불가')

    def set_reg_name_lab(self):
        self.reg_name_lab.setText('이름 정상적으로 적어주세요')


    def set_reg_nn_lab(self):
        self.reg_nn_lab.setText('닉네임 정상적으로 적어주세요')


    def set_reg_pw_lab(self):
        self.reg_pw_lab.setText('비밀번호 다시 확인해주세요')


    def register(self):
        self.reg_name_lab.setText('이름')
        self.reg_nn_lab.setText('닉네임')
        self.reg_pw_lab.setText('비밀번호')

        if len(reg_name_edit) < 2:
            self.set_reg_name_lab()
            return False

        if len(reg_nn_edit) < 2:
            self.set_reg_nn_lab()
            return False

        if self.reg_pw_edit.text() == self.reg_pw_check_edit.text():
            self.set_reg_pw_lab()
            return False

        if self.reg_id_lab.text() != 'ID 사용가능':
            return False

        return True