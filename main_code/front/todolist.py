import sys

from PyQt5.QtWidgets import *

from main_code.front.ui.ui_class_todo_list import Ui_TodoForm
from main_code.front.Font import Font


class TodoList(QWidget, Ui_TodoForm):
    def __init__(self, main_window, result, people_lab, user_role):
        super().__init__()
        self.setupUi(self)
        self.main_window = main_window
        self.todo_id, todo, checked = result
        people_lab = people_lab
        # self.checkBox.clicked.connect()
        # self.checkBox.clicked(checked)
        self.checkBox.setText(todo)
        self.checkBox.setFont(Font.button(6))
        self.people_lab.setText(','.join(people_lab))
        self.people_lab.setFont(Font.contents(4))
        self.set_btn_trigger()

    def set_btn_trigger(self):
        self.checkBox.clicked.connect(self.todo_list_checked_return)

    def todo_list_checked_return(self):
        btn_checked = self.checkBox.isChecked()
        if btn_checked:
            btn_checked = 1
        else:
            btn_checked = 0

        self.main_window.send_todo_list_checked(self.todo_id ,btn_checked)
