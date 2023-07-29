from PyQt5.Qt import QSize
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import os
import sys
from main_code.front.ui.ui_class_admin_todo_edit_dialog import Ui_AdminTodoDialog
from main_code.front.ui.ui_class_todo_list_widget_for_admin_dialog import Ui_TodoList
# from main_code.domain.class_db_connector import DBConnector
from main_code.front.Font import Font
from datetime import datetime

'''
관리자가 개인별 투두리스트 조회 및 추가하는 창 

'''


class ToDoMiniList(QWidget, Ui_TodoList):
    def __init__(self, admintodoadd, todo_id, checked, title, contents, cmplt_time, user_id):
        super().__init__()
        self.setupUi(self)
        self.ui_init()
        self.set_btn_trigger()
        self.admintodoadd = admintodoadd
        self.title, self.todo_id, self.checked, self.contents, self.cmplt_time, self.user_id = str(
            title), todo_id, checked, contents, cmplt_time, user_id
        self.todo_title.setText(self.title)
        self.todo_detail.setText(contents)

        if cmplt_time == '0':
            self.end_time.setText('')
        else:
            self.end_time.setText(cmplt_time)

        if self.checked == 1:
            self.todo_title.setChecked(True)

    def ui_init(self):
        self.todo_title.setFont(Font.button(1))
        self.end_time.setFont(Font.text(4))
        self.todo_detail.setFont(Font.text(4))

    def set_btn_trigger(self):
        self.del_btn.clicked.connect(self.del_todo_list)
        self.todo_title.clicked.connect(self.todo_title_clicked)

    def del_todo_list(self):
        self.admintodoadd.admin_del_todo_list_send(self.title)
        self.close()

    def todo_title_clicked(self):
        if self.checked == 1:
            self.checked = 0
            self.end_time.setText('')
        elif self.checked == 0:
            now = datetime.now()  # 시간
            now_format = now.strftime("%Y-%m-%d %H:%M:%S")  # 년 월 일 시 분 초
            self.end_time.setText(now_format)
            self.checked = 1

        self.admintodoadd.admin_todo_checked_send(self.todo_id, self.checked)


class AdminTodoAdd(QDialog, Ui_AdminTodoDialog):
    def __init__(self, main_window, info):
        super().__init__()
        self.setupUi(self)
        self.todo_list_save = []
        self.main_window = main_window
        self.todo_list, self.user_id, self.user_name = info
        self.checkbox_list = []
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.table_init()  # 투두리스트 값 넣어주기
        self.style_init()  # 값 넣어주기
        self.event_init()  # 버튼 연결 이벤트
        # 체크 박스 리스트

    def table_init(self):
        self.name_lab.setText(self.user_name)
        for todo in self.todo_list:
            todo_id, title, contents, checked, cplt_time = todo[0], todo[1], todo[2], todo[3], todo[5]
            todo_form = ToDoMiniList(self, todo_id, checked, title, contents, cplt_time, self.user_id)
            self.todo_list_save.append(todo_form)
            self.admin_todo_lay.addWidget(todo_form)
        self.pushButton.clicked.connect(self.admin_todo_list_plus)

    def style_init(self):
        # 이름 적용 및 폰트 적용
        self.name_lab.setFont(Font.text(2))
        self.admit_btn.setFont(Font.button(3))
        self.cancel_btn.setFont(Font.button(3))
        self.todo_add_title_lab.setFont(Font.title(5))
        self.todo_title_lab.setFont(Font.text(4, t_blod=False))
        self.todo_contents_lab.setFont(Font.text(4, t_blod=False))

    def event_init(self):
        # 다이얼로그 안에 체크박스가 클릭될때마다 신호보냄
        self.cancel_btn.clicked.connect(self.close)
        self.admit_btn.clicked.connect(self.close)

        self.cancel_lab.mousePressEvent = lambda event: self.close_window(event)

    def close_window(self, evnet):
        self.close()

    def admin_del_todo_list_send(self, todo_title):
        self.main_window.admin_del_todo_list_send2(todo_title)

    def admin_todo_checked_send(self, todo_id, checked):
        self.main_window.admin_todo_checked_send2(todo_id, checked)

    def admin_todo_list_plus(self):
        title = self.todo_title_textedit.toPlainText()
        contents = self.todo_contents_plain.toPlainText()
        self.main_window.admin_todo_list_plus2(title, contents, self.user_id)

    def test(self, todo_info):
        for todo in todo_info:
            todo_id, title, contents, checked, cplt_time = todo[0], todo[5], todo[2], todo[3], todo[6]
            todo_form = ToDoMiniList(self, todo_id, checked, title, contents, cplt_time, self.user_id)
            self.todo_list_save.append(todo_form)
            self.admin_todo_lay.addWidget(todo_form)
