from PyQt5.QtWidgets import *
from code.front.ui.ui_class_category_list import Ui_CtgWidget
from PyQt5.QtGui import *
'''
카테고리 위젯
'''


class CtgList(QWidget, Ui_CtgWidget):
    """왼쪽 상단 카테고리 리스트 관련 클래스"""
    def __init__(self, img_path, c_name, parent):
        super().__init__()
        self.setupUi(self)
        self.parent = parent
        self.category_name = c_name

        self.img_lab.setPixmap(QPixmap(img_path))
        self.ctg_name_lab.setText(c_name)

    @property
    def c_frame(self):
        """프레임을 리턴합니다."""
        return self.frame

