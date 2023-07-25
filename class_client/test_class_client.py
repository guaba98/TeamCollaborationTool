import datetime
import socket
import time
from threading import *

# 사용할 구분자
header_split = chr(1)
list_split_1 = chr(2)
list_split_2 = chr(3)


class TestClientApp:
    HOST = '127.0.0.12'
    PORT = 9999
    BUFFER = 50000
    FORMAT = "utf-8"
    HEADER_LENGTH = 30

    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.HOST, self.PORT))
        self.client_widget = None

        # 로그인한 유저 정보 저장
        self.user_id = None
        self.user_pw = None
        self.username = None
        self.user_nickname = None

        # 클라이언트 recv 스레드
        self.receive_thread = Thread(target=self.receive_message)
        self.receive_thread.daemon = True
        self.receive_thread.start()

    def set_widget(self, widget_):
        self.client_widget = widget_

    def receive_message(self):
        while True:
            try:
                return_result = self.client_socket.recv(self.BUFFER).decode(self.FORMAT).strip()
                print(return_result.split(header_split), '리스트 확인')
                response_header = return_result.split(header_split)[0]
                response_substance = return_result.split(header_split)[1]
            except:
                continue
            if response_header == 'assertu_username':
                if response_substance == 'True':
                    self.client_widget.assert_same_id_signal.emit(True)
                else:
                    self.client_widget.assert_same_id_signal.emit(False)

            elif response_header == 'recvallclients':
                msg = response_substance
                # msg = msg.de
                print(msg, '받는 메시지')
                self.client_widget.recv_message.emit(msg)


            elif response_header == 'login':
                if response_substance == 'False':
                    self.client_widget.log_in_signal.emit(False)
                else:
                    data = response_substance.split(list_split_1)
                    self.user_id, self.username, self.user_pw, self.user_nickname = data
                    self.client_widget.log_in_signal.emit(True)

            elif response_header == 'join_access':
                if response_substance == 'True':
                    self.client_widget.assert_join_signal.emit(True)
                else:
                    self.client_widget.assert_join_signal.emit(False)

            # 상점아이템 목록 받기
            elif response_header == 'recv_shop_item_list':
                response_substance = eval(response_substance)
                self.shop_items_list = response_substance
                self.client_widget.get_item_list_signal.emit(self.shop_items_list)


            elif response_header == 'recv_character_stat':
                response_substance_list = list()
                response_substance = response_substance.split(list_split_1)
                for i in response_substance:
                    response_substance_list.append(int(i))
                self.user_character_id, self.user_character_hunger, self.user_character_affection, self.user_character_health, self.user_character_exp = response_substance_list
                self.client_widget.set_progressBar.emit()

            elif response_header == 'get_user_character':
                self.user_character_id = response_substance
                self.send_get_user_character_stat()
                # if response_substance == 'True':
                #     self.client_widget.assert_join_signal.emit(True)
                # else:
                #     self.client_widget.assert_join_signal.emit(False)
