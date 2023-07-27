from PyQt5.Qt import QSize
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from main_code.front.Font import Font
import os
import sys
from main_code.front.ui.ui_class_admin_todo_edit_dialog import Ui_AdminTodoDialog
from main_code.domain.class_db_connector import DBConnector
from main_code.front.Font import Font

'''
관리자가 개인별 투두리스트 추가하는 창 

'''


class AdminTodoAdd(QDialog, Ui_AdminTodoDialog):
    def __init__(self, user_id):
        super().__init__()
        self.setupUi(self)
        self.data = DBConnector()
        self.event_init() # 버튼 연결 이벤트

        # user id를 username으로 변경시켜준다.
        # user id를 참조해서 todolist를 가져온다.
        condition = f"\"USER_ID\" = '{user_id}'"
        user_name = self.data.return_specific_data(column='USER_NAME', table_name='TB_USER', condition=condition)
        user_no = self.data.return_specific_data(column='USER_NO', table_name='TB_USER', condition=condition)
        print(user_name, user_no)

        # 이름 적용 및 폰트 적용
        self.name_lab.setText(user_name)
        self.name_lab.setFont(Font.text(2))

        # 테스트(이 부분은 DB에서 가져와야 함)
        todo_list_ = self.data.get_todo_list(user_no)
        print(todo_list_)
        for todo in todo_list_:
            title, contents, checked = todo[1], todo[2], todo[3]
            self.add_todo_form(checked, contents, '시간' )



        # 추가 버튼 클릭했을 때 -> 0(완료안함, 해야할 일, 날짜)
        self.pushButton.clicked.connect(lambda x: self.add_todo_form(0, self.lineEdit.text(), ""))



    def event_init(self):
        self.cancel_btn.clicked.connect(self.close)
        self.admit_btn.clicked.connect(self.save_todo)

    # TODO 여기에서 서버 DB로 넘기는 부분 추가해야 함

    # def save_todo(self):
    #     check = list()
    #     todo_ = list()
    #
    #     widget = self.scrollArea.findChildren(QWidget)
    #     checkbox = self.scrollArea.findChildren(QCheckBox)
    #     for c in checkbox:
    #         istate = 1 if c.isChecked() else 0
    #         check.append(istate)
    #
    #     for w in widget:
    #         label = w.findChildren(QLabel)
    #         for i in label:
    #             todo_.append(i.text())
    #         break

    def save_todo(self):
        check_todo_list = []  # 리스트를 담을 변수 초기화
        check = list()
        todo_ = list()
        widget = self.scrollArea.findChildren(QWidget)
        checkbox = self.scrollArea.findChildren(QCheckBox)

        for c in checkbox:
            istate = 1 if c.isChecked() else 0
            check.append(istate)

        for w in widget:
            label = w.findChildren(QLabel)
            for i in label:
                print(i)
                todo_.append(i.text())
            break
        print(todo_)
        # check와 todo_ 값을 묶어서 튜플로 리스트에 추가
        # check와 todo_ 값을 묶어서 튜플로 리스트에 추가

        return check_todo_list

    def add_todo_form(self, checked, todo, time):
        todo_form = self.create_todo_form(checked, todo, time)
        self.admin_todo_lay.addWidget(todo_form)

    def create_todo_form(self, checked, todo, time):
        todo_form = QWidget()
        layout = QHBoxLayout(todo_form)
        layout.setContentsMargins(0, 0, 0, 0)

        # 체크박스, 라벨
        checkbox = QCheckBox()
        checkbox.setMinimumSize(QSize(26, 26))
        checkbox.setMaximumSize(QSize(26, 26))
        checkbox.setObjectName('checkbox')
        if checked == 1:
            checkbox.setChecked(True)

        todo_label = QLabel()
        todo_label.setObjectName('todo_label')
        todo_label.setText(todo)
        todo_label.setAlignment(Qt.AlignCenter)

        time_label = QLabel()
        time_label.setText(time)
        time_label.setObjectName('time_label')
        time_label.setAlignment(Qt.AlignCenter)

        # Add widgets to layout
        layout.addWidget(checkbox)
        layout.addWidget(todo_label)
        layout.addWidget(time_label)

        checkbox.setStyleSheet("""
            QCheckBox::indicator {
                width: 24px;
                height: 24px;
            }
            QCheckBox::indicator:unchecked {
                border: 1px solid #999999;
                border-radius: 12px;
                background-color: #ffffff;
            }
            QCheckBox::indicator:checked {
                image: url('./src_img/check.png');
            }
        """)

        return todo_form


if __name__ == '__main__':
    app = QApplication(sys.argv)
    todo = AdminTodoAdd(user_id='admin')
    todo.exec()

