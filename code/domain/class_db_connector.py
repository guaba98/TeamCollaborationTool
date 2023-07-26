import sqlite3

import pandas as pd
from datetime import datetime
# from Code.domain.class_user import User
# from Code.domain.class_user_talk_room import UserTalkRoom
# from Code.domain.class_talk_room import TalkRoom
# from Code.domain.class_message import Message
# from Code.domain.class_long_contents import LongContents
import psycopg2
from sqlalchemy import create_engine

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
        print('서버랑 db연결')
        self.conn = psycopg2.connect(host=host, database=database, user=user, password=password, port=port)
        print('db 연결된')
        # self.conn = psycopg2.connect(**db_params)
        # 커서 생성
        cur = self.conn.cursor()
        # query = f"SELECT * FROM public.\"TB_USER\""
        # cur.execute(query)
        # results = cur.fetchall()
        # print(results)

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

        # 결과 가져오기
        results = c.fetchall()
        print('[db_connector.py - log_in]결과값: ', results)
        # 연결 종료
        self.end_conn()

        # 결과값 리턴
        if len(results) > 0:
            return results
        return False

    # -- 로그인 기록 넣기
    def insert_login_log(self, login_id):
        print('타나요')
        # 커서 생성
        conn = psycopg2.connect(host=host, database=database, user=user, password=password, port=port)
        condition = f'"USER_ID"=\'{login_id}\''
        user_nm = self.return_specific_data(column='USER_NAME', table_name='TB_USER', condition=condition)
        time = self.return_datetime('time')
        insert_query = f"INSERT INTO public.\"TB_LOG\" (\"USER_ID\", \"USER_NAME\", \"USER_LOGIN_TIME\") " \
                       f"VALUES ('{login_id}', '{user_nm}', '{time}')"
        print('[db_connector - insert_login_log]: 쿼리문', insert_query)
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

    def insert_user(self, user_id, join_name, join_pw, join_nickname):
        """회원가입 정보 db에 추가"""
        conn = psycopg2.connect(host=host, database=database, user=user, password=password, port=port)
        cur = conn.cursor()
        join_date = self.return_datetime('date')

        insert_query = f"INSERT INTO public.\"TB_USER\" (\"USER_NAME\", \"USER_ID\", \"USER_PW\", \"USER_NM\", \"USER_CREATE_DATE\") " \
                       f"VALUES ('{join_name}', '{user_id}', '{join_pw}', '{join_nickname}', '{join_date}')"
        print('[db_connector - insert_login_log]: 쿼리문', insert_query)
        cur.execute(insert_query)
        conn.commit()
        cur.close()
        conn.close()

    # -- 채팅
    def insert_chat_log(self, user_id, chat):
        """채팅 기록 저장"""
        # db 연결
        conn = psycopg2.connect(host=host, database=database, user=user, password=password, port=port)
        cur = conn.cursor()

        # 데이터 삽입
        join_table = "TB_USER\" NATURAL JOIN \"TB_TEAM"
        condition = f"\"USER_ID\" = '{user_id}';"
        team_no = self.return_specific_data('TEAM_NO', join_table, condition)
        user_no = self.return_specific_data('USER_NO', join_table, condition)
        user_name = self.return_specific_data('USER_NAME', join_table, condition)
        chat_time = self.return_datetime('time')

        insert_query = f"INSERT INTO public.\"TB_CHAT\" " \
                       f"(\"TEAM_NO\", \"USER_NO\", \"USER_NAME\", \"CHAT_LOG\", \"CHAT_TIME\")" \
                       f" VALUES ('{team_no}', '{user_no}', '{user_name}', '{chat}', '{str(chat_time)}')"
        print('[db_connector - insert_chat_log]: 쿼리문', insert_query)

        # 저장
        cur.execute(insert_query)

        # 데이터 저장 및 닫기
        conn.commit()
        conn.close()

    # -- 공지
    def insert_notice_data(self, user_id, title, contents):
        """공지 작성시 db에 데이터 삽입"""
        # db 연결
        conn = psycopg2.connect(host=host, database=database, user=user, password=password, port=port)
        cur = conn.cursor()


        # 데이터 저장
        insert_query = f"INSERT INTO public.\"TB_NOTICE\" " \
                       f"(\"NOTICE_TITLE\", \"NOTICE_CONTENTS\", \"USER_ID\", \"UPDATE_DATE\")" \
                       f" VALUES ('{title}', '{contents}', '{user_id}', '{str(self.return_datetime('time'))}')"
        print('[db_connector - insert_chat_log]: 쿼리문', insert_query)

        # 저장
        cur.execute(insert_query)

        # 데이터 저장 및 닫기
        conn.commit()
        conn.close()

    def delete_notice_data(self, title):
        """공지 삭제시 데이터에서도 삭제"""
        # db 연결
        conn = psycopg2.connect(host=host, database=database, user=user, password=password, port=port)
        cur = conn.cursor()

        query = f"DELETE FROM \"TB_NOTICE\" WHERE \"NOTICE_TITLE\" = '{title}';"
        # 저장
        cur.execute(query)

        # 데이터 저장 및 닫기
        conn.commit()
        conn.close()

    # -- 특정 데이터 저장
    # 프로필
    def insert_specific_data(self, table_name, column, data, condition=None):
        """특정 테이블에 조건에 맞는 데이터 1개만 업데이트하기"""
        # db 연결
        conn = psycopg2.connect(host=host, database=database, user=user, password=password, port=port)
        cur = conn.cursor()

        query = f"UPDATE INTO public.\"{table_name}\" SET (\"{column}\") = ('{data}')"
        if condition is not None:
            query += f" WHERE {condition}"
        print('쿼리문', query)
        cur.execute(query)

        # 데이터 저장 및 닫기
        conn.commit()
        conn.close()


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

    def return_specific_data(self, column, table_name, condition=None):
        """특정 열 데이터만 반환합니다."""
        c = self.start_conn()

        query = f"SELECT \"{column}\" FROM public.\"{table_name}\""
        if condition is not None:
            query += f" WHERE {condition}"
        print(query)

        c.execute(query)
        r_data = c.fetchall()
        print('데이터', r_data)

        return r_data[0][0]

    # 여기서부터 사용 안함

    def user_sign_up(self, user_data):
        join_name, join_pw, join_nickname = user_data
        useable_id = self.assert_same_login_id(join_name)
        if useable_id is False:
            return False
        c = self.start_conn()
        last_user_row = c.execute('select * from user order by user_id desc limit 1').fetchone()
        if last_user_row is None:
            user_id = 1
        else:
            user_id = last_user_row[0] + 1
        self.end_conn()
        sing_up_obj = self.insert_user(user_id, join_name, join_pw, join_nickname)
        return sing_up_obj
    # def assert_same_login_id(self, inserted_id):
    #     c = self.start_conn()
    #
    #     username_id = c.execute('select * from user where username = ?', (inserted_id,)).fetchone()
    #     if username_id is None:
    #         print('사용 가능한 아이디 입니다.')  # 사용 가능 아이디
    #         return True
    #     else:tj
    #         print('사용 불가능한 아이디 입니다.')  # 사용불가
    #         return False
    #
    # # 회원가입용 함수(insert_user함수 호출)
    # def user_sign_up(self, insert_id, insert_pw, nickname):
    #     useable_id = self.assert_same_login_id(insert_id)
    #     if useable_id is False:
    #         return False
    #     c = self.start_conn()
    #     last_user_row = c.execute('select * from user order by user_id desc limit 1').fetchone()
    #     if last_user_row is None:
    #         user_id = 1
    #     else:
    #         user_id = last_user_row[0] + 1
    #     sign_up_user_obj = User(user_id, insert_id, insert_pw, nickname)
    #     self.end_conn()
    #     sing_up_obj = self.insert_user(sign_up_user_obj)
    #     return sing_up_obj


if __name__ == '__main__':
    pass
    d = DBConnector()
    # # query = '\"USER_NAME\"=\'박소연\''
    # # a = d.return_specific_data(table_name='TB_USER', column='USER_NAME', condition=query)
    # # d.insert_login_log('admin')
    #
    # d.insert_user('user_id', 'join_name', 'join_pw', 'join_nickname')
    # d.insert_notice_data('admin', '테스트 제목제목', '테스트 내용 내용')
    condition = "\"USER_NAME\" = '박소연'"
    d.insert_specific_data('TB_USER', 'USER_MESSAGE', '저는 행복합니다...', condition)