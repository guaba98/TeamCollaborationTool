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

'''
관리자가 개인별 투두리스트 조회 및 추가하는 창 

'''
class ToDoMiniList(QWidget, Ui_TodoList):
    def __init__(self, id, checked, title, contents, cmplt_time):
        super().__init__()
        self.setupUi(self)
        self.todo_title.setText(title)
        self.todo_detail.setText(contents)
        if checked == 1:
            self.todo_title.setChecked(True)



class AdminTodoAdd(QDialog, Ui_AdminTodoDialog):
    def __init__(self, main_window, info):
        super().__init__()
        self.setupUi(self)

        self.main_window = main_window
        self.todo_list, self.user_id, self.user_name = info
        self.checkbox_list = []

        # self.user_name = user_name
        # self.data = DBConnector()
        self.table_init()  # 투두리스트 값 넣어주기
        self.style_init()  # 값 넣어주기
        self.event_init()  # 버튼 연결 이벤트
        # 체크 박스 리스트
        self.exec_()

    def table_init(self):
        self.name_lab.setText(self.user_name)
        for todo in self.todo_list:
            todo_id, title, contents, checked, cplt_time = todo[0], todo[1], todo[2], todo[3], todo[5]
            ToDoMiniList(todo_id, checked, title, contents, cplt_time)


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

    def todo_checked_send(self):
        print()
        print('암튼 눌림')

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
