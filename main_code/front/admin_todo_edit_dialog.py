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
        self.set_btn_trigger()
        self.admintodoadd = admintodoadd
        self.title, self.todo_id, self.checked, self.contents, self.cmplt_time, self.user_id = str(title), todo_id, checked, contents, cmplt_time, user_id
        self.todo_title.setText(self.title)
        self.todo_detail.setText(contents)
        self.end_time.setText(cmplt_time)

        if self.checked == 1:
            self.todo_title.setChecked(True)

    def set_btn_trigger(self):
        self.del_btn.clicked.connect(self.del_todo_list)
        self.todo_title.clicked.connect(self.todo_title_clicked)

    def del_todo_list(self):
        self.admintodoadd.admin_del_todo_list_send(self.title)
        self.close()

    def todo_title_clicked(self):
        if self.checked == 1:
            self.checked = 0
            self.end_time.setText('0')
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
        # self.user_name = user_name
        # self.data = DBConnector()
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
        print(self.checkbox_list)

    def style_init(self):
        # 이름 적용 및 폰트 적용
        self.name_lab.setFont(Font.text(2))
        self.admit_btn.setFont(Font.button(3))
        self.cancel_btn.setFont(Font.button(3))

    def event_init(self):
        # 다이얼로그 안에 체크박스가 클릭될때마다 신호보냄
        for i in self.checkbox_list:
            print(i.findChildren())
            # i.checkbox.clicked.connect(self.todo_checked_send)
        # self.findChild
        self.cancel_btn.clicked.connect(self.close)

    def admin_del_todo_list_send(self, todo_title):
        self.main_window.admin_del_todo_list_send2(todo_title)

    def admin_todo_checked_send(self, todo_id, checked):
        self.main_window.admin_todo_checked_send2(todo_id, checked)

    def admin_todo_list_plus(self):
        title = self.todo_title_textedit.toPlainText()
        contents = self.todo_contents_plain.toPlainText()
        self.main_window.admin_todo_list_plus2(title, contents, self.user_id)
        # self.main_window.show_member_todo_list_for_admin3()

        pass

    def test(self, todo_info):
        for todo in todo_info:
            todo_id, title, contents, checked, cplt_time = todo[0], todo[5], todo[2], todo[3], todo[6]
            todo_form = ToDoMiniList(self, todo_id, checked, title, contents, cplt_time, self.user_id)
            self.todo_list_save.append(todo_form)
            self.admin_todo_lay.addWidget(todo_form)



        # print(self.checkbox_list)
        # todo_id, title, contents, checked, cplt_time = todo_info[0], todo_info[1], todo_info[2], todo_info[3], \
        # todo_info[5]
        # todo_form = ToDoMiniList(self, todo_id, checked, title, contents, cplt_time, self.user_id)
        # self.admin_todo_lay.addWidget(todo_form)
        # print('이거 되야되는데')
    # def add_todo_form(self, checked, todo, cplt_time):
    #     todo_form = self.create_todo_form(checked, todo, cplt_time, self.user_id)
    #     # self.checkbox_list.append(todo_form.findChildren(QCheckBox)[0])
    #     self.checkbox_list.append(todo_form)
    #     self.admin_todo_lay.addWidget(todo_form)
    #
    # def create_todo_form(self, checked, todo_, cplt_time, user_id):
    #     """체크박스 폼 만들어주는 함수"""
    #     user_id = user_id
    #     todo_form = QWidget()
    #     layout = QHBoxLayout(todo_form)
    #     layout.setContentsMargins(0, 0, 0, 0)
    #
    #     # 체크박스, 라벨
    #     checkbox = QCheckBox()
    #     checkbox.setMinimumSize(QSize(26, 26))
    #     checkbox.setMaximumSize(QSize(26, 26))
    #     checkbox.setObjectName('checkbox')
    #     if checked == 1:
    #         checkbox.setChecked(True)
    #
    #     todo_label = QLabel()
    #     todo_label.setObjectName('todo_label')
    #     todo_label.setText(todo_)
    #     todo_label.setFont(Font.text(3))
    #     todo_label.setAlignment(Qt.AlignCenter)
    #
    #     time_label = QLabel()
    #     time_label.setText(cplt_time)
    #     time_label.setFont(Font.text(3))
    #     time_label.setObjectName('time_label')
    #     time_label.setAlignment(Qt.AlignCenter)
    #
    #     # 레이아웃에 위젯 추가
    #     layout.addWidget(checkbox)
    #     layout.addWidget(todo_label)
    #     layout.addWidget(time_label)
    #
    #     checkbox.setStyleSheet("""
    #         QCheckBox::indicator {
    #             width: 25px;
    #             height: 25px;
    #         }
    #         QCheckBox::indicator:unchecked {
    #             border: 0.5px solid #14C871;
    #             border-radius: 13px;
    #             background-color: #ffffff;
    #         }
    #         QCheckBox::indicator:checked {
    #             image: url('./src_img/check.png');
    #         }
    #     """)
    #
    #     return todo_form


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # self.todo_list, self.user_id, self.user_name = [['제목', '내용', '1', '시간'], 'admin', '소연']
    # title, contents, checked, cplt_time = ['제목', '내용', '1', '시간']

    todo = AdminTodoAdd('window', ([['id', '제목', '내용', '1', '시간', 'test']], 'admin', '소연'))
    todo.exec()
