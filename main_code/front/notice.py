import sys

from PyQt5.QtWidgets import *
from main_code.front.ui.ui_class_notice_widget import Ui_Notice_widget
from main_code.front.Font import Font


class Notice(QWidget, Ui_Notice_widget):
    def __init__(self, main_window, result, user_role):
        super().__init__()
        self.setupUi(self)
        self.main_window = main_window
        if len(result) > 2:
            notice_id, title, contents, cplt_time, checked = result
        else:
             title, contents = result
        if '관리자' not in user_role:
            self.del_btn.hide()
        self.label.setText(title)
        self.label.setFont(Font.title(3))
        self.detail_lab.setText(contents)
        self.detail_lab.setFont(Font.text(3))
        self.del_btn.clicked.connect(lambda state, title = title: self.close(title))

    def close(self, title):
        self.main_window.del_notice(title)
        super().close()
