from PyQt5.QtWidgets import *
from code.front.ui.ui_class_profile_dialog import ProfileDialog
from PyQt5.QtGui import *

'''
프로필 변경 다이얼로그
'''

class CtgList(QWidget, Ui_CtgWidget):
    """왼쪽 상단 카테고리 리스트 관련 클래스"""
    def __init__(self, img_name, c_name, parent):
        super().__init__()
        self.setupUi(self)
        self.parent = parent
        self.category_name = c_name