from PyQt5.QtWidgets import *
from code.front.ui.ui_class_category_list import Ui_CtgWidget
# from code.front.ui.ui_class_TEST_ctg import Ui_Form
from PyQt5.QtGui import *
import os
'''
카테고리 위젯
'''

class CtgList(QWidget, Ui_CtgWidget):
    """왼쪽 상단 카테고리 리스트 관련 클래스"""
    def __init__(self, img_name, c_name, parent):
        super().__init__()
        self.setupUi(self)
        self.parent = parent
        self.category_name = c_name

        # 현재 실행 파일의 경로
        current_dir = os.path.dirname(os.path.abspath(__file__))
        img_path = os.path.join(current_dir, "", "src_img", f"{img_name}")

        self.img_lab.setPixmap(QPixmap(f"{img_path}"))
        self.ctg_name_lab.setText(c_name)



    def mousePressEvent(self, event):
        print(self.category_name)
        self.parent.ctg_list_trigger(self.category_name)
        # 여기서 이벤트 시그널 연결