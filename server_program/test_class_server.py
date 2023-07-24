import json
import os
import threading
from multiprocessing import Process
from socket import *
from threading import Thread, Event
# from Common.class_json import *

import select

from code.domain.class_db_connector import DBConnector
# from common.class_json import *

# from Code.domain.class_db_connector import DBConnector
# 사용할 구분자
header_split = chr(1)
list_split_1 = chr(2)
list_split_2 = chr(3)

class Server:
    HOST = '127.0.0.12'
    PORT = 9999
    BUFFER = 50000
    FORMAT = "utf-8"
    HEADER_LENGTH = 30

    def __init__(self, db_conn: DBConnector):
        # 서버 소켓 설정
        self.db_conn = db_conn
        self.server_socket = None
        self.config = None
        self.sockets_list = list()
        self.clients = dict()
        self.thread_for_run = None
        self.run_signal = True
        self.decoder = KKODecoder()
        self.encoder = KKOEncoder()

    def set_config(self, configure):
        self.config = configure
        print('서버 설정 적용됨')

    def start(self):
        if self.thread_for_run is not None:  # 실행중이면 종료 시키기
            return
        self.server_socket = socket(AF_INET, SOCK_STREAM)  # AF_INET(ipv4를 의미)
        self.server_socket.bind((self.HOST, self.PORT))  # 바인딩
        self.server_socket.listen()  # 리슨 시작
        self.sockets_list.clear()  # 소켓리스트 클리어
        self.sockets_list.append(self.server_socket)
        self.run_signal = True
        self.thread_for_run = Thread(target=self.run)
        self.thread_for_run.start()

    def stop(self):
        self.run_signal = False
        if self.thread_for_run is not None:
            self.thread_for_run.join()
        self.server_socket.close()
        self.thread_for_run = None

    def run(self):
        while True:
            if self.run_signal is False:
                break
            try:
                read_sockets, _, exception_sockets = select.select(self.sockets_list, [], self.sockets_list, 0.1)
            except Exception:
                continue

            for notified_socket in read_sockets:
                if notified_socket == self.server_socket:
                    client_socket, client_address = self.server_socket.accept()
                    self.sockets_list.append(client_socket)
                else:
                    message = self.receive_message(notified_socket)
                    if message is False:
                        self.sockets_list.remove(notified_socket)
                        # del self.clients[notified_socket]
                        continue

            for notified_socket in exception_sockets:
                self.sockets_list.remove(notified_socket)
                del self.clients[notified_socket]

    # def send_message(self, client_socket: socket, result):
    #     client_socket.send(result)
    # def sendAllClients(self, msg):
    #     for c in self.clients:
    #         c.sendMsg(msg)
    def receive_message(self, client_socket: socket, UserTalkRoom=None):
        try:
            recv_message = client_socket.recv(self.BUFFER)
            decode_msg = recv_message.decode(self.FORMAT).strip()
            header = decode_msg.split(header_split)[0]
            substance = decode_msg.split(header_split)[1]

            if header == 'login':  # 로그인
                data = substance.split(list_split_1)
                login_name, login_pw = data
                result = self.db_conn.user_log_in(login_name, login_pw)

                # result =
                if result is False:
                    response_header = f"{f'login{header_split}{False}':{self.BUFFER}}".encode(self.FORMAT)
                    client_socket.send(response_header)

                else:
                    user_id, username, user_pw, user_nickname = result
                    response_header = f"{f'login{header_split}{user_id}{list_split_1}{username}{list_split_1}{user_pw}{list_split_1}{user_nickname}':{self.BUFFER}}".encode(
                        self.FORMAT)
                    client_socket.send(response_header)

            elif header == 'send_all_clients':  # 채팅
                msg = substance
                response_header = f"{f'recvallclients{header_split}{msg}':{self.BUFFER}}".encode(self.FORMAT)

                for c in self.sockets_list[1:]:
                    c.send(response_header)

            elif header == 'assertu_username':  # 아이디 중복
                join_username = substance
                result = self.db_conn.assertu_username(join_username)
                if result is True:
                    response_header = f"{f'assertu_username{header_split}{True}':{self.BUFFER}}".encode(self.FORMAT)
                    client_socket.send(response_header)
                elif result is False:
                    response_header = f"{f'assertu_username{header_split}{False}':{self.BUFFER}}".encode(self.FORMAT)
                    client_socket.send(response_header)

            elif header == 'get_user_character':  # 유저 캐릭터 찾기
                user_id = substance
                result = self.db_conn.find_user_character(user_id)
                character_id, _, _ = result

                if result is not None:
                    response_header = f"{f'get_user_character{header_split}{character_id}':{self.BUFFER}}".encode(
                        self.FORMAT)
                    client_socket.send(response_header)

            elif header == 'get_user_character_stat':  # 캐릭터 stat 조회
                character_id = substance
                result = self.db_conn.find_character_stat(character_id)
                character_id, character_hunger, character_affection, character_health, character_exp = result
                response_header = f"{f'recv_character_stat{header_split}{character_id}{list_split_1}{character_hunger}{list_split_1}{character_affection}{list_split_1}{character_health}{list_split_1}{character_exp}':{self.BUFFER}}".encode(
                    self.FORMAT)
                client_socket.send(response_header)


            elif header == 'join_access':  # 회원가입
                data = substance.split(list_split_1)
                result = self.db_conn.user_sign_up(data)

                if result is False:
                    response_header = f"{f'join_access{header_split}{False}':{self.BUFFER}}".encode(self.FORMAT)
                    client_socket.send(response_header)

                else:
                    response_header = f"{f'join_access{header_split}{True}':{self.BUFFER}}".encode(self.FORMAT)
                    client_socket.send(response_header)

            elif header == 'get_shop_item_list':  # 상점 아이템 목록 조회
                result = self.db_conn.find_all_shop_item()
                items = json.dumps(result)
                message = f"recv_shop_item_list{header_split}{items}"
                client_socket.send(bytes(message, "UTF-8"))
        except:
            return False

    def fixed_volume(self, header, data):
        header_msg = f"{header:<{self.HEADER_LENGTH}}".encode(self.FORMAT)
        data_msg = f"{data:<{self.BUFFER - self.HEADER_LENGTH}}".encode(self.FORMAT)
        return header_msg + data_msg
