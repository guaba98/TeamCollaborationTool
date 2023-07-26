import sys

from PyQt5.QtWidgets import *
from main_code.front.ui.ui_class_notice_widget import Ui_Notice_widget
from main_code.front.Font import Font


class Notice(QWidget, Ui_Notice_widget):
    def __init__(self, result, user_role):
        super().__init__()
        self.setupUi(self)
        # title, contents = result[0], result[1]
        title, contents = result
        print(title, contents)
        self.label.setText(title)
        self.label.setFont(Font.title(3))
        self.detail_lab.setText(contents)
        self.detail_lab.setFont(Font.text(3))
        self.del_btn.clicked.connect(lambda state: self.close())

    def close(self):
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
