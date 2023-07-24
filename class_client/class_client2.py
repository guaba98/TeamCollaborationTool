import datetime
import socket
import time
from threading import *

# 사용할 구분자
header_split = chr(1)
list_split_1 = chr(2)
list_split_2 = chr(3)


class ClientApp2:

    HOST = '127.0.0.12'
    PORT = 9999
    BUFFER = 10000
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

        # 로그인한 유저의 캐릭터 정보 저장
        self.user_character_id = None
        self.user_character_exp = None
        self.user_character_id = None
        self.user_character_hunger = None
        self.user_character_affection = None
        self.user_character_health = None
        self.user_character_exp = None

        #상점 아이템 리스트
        self.shop_items_list = None

        # 클라이언트 recv 스레드
        self.receive_thread = Thread(target=self.receive_message)
        self.receive_thread.daemon = True
        self.receive_thread.start()

    def send_chat_all_clients(self, user_chat):
        msg = user_chat
        client_sand_data = f"{f'send_all_clients{header_split}{msg}':{self.BUFFER}}".encode(self.FORMAT)
        self.client_socket.send(client_sand_data)
    def send_get_shop_item_list(self):
        client_sand_data = f"{f'get_shop_item_list{header_split}':{self.BUFFER}}".encode(
            self.FORMAT)
        self.client_socket.send(client_sand_data)
    def send_get_user_character(self):
        client_sand_data = f"{f'get_user_character{header_split}{self.user_id}':{self.BUFFER}}".encode(
            self.FORMAT)
        self.client_socket.send(client_sand_data)

    def send_get_user_character_stat(self):
        client_sand_data = f"{f'get_user_character_stat{header_split}{self.user_character_id}':{self.BUFFER}}".encode(
            self.FORMAT)
        self.client_socket.send(client_sand_data)

    def send_join_id_and_pw_for_join_access(self, join_username, join_pw, join_nickname):
        client_sand_data = f"{f'join_access{header_split}{join_username}{list_split_1}{join_pw}{list_split_1}{join_nickname}':{self.BUFFER}}".encode(
            self.FORMAT)
        self.client_socket.send(client_sand_data)

    def set_widget(self, widget_):
        self.client_widget = widget_

    def send_username_duplicatecheck(self, join_inp_username):
        client_sand_data = f"{f'assertu_username{header_split}{join_inp_username}':{self.BUFFER}}".encode(self.FORMAT)
        self.client_socket.send(client_sand_data)

    def send_login_id_and_pw_for_login_access(self, login_username, login_pw):
        client_sand_data = f"{f'login{header_split}{login_username}{list_split_1}{login_pw}':{self.BUFFER}}".encode(
            self.FORMAT)
        self.client_socket.send(client_sand_data)

    def receive_message(self):
        while True:
            return_result = self.client_socket.recv(self.BUFFER).decode(self.FORMAT).strip()
            print(return_result.split(header_split), '리스트 확인')
            response_header = return_result.split(header_split)[0]
            response_substance = return_result.split(header_split)[1]

            if response_header == 'assertu_username':
                if response_substance == 'True':
                    self.client_widget.assert_same_id_signal.emit(True)
                else:
                    self.client_widget.assert_same_id_signal.emit(False)

            elif response_header == 'recvallclients':
                msg = response_substance
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
