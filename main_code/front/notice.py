import sys

from PyQt5.QtWidgets import *
from main_code.front.ui.ui_class_notice_widget import Ui_Notice_widget
from main_code.front.Font import Font


class Notice(QWidget, Ui_Notice_widget):
    def __init__(self, main_window, result, user_role):
        super().__init__()
        self.setupUi(self)
        print(result,'공지 오류')
        self.main_window = main_window
        # title, contents = result[0], result[1]
        if len(result) > 2:
            notice_id, title, contents, cplt_time, checked = result
        else:
             title, contents = result
        self.label.setText(title)
        self.label.setFont(Font.title(3))
        self.detail_lab.setText(contents)
        self.detail_lab.setFont(Font.text(3))
        self.del_btn.clicked.connect(lambda state, title = title: self.close(title))

    def close(self, title):
        self.main_window.del_notice(title)
        super().close()

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     app.setStyle('Fusion')
#     msgbox = Notice('제목','내용')
#     # msgbox.set_dialog_type(bt_cnt=1, t_type='register_cmplt')
#     # msgbox.show_dialog()
#     # msgbox.exec_()
#     msgbox.show()
#     while 1:
#         pass

    # n = Notice('제목','내용')
