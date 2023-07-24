from threading import *
from socket import *
from temporary_storage import Store

# _SERVER_IP = '10.10.20.109'
_SERVER_IP = gethostbyname(gethostname())
_SERVER_PORT = 5050
BUFFER = 50000
FORMAT = "utf-8"
_CONNECT = (_SERVER_IP, _SERVER_PORT)

header_split = chr(1)
list_split_1 = chr(2)
list_split_2 = chr(3)


class Client(Store):
    def __init__(self, ui_controller = None):
        super().__init__()
        self.ui_controller = ui_controller
        self.client_socket = None
        self._connected = None

        self.connect_server()
        self.listeningThread = Thread(target=self.check_server_response, daemon=True)
        self.listeningThread.start()

    def connect_server(self):
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect(_CONNECT)
        message = f"{f'enter{header_split}접속한다':{BUFFER}}".encode(FORMAT)
        self.send_message(message)
        self._connected = True

    def send_message(self, message):
        self.client_socket.send(message)

    def check_server_response(self):
        while self._connected:
            # if not self.client_socket == None:
            try:
                response = self.client_socket.recv(BUFFER).decode(FORMAT).strip()
                print("메인 레스폰스", response)
                self._parse_packet(response)

            except Exception as e:
                print(e)
                pass

    def _parse_packet(self, p: str):
        parsed = p.split(header_split)
        header = parsed[0].strip()

        if header == 'duple': # 아이디 중복 검사 true면 노중복 false면 중복
            result = parsed[1]
            if result == 'true':
                self.ui_controller.emit_login_object("사용 가능한 아이디 입니다")
                self.ui_controller.emit_login_object_duple_status()
            elif result == 'false':
                self.ui_controller.emit_login_object("사용할 수 없는 아이디입니다")
        elif header == 'login':
            result = parsed[1]
            if result == 'true':
                self.ui_controller.emit_login_object_login('true')
            elif result == 'false':
                self.ui_controller.emit_login_object_login('false')
        elif header == 'info':
            substance = parsed[1].split(list_split_1)
            self.member_info['id'] = [substance[0]]
            self.member_info['pw'] = [substance[1]]
            self.member_info['name'] = [substance[2]]
            self.member_info['car'] = [substance[3]]
            self.ui_controller.emit_mypage_data()
        elif header == 'open':
            self.ui_controller.emit_add_msg(f'{header}','무엇을 도와드릴까요?')
        elif header == 'member':
            msg = parsed[1]
            self.ui_controller.emit_add_msg(f'{header}', msg)
        elif header == 'admin':
            msg = parsed[1]
            self.ui_controller.emit_add_msg(f'{header}', msg)
        elif header == 'blue':
            substance = parsed[1]
            data = substance.split(list_split_1)
            self.ui_controller.emit_blue_info(data)
        elif header == 'r_duple':
            result = parsed[1]
            self.ui_controller.emit_alert_reserve_duple(result)
        elif header == 'req_reserve_data':
            substance = parsed[1]
            receive_data = substance.split(f"{list_split_1}")
            self.ui_controller.emit_set_reserve_check_page(receive_data)
        elif header == 'reserve_duple':
            receive_data = parsed[1]
            self.ui_controller.emit_check_reserve_duple(receive_data)
