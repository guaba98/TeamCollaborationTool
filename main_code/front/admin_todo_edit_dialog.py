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
관리자가 개인별 투두리스트 조회 및 추가하는 창 

'''


class AdminTodoAdd(QDialog, Ui_AdminTodoDialog):
    def __init__(self, user_id):
        super().__init__()
        self.setupUi(self)
        self.user_id = user_id
        self.data = DBConnector()
        self.event_init()  # 버튼 연결 이벤트
        self.table_init()  # 투두리스트 값 넣어주기
        self.style_init()  # 값 넣어주기



    def table_init(self):
        # user id를 username으로 변경시켜준다.
        # user id를 참조해서 todolist를 가져온다.
        condition = f"\"USER_ID\" = '{self.user_id}'"
        user_name = self.data.return_specific_data(column='USER_NAME', table_name='TB_USER', condition=condition)
        user_no = self.data.return_specific_data(column='USER_NO', table_name='TB_USER', condition=condition)
        print(user_name, user_no)

        # 이름 넣어주기
        self.name_lab.setText(user_name)

        # TODO DB에서 시간값 가져와야 함
        todo_list_ = self.data.get_todo_list(user_no)
        print('투두리스트====')
        print(todo_list_)
        for todo in todo_list_:
            print(todo)
            title, contents, checked, todo_time = todo[1], todo[2], todo[3], todo[4]
            self.add_todo_form(checked, contents, todo_time)

    def style_init(self):
        # 이름 적용 및 폰트 적용
        self.name_lab.setFont(Font.text(2))
        self.admit_btn.setFont(Font.button(3))
        self.cancel_btn.setFont(Font.button(3))

    def event_init(self):
        self.cancel_btn.clicked.connect(self.close)
        self.admit_btn.clicked.connect(self.save_todo)
        self.pushButton.clicked.connect(
            lambda x: self.add_todo_form(0, self.lineEdit.text(), ""))  # 추가 버튼 클릭했을 때 -> 0(완료안함, 해야할 일, 날짜)

    # TODO 여기에서 서버 DB로 넘기는 부분 추가해야 함
    def save_todo(self):
        """
        확인 버튼을 누르면 투두리스트 값이
        :return: result : 결과값을 튜플로 각각 묶어 리스트 형태로 출력합니다.
        """
        check = list()
        todo_ = list()
        time = list()
        widget = self.scrollArea.findChildren(QWidget)
        checkbox = self.scrollArea.findChildren(QCheckBox)

        # 체크박스
        for c in checkbox:
            istate = 1 if c.isChecked() else 0
            check.append(istate)

        # 할일과 시간
        for w in widget:
            label = w.findChildren(QLabel)
            for i in label:
                if 'todo' in i.objectName():
                    todo_.append(i.text())
                elif 'time' in i.objectName():
                    time.append(i.text())
            break

        # 튜플로 묶기
        zipped_tuples = zip(check, todo_, time)  # zip 함수를 사용하여 튜플로 묶기
        result = list(zipped_tuples)  # zip 객체를 리스트로 변환하여 결과 확인
        # 결과값 리턴
        print(result)

    def add_todo_form(self, checked, todo, time):
        todo_form = self.create_todo_form(checked, todo, time)
        self.admin_todo_lay.addWidget(todo_form)

    def create_todo_form(self, checked, todo, time):
        """체크박스 폼 만들어주는 함수"""
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
        todo_label.setFont(Font.text(3))
        todo_label.setAlignment(Qt.AlignCenter)

        time_label = QLabel()
        time_label.setText(time)
        time_label.setFont(Font.text(3))
        time_label.setObjectName('time_label')
        time_label.setAlignment(Qt.AlignCenter)

        # Add widgets to layout
        layout.addWidget(checkbox)
        layout.addWidget(todo_label)
        layout.addWidget(time_label)

        checkbox.setStyleSheet("""
            QCheckBox::indicator {
                width: 25px;
                height: 25px;
            }
            QCheckBox::indicator:unchecked {
                border: 0.5px solid #14C871;
                border-radius: 13px;
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
