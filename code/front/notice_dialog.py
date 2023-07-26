from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QIcon
import sys
from code.front.ui.ui_class_notice_dialog import Ui_NoticeDialog

class DialogNoticeAdd(QDialog, Ui_NoticeDialog):
    """공지를 추가하는 창"""
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.connect_event()
        self.set_ui()

    def set_ui(self):
        self.close_btn.setIcon(QIcon('./src_img/close.png'))

    def connect_event(self):
        self.ok_btn.clicked.connect(self.add_notice)
        self.close_btn.clicked.connect(self.close)

    def add_notice(self):
        """여기서 공지를 서버에 넘깁니다."""
        '''
        1. 공지 서버로 전달 -> db 저장
        2. 공지 버티컬 레이아웃에 추가
        '''
        title = self.title_edit.text()
        contents = self.contents_edit.toPlainText()
        print('[notice_dialog] 제목: ', title, '내용', contents)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    notice = DialogNoticeAdd()
    notice.exec()

