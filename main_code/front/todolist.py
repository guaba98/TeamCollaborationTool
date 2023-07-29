import sys
import os
from PyQt5.QtWidgets import *

from main_code.front.ui.ui_class_todo_list import Ui_TodoForm
from main_code.front.Font import Font


class TodoList(QWidget, Ui_TodoForm):
    def __init__(self, main_window, result, people_lab, user_role):
        super().__init__()
        self.setupUi(self)
        self.main_window = main_window
        self.user_role = user_role
        self.todo_id, self.todo, todo_list, checked, time, cplt_time = result
        people_lab = people_lab
        self.init_ui()
        self.set_btn_trigger()

        #

        # 관리자인지 확인
        if '관리자' in self.user_role:
            self.del_btn.show()
        else:
            self.del_btn.hide()

        if people_lab != None:
            self.people_lab.setText('함께하는 사람들 ' + ','.join(people_lab))
        self.label.setText(todo_list)
        self.checkBox.setText(self.todo)
        self.set_checked(checked)

    def init_ui(self):
        self.people_lab.setFont(Font.contents(4))
        self.label.setFont(Font.contents(4))
        self.checkBox.setFont(Font.button(6))
        self.checkBox.setText(self.todo)
        self.checkBox.setFont(Font.button(6))

        # # 경로 얻기
        # current_dir = os.path.dirname(os.path.abspath(__file__))
        # # parent_dir = os.path.dirname(current_dir) # 상위 폴더 경로
        # src_img_dir = os.path.join(current_dir, "src_img") # 이미지 폴더 경로
        # file_path = os.path.join(src_img_dir, "check.png") # 체크 이미지 경로
        #
        #
        # print(file_path)
        # self.checkBox.setStyleSheet("""
        #             QCheckBox::indicator {
        #                 width: 25px;
        #                 height: 25px;
        #             }
        #             QCheckBox::indicator:unchecked {
        #                 border: 0.5px solid #14C871;
        #                 border-radius: 13px;
        #                 background-color: #ffffff;
        #             }
        #             QCheckBox::indicator:checked {
        #                 image: url('');
        #
        #             }
        #         """)
        # self.checkBox.setStyleSheet(
        #     self.checkBox.styleSheet() +
        #     f"""
        #             QCheckBox::indicator:checked {{
        #                 image: url({file_path});
        #             }}
        #             """
        # )
        #
        # self.checkBox.setStyleSheet("""
        #             QCheckBox::indicator {
        #                 width: 25px;
        #                 height: 25px;
        #             }
        #             QCheckBox::indicator:unchecked {
        #                 border: 0.5px solid #14C871;
        #                 border-radius: 13px;
        #                 background-color: #ffffff;
        #             }
        #             QCheckBox::indicator:checked {
        #                 image: url('');
        #             }
        #         """)
        #
        #
        # self.checkBox.setStyleSheet(
        #     self.checkBox.styleSheet() +
        #     f"""
        #             QCheckBox::indicator:checked {{
        #                 image: url({file_path});
        #             }}
        #             """
        # )

    def set_checked(self, checked):
        if checked == 1:
            self.checkBox.setChecked(True)
        else:
            self.checkBox.setChecked(False)

    #     if checked
    def set_btn_trigger(self):
        self.checkBox.clicked.connect(self.todo_list_checked_return)

    def todo_list_checked_return(self):
        btn_checked = self.checkBox.isChecked()
        if btn_checked:
            btn_checked = 1
        else:
            btn_checked = 0

        self.main_window.send_todo_list_checked(self.todo_id, btn_checked)
