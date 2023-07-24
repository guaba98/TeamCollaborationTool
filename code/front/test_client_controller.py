# import sqlite3
# import sys
# from socket import *
# from threading import *
#
# from roll_client import Client
# from fun_login import LogIn
# from main_display import MainDisplay
# from func_chat import ChatDialog
# from class_blue import ClassBlueInfo
# from admin_chat import AdminChat
# from pw_dialog import PwChange
# from car_dialog import CarChange
# from PyQt5.QtWidgets import *
# from PyQt5.QtGui import *
# from PyQt5.QtCore import *
#
# header_split = chr(1)
# list_split_1 = chr(2)
# list_split_2 = chr(3)
# BUFFER = 50000
# FORMAT = "utf-8"
#
# class Controller(QWidget):
#     JoinSignal = pyqtSignal(str)
#     ChangeSignal = pyqtSignal(bool)
#     LoginSignal = pyqtSignal(bool)
#     ChatOpenSignal = pyqtSignal(str)
#     def __init__(self):
#         super().__init__()
#         self.duple_check = None
#         self.client_object = Client(self)
#         self.login_object = LogIn(self)
#         self.main_object = MainDisplay(self)
#         self.chat_object = ChatDialog(self)
#         self.blue_object = ClassBlueInfo(controller = self)
#         self.admin_object = AdminChat(self)
#         self.pwchange_object = PwChange(self)
#         self.carchange_object = CarChange(self)
#         self.init_var()
#         self.init_ui()
#         self.init_func()
#
#
#     def init_ui(self):
#         pass
#
#     def init_func(self):
#         self.JoinSignal.connect(self.emit_login_object)
#         self.ChangeSignal.connect(self.emit_login_object_duple_status)
#
#     def init_var(self):
#         pass
#
#     def send_message(self, message):
#         print(message)
#         self.client_object.send_message(message)
#
#     def emit_login_object(self, message):
#         self.login_object.AlertSignal.emit(message)
#
#     def emit_login_object_duple_status(self):
#         self.login_object.ChangeDuple.emit(True)
#
#     def emit_login_object_login(self, result):
#         self.login_object.LoginSignal.emit(result)
#
#     def emit_add_msg(self, target, txt):
#         """
#         target is admin or member
#         """
#         self.chat_object.AddMsg.emit(target, txt)
#         self.admin_object.AddMsg.emit(target, txt)
#
#     def open_main_display(self):
#         self.main_object.show()
#
#     def emit_blue_info(self, data):
#         self.main_object.blueSignal.emit(data)
#
#     def emit_set_center_name(self, name):
#         self.main_object.CenterNameSignal.emit(name)
#
#     def emit_alert_reserve_duple(self, message):
#         self.main_object.AlertReserveDuple.emit(message)
#
#     def emit_change_status_reserve(self):
#         self.main_object.StatusReserve.emit()
#
#     def emit_set_reserve_check_page(self, list_):
#         self.main_object.ReserveCheck.emit(list_)
#
#     def emit_check_reserve_duple(self, result):
#         self.main_object.CheckReserveDuple.emit(result)
#
#     def emit_mypage_data(self):
#         self.main_object.MypageSignal.emit()
#
#     def emit_open_pw_change(self):
#         self.pwchange_object.exec()
#
#     def emit_open_car_change(self):
#         self.carchange_object.exec()
#
#
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     mywin = Controller()
#     mywin.login_object.show()
#     app.exec()
