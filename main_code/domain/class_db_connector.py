import sqlite3

import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine
import psycopg2

# PostgreSQL 데이터베이스 정보
db_params = {
    "host": "10.10.20.103",
    "database": "data",
    "user": "postgres",
    "password": "1234",
    "port": 5432,
}
engine = create_engine(
    f"postgresql+psycopg2://{db_params['user']}:{db_params['password']}@{db_params['host']}/{db_params['database']}")

host = '10.10.20.103'  # 데이터베이스 호스트 주소
database = 'data'  # 데이터베이스 이름
user = 'postgres'  # 데이터베이스 사용자 이름
password = '1234'  # 데이터베이스 비밀번호
port = 5432  # 포트번호

# 사용할 구분자
header_split = chr(1)
list_split_1 = chr(2)
list_split_2 = chr(3)


class DBConnector:
    _instance = None

    def __new__(cls, test_option=None):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self, test_option=None):
        self.conn = None
        self.test_option = test_option

    def start_conn(self):
        self.conn = psycopg2.connect(host=host, database=database, user=user, password=password, port=port)

        # self.conn = psycopg2.connect(**db_params)
        # 커서 생성
        cur = self.conn.cursor()

        return cur

    def end_conn(self):

        if self.conn is not None:
            self.conn.close()
            self.conn = None

    def commit_db(self):

        if self.conn is not None:
            self.conn.commit()
        else:
            raise f"cannot commit database! {self.__name__}"

    # -- 로그인
    def log_in(self, login_id, login_pw):
        """아이디와 비밀번호 조회"""

        # 커서 생성
        c = self.start_conn()
        sql_query = f"SELECT * FROM public.\"TB_USER\" WHERE \"USER_ID\" = '{login_id}' AND \"USER_PW\" = '{login_pw}';"
        c.execute(sql_query)

        # 팀명 가져오기
        con1 = f"\"USER_ID\" = '{login_id}'"
        user_no = self.return_specific_data(column='USER_NO', table_name='TB_USER', condition=con1)
        con2 = f"\"USER_NO\" = '{user_no}'"
        team_name = self.return_specific_data(column='TEAM_NAME', table_name='TB_TEAM', condition=con2)

        # 결과 가져오기
        results = c.fetchall()
        results_ = [results[0] + (team_name,)]
        # 연결 종료
        self.end_conn()

        # 결과값 리턴
        if len(results) > 0:
            return results_
        return False

    # -- 로그인 기록 넣기
    def insert_login_log(self, login_id):
        # 커서 생성
        conn = psycopg2.connect(host=host, database=database, user=user, password=password, port=port)
        condition = f'"USER_ID"=\'{login_id}\''
        user_nm = self.return_specific_data(column='USER_NAME', table_name='TB_USER', condition=condition)
        time = self.return_datetime('time')
        insert_query = f"INSERT INTO public.\"TB_LOG\" (\"USER_ID\", \"USER_NAME\", \"USER_LOGIN_TIME\") " \
                       f"VALUES ('{login_id}', '{user_nm}', '{time}')"
        cur = conn.cursor()

        cur.execute(insert_query)
        conn.commit()
        conn.close()

    # -- 회원가입
    def duple_reg_id(self, join_username):
        """아이디 중복 확인"""

        # 커서 생성
        c = self.start_conn()

        # 쿼리문 및 중복 확인
        query = f"SELECT * FROM public.\"TB_USER\" WHERE \"USER_ID\" = '{join_username}';"
        c.execute(query)
        username_id = c.fetchone()
        self.end_conn()  # 커서 닫기

        # 결과값 리턴
        if username_id is None:
            return True  # 사용 가능한 아이디일때
        return False  # 사용 불가능한 아이디일때

    def insert_user(self, list_):
        """회원가입 정보 db에 추가"""
        user_id, join_pw, join_name, join_nickname, input_reg_team = list_
        conn = psycopg2.connect(host=host, database=database, user=user, password=password, port=port)
        cur = conn.cursor()
        join_date = self.return_datetime('date')

        insert_query = f"INSERT INTO public.\"TB_USER\" (\"USER_NAME\", \"USER_ID\", \"USER_PW\", \"USER_NM\", \"USER_CREATE_DATE\") " \
                       f"VALUES ('{join_name}', '{user_id}', '{join_pw}', '{join_nickname}', '{join_date}')"

        cur.execute(insert_query)

        conn.commit()
        cur.close()
        conn.close()
        self.insert_team_member(user_id, input_reg_team)
        return True

    def insert_team_member(self, user_id, team_name):
        """회원가입과 동시에 팀에 정보를 넣어줍니다."""
        conn = psycopg2.connect(host=host, database=database, user=user, password=password, port=port)
        cur = conn.cursor()
        user_no = self.return_specific_data('USER_NO', 'TB_USER', f"\"USER_ID\" = '{user_id}'")
        team_no = self.return_team_num(team_name)

        insert_query_2 = "INSERT INTO public.\"TB_TEAM\" (\"TEAM_NO\", \"TEAM_NAME\", \"TEAM_ROLE\", \"USER_NO\")" \
                         f" VALUES ('{team_no}', '{team_name}', '{'팀원'}', '{user_no}')"
        cur.execute(insert_query_2)
        conn.commit()
        cur.close()
        conn.close()

    # -- 채팅
    def insert_chat_log(self, user_no, chat):
        """채팅 기록 저장"""
        # db 연결
        conn = psycopg2.connect(host=host, database=database, user=user, password=password, port=port)
        cur = conn.cursor()

        # 데이터 삽입
        join_table = "TB_USER\" NATURAL JOIN \"TB_TEAM"
        condition = f"\"USER_NO\" = '{user_no}';"
        team_no = self.return_specific_data('TEAM_NO', join_table, condition)
        # user_no = self.return_specific_data('USER_NO', join_table, condition)
        user_name = self.return_specific_data('USER_NAME', join_table, condition)
        chat_time = self.return_datetime('time')

        insert_query = f"INSERT INTO public.\"TB_CHAT\" " \
                       f"(\"TEAM_NO\", \"USER_NO\", \"USER_NAME\", \"CHAT_LOG\", \"CHAT_TIME\")" \
                       f" VALUES ('{team_no}', '{user_no}', '{user_name}', '{chat}', '{str(chat_time)}')"

        # 저장
        cur.execute(insert_query)

        # 데이터 저장 및 닫기
        conn.commit()
        conn.close()

    # -- 공지
    def insert_notice_data(self, team_no, title, contents):
        """
        공지 작성시 db에 데이터 삽입
        :param team_no: 팀 번호
        :param title: 공지 제목
        :param contents: 공지 내용
        """
        # db 연결
        conn = psycopg2.connect(host=host, database=database, user=user, password=password, port=port)
        cur = conn.cursor()

        # 데이터 저장
        insert_query = f"INSERT INTO public.\"TB_NOTICE\" " \
                       f"(\"NOTICE_TITLE\", \"NOTICE_CONTENTS\", \"TEAM_NO\", \"UPDATE_DATE\")" \
                       f" VALUES ('{title}', '{contents}', '{team_no}', '{str(self.return_datetime('time'))}')"

        # 저장
        cur.execute(insert_query)

        # 데이터 저장 및 닫기
        conn.commit()
        conn.close()

    def get_notice_list(self, user_no):
        """공지에서 유저가 속한 팀 기준으로 공지 제목, 내용을 가져옴"""
        c = self.start_conn()

        query = "SELECT \"NOTICE_TITLE\", \"NOTICE_CONTENTS\" " \
                "FROM \"TB_NOTICE\" WHERE \"TEAM_NO\" = " \
                f"(SELECT \"TEAM_NO\" FROM \"TB_TEAM\" NATURAL JOIN \"TB_USER\" WHERE \"USER_NO\" = {user_no});"
        c.execute(query)
        result = c.fetchall()

        self.end_conn()  # 커서 닫기
        return result

    def delete_notice_data(self, title):
        """공지 삭제시 데이터에서도 삭제"""
        condition = f"\"NOTICE_TITLE\" = '{title}'"
        self.delete_specific_row(table_name="TB_NOTICE", condition=condition)

    # -- 특정 데이터 저장
    # 프로필
    def update_profile_message(self, user_no, msg):
        """프로필 상태메세지를 변경합니다."""
        condition = f"\"USER_NO\" = '{user_no}'"
        self.update_specific_data('TB_USER', 'USER_MESSAGE', msg, condition)

    def update_specific_data(self, table_name, column, data, condition=None):
        """특정 테이블에 조건에 맞는 데이터 1개만 업데이트하기"""
        # db 연결
        conn = psycopg2.connect(host=host, database=database, user=user, password=password, port=port)
        cur = conn.cursor()

        query = f"UPDATE public.\"{table_name}\" SET \"{column}\" = '{data}'"
        if condition is not None:
            query += f" WHERE {condition}"

        cur.execute(query)

        # 데이터 저장 및 닫기
        conn.commit()
        conn.close()

    # -- 투두리스트
    def delete_todo_data(self, title):
        """투두리스트 삭제시 데이터에서도 삭제"""
        condition = f"\"TODO_TITLE\" = '{title}'"
        self.delete_specific_row(table_name="TB_TODO_LIST", condition=condition)

    def update_todo_list(self, todo_id, checked):
        """투두리스트 체크시 DB 업데이트"""

        condition = f"\"TODO_ID\" = '{todo_id}'"
        time = self.return_datetime('time')

        if checked == '0':
            time = '0'

        self.update_specific_data(table_name='TB_TODO_LIST', column='TODO_CHECKED', data=checked, condition=condition)
        self.update_specific_data(table_name='TB_TODO_LIST', column='TODO_CPLT_TIME', data=time, condition=condition)

    def insert_todo_list(self, user_no, title, contents):
        """투두리스트에 값 넣어주기"""
        # db 연결
        conn = psycopg2.connect(host=host, database=database, user=user, password=password, port=port)
        cur = conn.cursor()

        # 데이터 저장
        insert_query = f"INSERT INTO public.\"TB_TODO_LIST\" " \
                       f"(\"USER_NO\", \"TODO_TITLE\", \"TODO_LIST\", \"TODO_TIME\")" \
                       f" VALUES ('{user_no}', '{title}', '{contents}', '{str(self.return_datetime('time'))}')"

        # 저장
        cur.execute(insert_query)

        # 데이터 저장 및 닫기
        conn.commit()
        conn.close()

    def insert_admin_todo_list(self, user_no, title, contents):
        """어드민이 투두리스트에 값 넣어주기"""
        # db 연결
        conn = psycopg2.connect(host=host, database=database, user=user, password=password, port=port)
        cur = conn.cursor()

        # condition = f"\"USER_ID\" = '{user_no}';"
        # user_no = self.return_specific_data('USER_NO', 'TB_USER', condition)
        # 데이터 저장
        insert_query = f"INSERT INTO public.\"TB_TODO_LIST\" " \
                       f"(\"USER_NO\", \"TODO_TITLE\", \"TODO_LIST\", \"TODO_TIME\")" \
                       f" VALUES ('{user_no}', '{title}', '{contents}', '{str(self.return_datetime('time'))}')"

        # 저장
        cur.execute(insert_query)

        # 데이터 저장 및 닫기
        conn.commit()
        conn.close()
        return user_no, title, contents, 0

    def get_todo_list(self, user_no):
        """
        투두리스트 목록 반환
        :param user_no: 유저 고유번호
        :return: results: 할일목록, 체크여부 반환. 예 - [('프로필 창 만들어야 함', 0), ('공지창도 띄워야 함', 0)]
        """
        # db 연결
        c = self.start_conn()

        # 조건
        sql_query = f"SELECT \"TODO_ID\", \"TODO_TITLE\", \"TODO_LIST\", \"TODO_CHECKED\", \"TODO_TIME\", \"TODO_CPLT_TIME\"" \
                    f"FROM \"TB_TODO_LIST\" WHERE \"USER_NO\" = {user_no} ORDER BY \"TODO_ID\" ASC"
        c.execute(sql_query)

        # 결과 가져오기
        results = c.fetchall()

        # 연결 종료
        self.end_conn()
        return results

    def return_todo_list_dict(self, team_name):
        c = self.start_conn()
        query = "SELECT \"USER_NAME\", \"TODO_TITLE\" \
                FROM \"TB_TEAM\" NATURAL JOIN \"TB_TODO_LIST\" " \
                f"NATURAL JOIN \"TB_USER\" WHERE \"TEAM_NAME\" = \'{team_name}\';"
        c.execute(query)

        result = c.fetchall()

        # 값을 딕셔너리로 반환받기.
        result_dict = dict()
        for i in result:
            if i[0] in list(result_dict.keys()):
                result_dict[i[0]].append(i[1])
            else:
                result_dict[i[0]] = [i[1]]

        # 딕셔너리 key값 리스트로 반환, value값 갯수로 반환하기
        todo_people = list(result_dict.keys())
        todo_cnt = [len(cnt) for cnt in result_dict.values()]

        # 결과값 리턴
        return todo_people, todo_cnt

    # def delete_todo_list(self):

    # db에 있는 팀명들 반환
    def return_team_name(self):
        c = self.start_conn()
        query = "SELECT \"TEAM_NAME\" FROM \"TB_TEAM\" GROUP BY \"TEAM_NAME\";"
        c.execute(query)

        # 결과 가져오기
        results = [row[0] for row in c.fetchall()]

        # 연결 종료 및 반환
        self.end_conn()
        return results

    def return_team_num(self, team_name):
        """팀 이름을 넣으면 팀 번호를 반환함"""
        self.start_conn()
        con = f"\"TEAM_NAME\" = '{team_name}'"
        team_no = self.return_specific_data(column='TEAM_NO', table_name='TB_TEAM', condition=con)

        return team_no

    def return_team_members_for_admin(self, team_name):
        """
        팀 이름을 입력하면 속한 팀원들을 모두 반환함
        :param team_name: 팀 이름
        :return: 팀원들을 리스트에 담아 반환
        """
        c = self.start_conn()
        query = f"SELECT \"USER_NO\", \"USER_ID\", \"USER_PW\", \"USER_NAME\", \"USER_NM\", \"USER_MESSAGE\", \"USER_CREATE_DATE\", \"TEAM_NAME\" " \
                f"FROM \"TB_USER\" NATURAL JOIN \"TB_TEAM\" WHERE \"TEAM_NAME\" = '{team_name}';"

        c.execute(query)

        results = c.fetchall()

        # 연결 종료
        self.end_conn()
        return results

    def return_todo_list_by_title(self, title):
        """
        투두리스트 타이틀을 입력받아 그 행을 반환합니다.
        :param title: 투두리스트 제목
        :return: 투두리스트 제목에 맞는 행
        """
        c = self.start_conn()
        query = f"SELECT * FROM \"TB_TODO_LIST\" WHERE \"TODO_TITLE\"='{title}'"

        c.execute(query)
        result = c.fetchall()
        return result

    def return_team_members(self, user_no):
        """
        유저 번호를 입력하면 속한 팀원들을 모두 반환함
        :param user_no: 유저 번호
        :return: 팀원들을 리스트에 담아 반환
        """
        c = self.start_conn()
        query = f'SELECT \"USER_NAME\" FROM \"TB_USER\" ' \
                f'NATURAL JOIN \"TB_TEAM\" WHERE \"TEAM_NAME\" ' \
                f'= (SELECT \"TEAM_NAME\" FROM \"TB_TEAM\" WHERE \"USER_NO\" = {user_no});'

        # 쿼리 실행
        c.execute(query)

        # results = c.fetchall()
        results = [row[0] for row in c.fetchall()]

        # 연결 종료
        self.end_conn()
        return results

    # -- 특정 데이터 반환하기

    def return_datetime(self, type):
        """원하는 날짜/시간 포멧을 반환"""
        now = datetime.now()  # 시간
        if type == 'date':
            now_format = now.strftime("%Y-%m-%d")  # 년 월 일
        elif type == 'time':
            now_format = now.strftime("%Y-%m-%d %H:%M:%S")  # 년 월 일 시 분 초
        elif type == 'time_only':
            now_format = now.strftime("%H:%M:%S")  # 시 분 초

        # print('[dateimte.py]시간 포멧팅: ', now_format)
        return now_format

    def return_notice_all_data(self):
        """모든 공지를 반환합니다.(관리자용)"""
        c = self.start_conn()
        query = "SELECT * FROM \"TB_NOTICE\""
        c.execute(query)
        result = c.fetchall()

        return result

    def return_specific_data(self, column, table_name, condition=None, type=None):
        """특정 열 데이터만 반환합니다."""
        c = self.start_conn()

        query = f"SELECT \"{column}\" FROM public.\"{table_name}\""
        if condition is not None:
            query += f" WHERE {condition}"

        c.execute(query)
        r_data = c.fetchall()
        # print('데이터', r_data)
        if type is None:
            return r_data[0][0]
        return r_data

    def return_user_no(self, user_id):
        """
        유저 아이디를 받으면 넘버로 돌려줌
        :param user_id:
        :return:
        """
        c = self.start_conn()
        condition = f"\"USER_ID\" = '{user_id}'"
        user_no = self.return_specific_data(table_name='TB_USER', column='USER_NO', condition=condition)

        return user_no

    def delete_specific_row(self, table_name, condition):
        """특정 열 삭제"""
        # db 연결
        conn = psycopg2.connect(host=host, database=database, user=user, password=password, port=port)
        cur = conn.cursor()

        query = f"DELETE FROM \"{table_name}\" WHERE {condition};"

        # 저장
        cur.execute(query)

        # 데이터 저장 및 닫기
        conn.commit()
        conn.close()

    def return_chat_log(self, user_id):
        """
        유저 아이디를 기준으로 마지막으로 유저가 채팅한 시간과 현재 시간 사이에 온 채팅을 접속할 때 넣어준다.
        :param user_id:
        :return: 채팅 기록 리턴
        """

        c = self.start_conn()
        user_no = self.return_user_no(user_id=user_id)

        # 유저의 마지막 채팅 시간 구하기
        query = f"SELECT \"CHAT_TIME\" FROM \"TB_CHAT\" WHERE \"USER_NO\" = '{user_no}' " \
                f"ORDER BY \"CHAT_TIME\" DESC LIMIT 1"
        c.execute(query)
        results = c.fetchall()
        last_chat_time = results[0][0]  # 유저의 마지막 채팅 시간

        # 현재 시간 구하기
        now = self.return_datetime('time')

        # 마지막 채팅 시간과 현재 시간 사이의 채팅들 불러오기
        query_ = "SELECT \"USER_NAME\", \"CHAT_LOG\", \"CHAT_TIME\" FROM \"TB_CHAT\" " \
                 f"WHERE \"CHAT_TIME\" > '{last_chat_time}' " \
                 f"AND \"CHAT_TIME\" < '{now}';"
        c.execute(query_)
        chats = [(n[0], n[1]) for n in c.fetchall()]  # 이름, 내용 반환

        return chats


