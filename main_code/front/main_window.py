# 모듈
import json
import sys
from PyQt5.QtWidgets import QMainWindow, QLayout, QLabel, QPushButton, QLineEdit, QTextEdit, QGraphicsDropShadowEffect, QApplication
from PyQt5.QtCore import Qt, pyqtSignal, QSize, QTimer
from PyQt5.QtGui import QFontDatabase, QIcon, QColor, QPixmap

# UI
from main_code.front.message import YourMsg, MyMsg  # 메세지
# from main_code.front.client_controller import ClientController
from main_code.front.ui.ui_class_notice_board import Ui_NoticeBoard  # 메인 화면
from main_code.front.profile_widget import ProFile  # 프로필 변경
from main_code.front.category_list import CtgList  # 카테고리 리스트
from main_code.front.Warning_dialog import DialogWarning  # 경고창
from main_code.front.Font import Font  # 폰트 클래스
from main_code.front.notice import Notice  # 공지 캐러셀
from main_code.front.todolist import TodoList  # 투두리스트 캐러셀
from main_code.front.notice_dialog import DialogNoticeAdd, DialogToDoAdd  # 공지 다이얼로그, 투두리스트 다이얼로그

header_split = chr(1)
list_split_1 = chr(2)
list_split_2 = chr(3)
BUFFER = 50000
FORMAT = "utf-8"


class WidgetNoticeBorad(QMainWindow, Ui_NoticeBoard):
    reg_id_lab_signal = pyqtSignal(bool)
    recv_emit_insertuser = pyqtSignal(bool)
    emit_signal_my_chat = pyqtSignal(list)
    emit_signal_chat = pyqtSignal(list)
    recv_login_signal = pyqtSignal(bool)
    recv_get_notice_signal = pyqtSignal(list)
    recv_get_todolist_signal = pyqtSignal(list)
    refresh_todolist_signal = pyqtSignal()
    refresh_notice_signal = pyqtSignal()

    def __init__(self, client_controller):
        super().__init__()

        self.ctg_clicked = None
        self.user_role = None  # 로그인한 유저의 역할

        self.setupUi(self)
        self.client_controller = client_controller
        self.Warn = DialogWarning()
        self.font = Font()

        self.Notice_add = DialogNoticeAdd(self)
        self.Todo_add = DialogToDoAdd(self)

        # window frame 설정
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setWindowFlags(Qt.FramelessWindowHint)
        # 변수
        self.init_var()

        # 버튼 트리거 함수 호출
        self.set_btn_trigger()
        self.init_func()


    # 변수
    def init_var(self):
        self.ctg_clicked = None  # 카테고리 버튼 클릭 확인(공지, 투두리스트)
        self.update_timer = QTimer(self)
        self.update_timer.setInterval(10)
        self.vsb = self.chat_scrollarea.verticalScrollBar()

    # widget 이동 함수=======================================================================
    def mousePressEvent(self, event):
        self.client_controller.mousePressEvent(self, event)

    def mouseMoveEvent(self, event):
        self.client_controller.mouseMoveEvent(self, event)

    # 시그널======================================================================
    def init_func(self):
        """클라이언트 - 서버 받는 시그널"""
        self.reg_id_lab_signal.connect(self.set_reg_id_lab)
        self.recv_emit_insertuser.connect(self.insertuser)
        self.emit_signal_my_chat.connect(self.recv_my_chat)
        self.emit_signal_chat.connect(self.recv_chat)
        self.recv_login_signal.connect(self.login)
        self.recv_get_notice_signal.connect(self.set_notice)
        self.recv_get_todolist_signal.connect(self.set_todolist)
        self.refresh_todolist_signal.connect(self.get_todolist)
        self.refresh_notice_signal.connect(self.get_notice)
        self.update_timer.timeout.connect(self.set_scrollbar)
        self.update_timer.start()

    def set_scrollbar(self):
        if self.vsb.value() != self.vsb.maximum():
            self.vsb.setValue(self.vsb.maximum())

    def set_btn_trigger(self):
        """UI 버튼 시그널 연결"""

        self.login_btn.clicked.connect(lambda state: self.click_login_btn())  # 로긴 버튼
        self.register_btn.clicked.connect(lambda state: self.click_register_btn())  # 회원가입 화면 이동 버튼
        self.reg_register_btn.clicked.connect(lambda state: self.click_reg_register_btn())  # 회원가입 버튼
        self.send_btn.clicked.connect(lambda state: self.click_send_btn())  # 채팅 전송 버튼
        self.chat_edit.returnPressed.connect(self.click_send_btn)
        self.plus_button.clicked.connect(lambda state: self.click_plus_button())

    def set_font(self):
        """기본 폰트 적용하는 부분"""
        # 로그인 창
        self.login_title_lab.setFont(Font.title(1))
        self.login_id_lab.setFont(Font.text(3))
        self.login_pw_lab.setFont(Font.text(3))
        self.login_id_edit.setFont(Font.text(3, False))
        self.login_pw_edit.setFont(Font.text(3, False))
        self.login_btn.setFont(Font.button(2))
        self.register_btn.setFont(Font.button(2))

        # 회원가입 창
        reg_lab = self.register_page.findChildren(QLabel)
        reg_edit = self.register_page.findChildren(QLineEdit)
        [lab.setFont(Font.text(3)) for lab in reg_lab]
        [edit.setFont(Font.text(3, False)) for edit in reg_edit]
        self.reg_title_lab.setFont(Font.title(1))
        self.reg_sub_title.setFont(Font.text(3))
        self.reg_register_btn.setFont(Font.button(1))

        # -- 메인창
        # 프로필창
        profile_lab = self.profile_widget.findChildren(QLabel)
        [lab.setFont(Font.text(3)) for lab in profile_lab]

        # 채팅
        self.chat_edit.setFont(Font.text(2))

    def ctg_list_show(self):
        """카테고리 넣어주기"""
        self.ctg_dict = {
            '프로필 수정': ['user.png', None],
            '채팅': ['send_black.png', self.chat_page],
            '공지': ['bell.png', self.notice_page],
            '투두리스트': ['heart.png', self.notice_page]
        }
        self.ctg_list = list(self.ctg_dict.keys())
        self.event_dict = {'채팅': [None, self.get_chat, self.plus_button.hide],
                           '공지': [self.notice_v_lay, self.get_notice, self.plus_button.hide],
                           '투두리스트': [self.notice_v_lay, self.get_todolist, self.plus_button.show],
                           '....': [self.team_mem_v_lay, self.plus_button.hide ]
                           }

        for ctg in self.ctg_list:  # 카테고리 이미지, 카테고리 이름 넣어주기
            img_name = self.ctg_dict[ctg][0]
            ctg_ = CtgList(img_name=img_name, c_name=ctg, parent=self, role= self.user_role)
            self.category_v_lay.addWidget(ctg_)
    def admin_ctg_list_show(self):
        """카테고리 넣어주기"""
        self.admin_ctg_dict = {
            '프로필 수정': ['user.png', None],
            '채팅': ['send_black.png', self.chat_page],
            '공지': ['bell.png', self.notice_page],
        }

        self.admin_ctg_list = list(self.admin_ctg_dict.keys())
        self.adminevent_dict = {'채팅': [None, self.get_chat, self.plus_button.hide],
                           '공지': [self.notice_v_lay, self.get_notice, self.plus_button.show],
                           '투두리스트': [self.notice_v_lay, self.get_todolist, self.plus_button.show],
                           '....': [self.team_mem_v_lay, self.plus_button.hide ]
                           }

        for ctg in self.admin_ctg_list:  # 카테고리 이미지, 카테고리 이름 넣어주기
            img_name = self.admin_ctg_dict[ctg][0]
            ctg_ = CtgList(img_name=img_name, c_name=ctg, parent=self, role= self.user_role)
            self.category_v_lay.addWidget(ctg_)

    def click_plus_button(self):
        actions = {
            '공지': self.Notice_add.exec_,
            '투두리스트': self.Todo_add.exec_
        }
        action = actions.get(self.ctg_clicked)
        if action:
            action()

    def ctg_list_trigger(self, ctg_name):
        """카테고리에 따라 페이지 변경 혹은 창 띄우기"""
        name = self.client_controller.client_app.user_name
        state = self.client_controller.client_app.user_message
        self.ctg_clicked = ctg_name
        print('카테고리 클릭', self.ctg_clicked)
        for c in self.ctg_list:
            if ctg_name == '프로필 수정':
                img_path = 'user_green.png'
                p_ = ProFile(self, img=img_path, name=name, state=state)
                p_.show_dialog()
                break
            elif ctg_name == c:
                self.clear_layout(self.event_dict[ctg_name][0])  # 레이아웃 비우기
                self.event_dict[ctg_name][1]()
                self.event_dict[ctg_name][2]()
                self.inner_stackedWidget.setCurrentWidget(self.ctg_dict[c][1])
    def admin_ctg_list_trigger(self, ctg_name):
        """카테고리에 따라 페이지 변경 혹은 창 띄우기"""
        name = self.client_controller.client_app.user_name
        state = self.client_controller.client_app.user_message
        self.ctg_clicked = ctg_name
        print('어드민 카테고리 클릭', self.ctg_clicked)
        print(self.admin_ctg_list)
        for c in self.admin_ctg_list:
            if ctg_name == '프로필 수정':
                p_ = ProFile(self, img=None, name=name, state=state)
                p_.show_dialog()
                break
            elif ctg_name == '채팅':
                self.inner_stackedWidget.setCurrentWidget(self.admin_ctg_dict[c][1])

            elif ctg_name == c:
                print('1')
                self.clear_layout(self.event_dict[ctg_name][0])  # 레이아웃 비우기
                print('2')
                self.event_dict[ctg_name][1]()
                print('3')
                self.event_dict[ctg_name][2]()
                print('4')
                self.inner_stackedWidget.setCurrentWidget(self.admin_ctg_dict[c][1])

    # 유저 프로필 상메 업데이트
    def update_user_message(self, user_message):
        message = f"{f'update_user_message{header_split}{self.client_controller.client_app.user_no}{list_split_1}{user_message}':{BUFFER}}".encode(
            FORMAT)
        self.client_controller.controller_send_message(message)

    # 레이아웃 비우기
    def clear_layout(self, layout: QLayout):
        """레이아웃 안의 모든 객체를 지웁니다."""
        if layout == None:
            pass
        else:
            if layout is None or not layout.count():
                return
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()

                if widget is not None:
                    widget.setParent(None)
                # 아이템이 레이아웃일 경우 재귀 호출로 레이아웃 내의 위젯 삭제
                else:
                    self.clear_layout(item.layout())

    # 투루리스트==========================================
    def insert_todo_list(self, title, contents):
        msg = title, contents, self.client_controller.client_app.team_no
        print(msg)
        message = f"{f'insert_todo{header_split}{msg}':{BUFFER}}".encode(
            FORMAT)
        self.client_controller.controller_send_message(message)

    def get_todolist(self):
        # 유저가 입력한 로그인 정보 encode
        print('투드리스트 클릭')
        self.clear_layout(self.notice_v_lay)  # 레이아웃 비우기
        self.client_controller.controller_send_get_todolist()

    def set_todolist(self, result):
        print('투두 내용들 받아오기', result)
        people_lab = result[1]
        for i in result[0]:
            print('[set_notice]', i)
            todo = TodoList(self, i, people_lab, self.user_role)
            self.notice_v_lay.addWidget(todo)
    def send_todo_list_checked(self,todo_id, btn_checked):
        message = f"{f'update_todo_checked{header_split}{todo_id}{list_split_1}{btn_checked}':{BUFFER}}".encode(
            FORMAT)
        self.client_controller.controller_send_message(message)


    # 공지 화면 =====================================================================================
    def insert_notice(self, title, contents):
        msg = title, contents, self.client_controller.client_app.team_no
        print(msg)
        message = f"{f'insert_notice{header_split}{msg}':{BUFFER}}".encode(
            FORMAT)
        self.client_controller.controller_send_message(message)
    def set_notice(self, result):
        print('공지 내용들 받아오기', result)
        for i in result:
            print('[set_notice]', i)
            notice = Notice(i, self.user_role)
            self.notice_v_lay.addWidget(notice)

    # 공지를 db에서 받아오는 함수
    def get_notice(self):
        print('테스트')
        self.clear_layout(self.notice_v_lay)  # 레이아웃 비우기
        # 유저가 입력한 로그인 정보 encode
        message = f"{f'get_notice{header_split}':{BUFFER}}".encode(
            FORMAT)
        self.client_controller.controller_send_message(message)

    # window widget show=======================================================================
    def show(self):
        self.stackedWidget.setCurrentWidget(self.login_page)
        self.inner_stackedWidget.setCurrentWidget(self.chat_page)
        self.set_font()  # 폰트 설정
        self.style_init()
        super().show()

    def style_init(self):
        #  채팅 버튼 넣어주기
        # self.send_btn.setIcon(QIcon('./src_img/send_green.png'))
        # self.send_btn.setIconSize(QSize(35, 35))
        # self.profile_img.setPixmap(QPixmap('./../front/src_img/user_green.png'))

        # 카테고리 바 그림자 넣기
        self.set_background_color(self.category_bar)

    def set_background_color(self, obj):
        effect = QGraphicsDropShadowEffect()
        effect.setColor(QColor(0, 0, 0, 150))
        effect.setBlurRadius(5)
        effect.setOffset(5, 5)  # 객체와 그림자 사이의 거리 또는 변위
        obj.setGraphicsEffect(effect)

    # 채팅 =========================================================================================
    # 전송버튼 클릭시 채팅을 서버에 보내는 함수
    def get_chat(self):
        print('채팅창 열때 실해')

    def click_send_btn(self):

        if len(self.chat_edit.text()) >= 1:
            input_chat = self.chat_edit.text()
            self.chat_edit.clear()  # 채팅바 클리어
            self.client_controller.controller_send_chat_message(input_chat)  # 입력된 채팅 client_controller에 보내기


    # 서버에서 채팅 메시지 받는 함수
    def recv_my_chat(self, result):  # 본인이 보낸 메시지라면
        user_no, team_no, name, chat = result
        message_widget = MyMsg(name, chat)
        self.chat_v_lay.addWidget(message_widget)

    def recv_chat(self, result):  # 다른 사람이 보낸 메시지라면
        user_no, team_no, name, chat = result
        message_widget = YourMsg(name, chat)
        self.chat_v_lay.addWidget(message_widget)

    # 채팅방 입장시 db에 저장된 채팅 요청
    def send_det_chat(self):
        message = f"{f'get_chat{header_split}{user_input_id}':{BUFFER}}".encode(FORMAT)
        self.client_controller.controller_send_message(message)

    # 로그인 함수=======================================================================
    def click_login_btn(self):
        # test test
        self.Warn.set_dialog_type(bt_cnt=1, t_type='login_cmplt')
        self.Warn.exec_()
        user_input_id = self.login_id_edit.text()  # 유저가 입력한 id
        user_input_pw = self.login_pw_edit.text()  # 유저가 입력한 pw

        # 유저가 입력한 로그인 정보 encode
        message = f"{f'login{header_split}{user_input_id}{list_split_1}{user_input_pw}':{BUFFER}}".encode(
            FORMAT)
        self.client_controller.controller_send_message(message)

    # 로그인 결과 알림 및 화면 전환
    def login(self, result):
        self.user_role = self.client_controller.client_app.user_nickname
        if result:
            if '관리자' in self.client_controller.client_app.user_nickname:
                self.admin_ctg_list_show()
            else:
                self.ctg_list_show()  # 카테고리 넣어주기

            self.Warn.set_dialog_type(bt_cnt=1, t_type='loginSuccessfully')  # 알림창 띄우기
            self.user_role = self.client_controller.client_app.user_nickname
            # self.login_user_role(user_role)
            self.stackedWidget.setCurrentWidget(self.main_page)  # 화면전환
        else:
            self.Warn.set_dialog_type(bt_cnt=1, t_type='loginfailed')  # 알림창 띄우기

    # 회원 가입 함수=======================================================================

    def insertuser(self, result):
        if result:
            self.Warn.set_dialog_type(bt_cnt=1, t_type='register_cmplt')
            self.Warn.show_dialog()
            print('회원가입 성공')
        else:
            self.Warn.set_dialog_type(bt_cnt=1, text='회원가입 실패')
            self.Warn.show_dialog()
            print('회원가입 실패')

    # 회원 가입 화면 으로 이동 하는 함수
    def click_register_btn(self):
        self.stackedWidget.setCurrentWidget(self.register_page)

    # 아이디 중복 검사
    def click_reg_register_btn(self):
        self.send_duple()

    # 아이디 중복검사후 pw name nickname 검사
    def click_reg_register_btn2(self):
        if self.register_check():
            self.register_user()

    # 유저가 입력한 아이디 server에 보내서 중복확인
    def send_duple(self):
        input_reg_id = self.reg_id_edit.text()
        message = f"{f'duple{header_split}{input_reg_id}':{BUFFER}}".encode(
            FORMAT)
        self.client_controller.controller_send_message(message)

    # 조건 충족 회원가입 진행
    def register_user(self):
        input_reg_id = self.reg_id_edit.text()
        input_reg_pw = self.reg_pw_edit.text()
        input_reg_name = self.reg_name_edit.text()
        input_reg_nn = self.reg_nn_edit.text()
        result = [input_reg_id, input_reg_pw, input_reg_name, input_reg_nn]

        user_info = json.dumps(result)
        message = f"{f'insertuser{header_split}{user_info}'}"
        self.client_controller.controller_send_json_message(message)

    # 아이디 중복검사 결과에따른 이벤트
    def set_reg_id_lab(self, result):
        if result is True:
            self.reg_id_lab.setText('ID 사용가능')
            self.reg_id_lab.setStyleSheet('color:blue;')
            self.click_reg_register_btn2()
        else:
            self.reg_id_lab.setText('ID 사용불가')
            self.reg_id_lab.setStyleSheet('color:red;')

    def set_reg_name_lab(self):
        self.reg_name_lab.setText('이름은 두 글자 이상이여야 합니다.')
        self.reg_id_lab.setStyleSheet('color:red;')

    def set_reg_nn_lab(self):
        self.reg_nn_lab.setText('닉네임은 두 글자 이상이여야 합니다.')
        self.reg_id_lab.setStyleSheet('color:red;')

    def set_reg_pw_lab(self):
        self.reg_pw_lab.setText('비밀번호가 같지 않습니다.')
        self.reg_id_lab.setStyleSheet('color:red;')

    # 유저가 입력한 회원가입조건 검사
    def register_check(self):
        self.reg_name_lab.setText('이름')
        self.reg_nn_lab.setText('닉네임')
        self.reg_pw_lab.setText('비밀번호')

        if len(self.reg_name_edit.text()) < 2:
            self.set_reg_name_lab()
            return False

        if len(self.reg_nn_edit.text()) < 2:
            self.set_reg_nn_lab()
            return False

        if self.reg_pw_edit.text() != self.reg_pw_check_edit.text():
            self.set_reg_pw_lab()
            return False

        if self.reg_id_lab.text() != 'ID 사용가능':
            return False
        return True

    def log_out(self):
        """로그아웃 함수"""
        self.user_role = None
        self.stackedWidget.setCurrentWidget(self.login_page)
