import sqlite3
import select
from socket import *
from threading import *
from code.domain.class_db_connector import DBConnector

# 사용할 구분자
header_split = chr(1)
list_split_1 = chr(2)
list_split_2 = chr(3)


class Server():
    HOST = gethostbyname(gethostname())

    PORT = 5050
    BUFFER = 50000
    FORMAT = 'utf-8'

    connected_member = list()
    def __init__(self, db_conn: DBConnector):
        self.db_conn = db_conn
        self._serverSocket = socket(AF_INET, SOCK_STREAM)
        self.server_socket = None
        self.config = None
        self.sockets_list = list()
        self.clients = dict()
        self.thread_for_run = None
        self.run_signal = True

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
                    user = self.receive_message(client_socket)
                    print("connected")
                    if user is False:
                        continue
                    self.sockets_list.append(client_socket)
                    self.clients[client_socket] = user

                else:
                    message = self.receive_message(notified_socket)

                    if message is False:
                        self.sockets_list.remove(notified_socket)
                        del self.clients[notified_socket]
                        continue

            for notified_socket in exception_sockets:
                self.sockets_list.remove(notified_socket)
                del self.clients[notified_socket]

    def receive_message(self, client_socket: socket):
        try:
            recv_message = client_socket.recv(self.BUFFER)
            print(recv_message.decode(self.FORMAT))

            decode_msg = recv_message.decode(self.FORMAT).strip()
            header = decode_msg.split(header_split)[0]
            if header == 'duple': # 아이디 중복제거
                id =  decode_msg.split(header_split)[1]
                sql = f"select member_id from member where member_id = '{id}'"
                data = self.active_DB(sql)
                result = self.duple_check(data)
                if result == 0:
                    message = f"{f'duple{header_split}true':{self.BUFFER}}".encode(self.FORMAT)
                    self.send_message(client_socket, message)
                elif result > 0:
                    message = f"{f'duple{header_split}false':{self.BUFFER}}".encode(self.FORMAT)
                    self.send_message(client_socket, message)
            elif header == 'join': # 가입
                substance = decode_msg.split(header_split)[1]
                data = substance.split(list_split_1)
                id, pw, name, car = data
                sql = f"insert into member (member_id, member_pw, member_name, member_car) values " \
                      f"('{id}', '{pw}', '{name}', '{car}')"
                self.active_DB(sql)
            elif header == 'login': # 로긴
                substance = decode_msg.split(header_split)[1]
                data = substance.split(list_split_1)
                id, pw = data
                sql = f"select member_pw from member where member_id = '{id}'"
                sql_data = self.active_DB(sql)
                result = self.password_check(pw, sql_data)
                if result == 1: # 패스워드가 맞으면 트루 센드
                    message = f"{f'login{header_split}true':{self.BUFFER}}".encode(self.FORMAT)
                    self.send_message(client_socket, message)
                    self.connected_member.append(id)
                    sql = f"select * from member where member_id = '{id}'"
                    info = self.active_DB(sql)
                    info_data = self.send_info(info)
                    member_id, member_pw, member_name, member_car = info_data[1:]
                    info_message = f"{f'info{header_split}{member_pw}{list_split_1}{member_pw}{list_split_1}{member_name}{list_split_1}{member_car}':{self.BUFFER}}".encode(
                        self.FORMAT)
                    self.send_message(client_socket, info_message)
                else: # 패스워드 틀리면 펄스 센드
                    message = f"{f'login{header_split}false':{self.BUFFER}}".encode(self.FORMAT)
                    self.send_message(client_socket, message)
            elif header == 'open': # 문의하기 오픈
                message = f"{f'open{header_split}무엇을 도와드릴까요?':{self.BUFFER}}".encode(self.FORMAT)
                self.send_message(client_socket, message)
            elif header == 'member':
                substance = decode_msg.split(header_split)[1]
                message = f"{f'member{header_split}{substance}':{self.BUFFER}}".encode(self.FORMAT)
                self.send_message(client_socket, message)
            elif header == 'admin':
                substance = decode_msg.split(header_split)[1]
                message = f"{f'admin{header_split}{substance}':{self.BUFFER}}".encode(self.FORMAT)
                self.send_message(client_socket, message)
            elif header == 'blue':
                sql = f"select * from bluehands"
                datas = self.active_DB(sql)
                for data in datas:
                    name, address, tel, worktime = data
                    message = f"{f'blue{header_split}{name}{list_split_1}{address}{list_split_1}{tel}{list_split_1}{worktime}':{self.BUFFER}}".encode(self.FORMAT)
                    self.send_message(client_socket, message)
            elif header == 'r_duple':
                substance = decode_msg.split(header_split)[1]
                receive_data = substance.split(list_split_1)
                center_name, date, time = receive_data
                sql = f"select * from reserve where center_name = '{center_name}' and date = '{date}' and time = '{time}'"
                sql_result = self.active_DB(sql)
                result = self.reserve_duple_check(sql_result)
                if result == 0: # 중복 예약 없음
                    message = f"{f'r_duple{header_split}true':{self.BUFFER}}".encode(self.FORMAT)
                    self.send_message(client_socket, message)
                else:
                    message = f"{f'r_duple{header_split}false':{self.BUFFER}}".encode(self.FORMAT)
                    self.send_message(client_socket, message)
            elif header == "reserve":
                substance = decode_msg.split(header_split)[1]
                data = substance.split(list_split_1)
                center_name, date, time, member_id, member_name, member_car, reserve_contents = data
                if chr(3) in data[-1]:
                    reserve_contents = data[-1].split(list_split_2)
                    reserve_contents = ','.join(reserve_contents)
                sql = f"insert into reserve values('{center_name}', '{date}', '{time}', '{member_id}','{member_name}', '{member_car}', '{reserve_contents}')"
                self.active_DB(sql)
            elif header == 'req_reserve_data':
                receive_id = decode_msg.split(header_split)[1]
                sql = f"select * from reserve where member_id = '{receive_id}'"
                sql_data = self.active_DB(sql)
                send_data = self.send_info(sql_data)
                center_name, date, time, member_id, member_name, member_car, reserve_desc = send_data
                if ',' in reserve_desc:
                    reserve_desc.replace(',', f'{list_split_2}')
                message = f"{f'req_reserve_data{header_split}{center_name}{list_split_1}{date}{list_split_1}{time}{list_split_1}{member_name}{list_split_1}{member_car}{list_split_1}{reserve_desc}':{self.BUFFER}}".encode(
                    self.FORMAT)
                self.send_message(client_socket, message)
            elif header == 'reserve_duple':
                receive_id = decode_msg.split(header_split)[1]
                sql = f"select member_id from reserve where member_id = '{receive_id}'"
                sql_data = self.active_DB(sql)
                result = self.duple_check(sql_data)
                if result == 0 :
                    message = f"{f'reserve_duple{header_split}possible':{self.BUFFER}}".encode(
                        self.FORMAT)
                else:
                    message = f"{f'reserve_duple{header_split}impossible':{self.BUFFER}}".encode(
                        self.FORMAT)
                self.send_message(client_socket, message)
            elif header == 'reserve_cancel':
                receive_id = decode_msg.split(header_split)[1]
                sql = f"delete from reserve where member_id = '{receive_id}'"
                self.active_DB(sql)
            elif header == 'change_pw':
                receive_data = decode_msg.split(header_split)[1]
                id = receive_data.split(list_split_1)[0]
                pw = receive_data.split(list_split_1)[1]
                sql = f"update member set member_pw = '{pw}' where member_id = '{id}'"
                self.active_DB(sql)
            elif header == 'change_car':
                receive_data = decode_msg.split(header_split)[1]
                id = receive_data.split(list_split_1)[0]
                car = receive_data.split(list_split_1)[1]
                sql = f"update member set member_car = '{car}' where member_id = '{id}'"
                self.active_DB(sql)
        except Exception as e:
           pass

    def send_message(self, client_socket: socket, result):
        print(f"Server SENDED: ({result})")
        client_socket.send(result)

    def active_DB(self, sql):
        conn = sqlite3.connect("./db/server_data.db")
        cur = conn.cursor()
        result = cur.execute(sql)
        conn.commit()
        return result

    # 중복검사
    def duple_check(self, object):
        tmp_list = list()
        for id in object:
            tmp_list.append(id[0])
        return len(tmp_list)

    def password_check(self, pw, object):
        for data in object:
            if pw == data[0]:
                return 1
        return 0

    def reserve_duple_check(self, object):
        tmp_list = list()
        for id in object:
            tmp_list.append(id[0])
        return len(tmp_list)


    def send_info(self, object):
        for data in object:
            return data



# if __name__ == '__main__':
#     server = Server()
#     server.start()
