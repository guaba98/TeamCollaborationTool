from PyQt5.QtWidgets import *
from main_code.front.ui.ui_class_category_list import Ui_CtgWidget
# from main_code.front.ui.ui_class_TEST_ctg import Ui_Form
from main_code.front.Font import Font
from PyQt5.QtGui import *
import os

'''
카테고리 위젯
'''


class CtgList(QWidget, Ui_CtgWidget):
    """왼쪽 상단 카테고리 리스트 관련 클래스"""

    def __init__(self, img_name, c_name, parent, role):
        super().__init__()
        self.setupUi(self)
        self.parent = parent
        self.category_name = c_name
        self.role = role
        # 현재 실행 파일의 경로
        current_dir = os.path.dirname(os.path.abspath(__file__))
        img_path = os.path.join(current_dir, "", "src_img", f"{img_name}")

        self.img_lab.setPixmap(QPixmap(f"{img_path}"))
        self.ctg_name_lab.setText(c_name)
        self.ctg_name_lab.setFont(Font.text(2))

    def mousePressEvent(self, event):
        print(self.category_name, 'zkxprhfl dlfma')
        if self.role == '관리자':
            print(self.role, '직급이?')
            self.parent.admin_ctg_list_trigger(self.category_name)
        else:
            self.parent.ctg_list_trigger(self.category_name)
        # 여기서 이벤트 시그널 연결
