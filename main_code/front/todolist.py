import sys

from PyQt5.QtWidgets import *

from main_code.front.ui.ui_class_todo_list import Ui_TodoForm
from main_code.front.Font import Font


class TodoList(QWidget, Ui_TodoForm):
    def __init__(self, main_window, result, people_lab, user_role):
        super().__init__()
        self.setupUi(self)
        self.main_window = main_window
        self.user_role = user_role
        self.todo_id, todo, todo_list, checked, time, cplt_time = result
        people_lab = people_lab
        # self.checkBox.clicked.connect()
        # self.checkBox.clicked(checked)
        if '관리자' in self.user_role:
            self.del_btn.show()
        else:
            self.del_btn.hide()

        if people_lab != None:
            self.people_lab.setText('함께하는 사람들 ' + ','.join(people_lab))
        self.label.setText(todo_list)
        self.checkBox.setText(todo)
        self.checkBox.setFont(Font.button(6))
        self.people_lab.setFont(Font.contents(4))
        self.set_btn_trigger()
        self.set_checked(checked)

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
