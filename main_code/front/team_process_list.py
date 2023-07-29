from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QIcon
import sys
from main_code.front.ui.ui_class_admin_todo_check import Ui_MemberWidget
from main_code.front.Font import Font


class MemberList(QWidget, Ui_MemberWidget):
    """관리자 창에서 멤버들을 보여주는 창"""

    def __init__(self, main_window, user_info):
        super().__init__()
        self.setupUi(self)
        self.user_no, self.user_id, self.user_pw, self.name, self.role, self.message, self.date, self.team = user_info
        self.main_window = main_window

        # 화면 설정
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.connect_event()
        self.set_ui()

    def connect_event(self):
        self.show_btn.clicked.connect(self.clicked_memeber)

    def set_ui(self):
        self.name_lab.setText(self.name)  # 값 넣어주기
        self.role_lab.setText(self.team)

        # 폰트 지정
        self.name_lab.setFont(Font.text(1))
        self.role_lab.setFont(Font.text(1))

    def clicked_memeber(self):
        """여기서 멤버 다이얼로그를 보여줍니다."""
        self.main_window.show_member_todo_list_for_admin(self.user_id, self.user_no, self.name)
