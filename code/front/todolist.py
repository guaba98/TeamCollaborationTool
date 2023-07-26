import sys

from PyQt5.QtWidgets import *

from code.front.ui.ui_class_todo_list import Ui_TodoForm


class TodoList(QWidget, Ui_TodoForm):
    def __init__(self, result):
        super().__init__()
        self.setupUi(self)

        self.checkBox
        self.detail_lab.setText()
        self.date_lab.setText()
        self.people_lab.setText()