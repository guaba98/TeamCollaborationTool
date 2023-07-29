from PyQt5.QtWidgets import *
from main_code.front.ui.ui_class_message_label_left import Ui_LeftMessage
from main_code.front.ui.ui_class_message_label_right import Ui_RightMessage
from main_code.front.Font import Font

'''
나의 메세지, 상대방 메세지
'''


class YourMsg(QWidget, Ui_LeftMessage):
    """상대방 메세지가 담기는 클래스입니다."""

    def __init__(self, name, msg):
        super().__init__()
        self.setupUi(self)
        self.label.setText(f'{name}: {msg}')
        self.label.setFont(Font.text(2))


class MyMsg(QWidget, Ui_RightMessage):
    """상대방 메세지가 담기는 클래스입니다."""

    def __init__(self, name, msg):
        super().__init__()
        self.setupUi(self)
        self.label.setText(f'{name}: {msg}')
        self.label.setFont(Font.text(2))
