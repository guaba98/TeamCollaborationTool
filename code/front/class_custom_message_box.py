from PyQt5.QtWidgets import QMessageBox, QDialog
from PyQt5.QtCore import Qt

from code.front.ui.ui_class_widget_custom_message_box import Ui_custom_message_box

class NoFrameMessageBox(QDialog, Ui_custom_message_box):
    def __init__(self, client_controller, title, contents, dialog_type):
        super().__init__()
        self.setupUi(self)
        self.client_controller = client_controller
        self.title = title
        self.contents = contents
        self.dialog_type = dialog_type
        self.result = None
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.initial_setting()
        self.set_btn_trigger()
        self.exec()

    def mousePressEvent(self, event):
        self.client_controller.mousePressEvent(self, event)

    def mouseMoveEvent(self, event):
        self.client_controller.mouseMoveEvent(self, event)

    def initial_setting(self):
        self.label_title.setText(self.title)
        self.label_contents.setText(self.contents)

        if self.dialog_type == "about":
            self.btn_no.hide()

    def set_btn_trigger(self):
        self.btn_yes.clicked.connect(lambda state: self.answered(True))
        self.btn_no.clicked.connect(lambda state: self.answered(False))

    def answered(self, boolean_answer: bool):
        self.result = boolean_answer
        self.close()

