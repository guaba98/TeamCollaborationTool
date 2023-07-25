from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QIcon
import sys
from ui.ui_class_Warning_dialog import Ui_WarnDialog


class DialogWarning(QDialog, Ui_WarnDialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.connect_event()
        self.set_ui()

    def on_ok_btn_clicked(self):
        print('예')
        self.close()

    def reject_btn(self):
        print('아니오')
        self.close()

    # 이벤트 연결
    def connect_event(self):
        # 예, 확인 : accept (1)
        # 아니오, 닫기 : reject (0)
        self.ok_btn.clicked.connect(self.on_ok_btn_clicked)
        self.accept_btn.clicked.connect(self.on_ok_btn_clicked)
        self.cancel_btn.clicked.connect(self.reject_btn)
        self.close_btn.clicked.connect(self.close)

    def set_ui(self):
        self.close_btn.setIcon(QIcon('./src_img/close.png'))
        self.close_btn.setIconSize(QSize(35, 35))


    # 다이얼로그 타입 설정
    # bt_cnt : 버튼 수량
    # t_type : 다이얼로그 타입
    def set_dialog_type(self, bt_cnt: int, t_type="", text=""):
        if bt_cnt == 1:
            self.widget_1.setHidden(False)
            self.widget_2.setHidden(True)

        elif bt_cnt == 2:
            self.widget_1.setHidden(True)
            self.widget_2.setHidden(False)

        if text:
            self.warning_lab.setText(text)
        if t_type == 'reject_login':
            self.warning_lab.setText('존재하는 아이디나 비밀번호가 아닙니다.')
        elif t_type == 'used_id':
            self.warning_lab.setText('사용 중인 아이디입니다.')
        elif t_type == 'user_can_use_id':
            self.warning_lab.setText('사용할 수 있는 아이디입니다.')
        elif t_type == 'pw_recheck':
            self.warning_lab.setText('비밀번호가 일치하지 않습니다.\n다시 확인해 주세요.')
        elif t_type == 'used_email':
            self.warning_lab.setText('사용중인 이메일입니다.')
        elif t_type == 'not_valid_email':
            self.warning_lab.setText('유효하지 않은 이메일입니다.')
        elif t_type == 'name_input':
            self.warning_lab.setText('이름을 입력해 주세요.')
        elif t_type == 'email_input':
            self.warning_lab.setText('이메일을 입력해 주세요.')
        elif t_type == 'cell_num_input':
            self.warning_lab.setText('올바른 핸드폰 번호를 입력해 주세요.')
        elif t_type == 'pw_input':
            self.warning_lab.setText('비밀번호를 입력해 주세요.')
        elif t_type == 'unable_chat':
            self.warning_lab.setText('회원만 채팅이 가능합니다.')
        elif t_type == 'register_cmplt':
            self.warning_lab.setText('회원가입이 완료되었습니다.\n로그인 해 주세요!')

    def show_dialog(self):
        self.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    msgbox = DialogWarning()
    msgbox.set_dialog_type(bt_cnt=1, text='테스트입니다.')
    msgbox.show_dialog()

    pass
