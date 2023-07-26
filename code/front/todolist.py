import sys

from PyQt5.QtWidgets import *

from code.front.ui.ui_class_todo_list import Ui_TodoForm


class TodoList(QWidget, Ui_TodoForm):
    def __init__(self, result):
        super().__init__()
        self.setupUi(self)
        todo , checked, people_lab = result
        # self.checkBox.clicked.connect()
        # self.checkBox.clicked(checked)
        self.checkBox.setText(todo)
        self.people_lab.setText(','.join(people_lab))