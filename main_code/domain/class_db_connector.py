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
        print('[db_connector.py - log_in]결과값: ', results_)
        # 연결 종료
        self.end_conn()

        # 결과값 리턴
        if len(results) > 0:
            return results_
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

    def insert_user(self, list_):
        """회원가입 정보 db에 추가"""
        user_id, join_pw, join_name, join_nickname = list_
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
        return True

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
        print('[db_connector - insert_chat_log]: 쿼리문', insert_query)

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
        print('[db_connector - insert_chat_log]: 쿼리문', insert_query)

        # 저장
        cur.execute(insert_query)

        # 데이터 저장 및 닫기
        conn.commit()
        conn.close()

    def get_notice_list(self, user_no):
        """공지에서 유저가 속한 팀 기준으로 공지 제목, 내용을 가져옴"""
        c = self.start_conn()
        query = "SELECT \"NOTICE_TITLE\", \"NOTICE_CONTENTS\" " \
                "FROM \"TB_NOTICE\" NATURAL JOIN \"TB_TEAM\" " \
                f"WHERE \"TEAM_NO\" = (SELECT \"TEAM_NO\" FROM \"TB_TEAM\" WHERE \"USER_NO\" = {user_no});"
        print(query)
        c.execute(query)
        result = c.fetchall()
        print('[db_connector.py - get_notice_list]: ', result)
        print(result)

        self.end_conn()  # 커서 닫기
        return result

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
        print('쿼리문', query)
        cur.execute(query)

        # 데이터 저장 및 닫기
        conn.commit()
        conn.close()

    # -- 투두리스트

    def update_todo_list(self, todo_id, checked):
        """투두리스트 체크시 DB 업데이트"""

        condition = f"\"TODO_ID\" = '{todo_id}'"
        self.update_specific_data(table_name='TB_TODO_LIST', column='TODO_CHECKED', data=checked, condition=condition)

    def insert_todo_list(self, user_no, title, contents):
        """투두리스트에 값 넣어주기"""
        # db 연결
        conn = psycopg2.connect(host=host, database=database, user=user, password=password, port=port)
        cur = conn.cursor()

        # condition = f"\"USER_ID\" = '{user_no}';"
        # user_no = self.return_specific_data('USER_NO', 'TB_USER', condition)
        # 데이터 저장
        insert_query = f"INSERT INTO public.\"TB_TODO_LIST\" " \
                       f"(\"USER_NO\", \"TODO_TITLE\", \"TODO_LIST\", \"TODO_TIME\")" \
                       f" VALUES ('{user_no}', '{title}', '{contents}', '{str(self.return_datetime('time'))}')"
        print('[db_connector - insert_chat_log]: 쿼리문', insert_query)

        # 저장
        cur.execute(insert_query)

        # 데이터 저장 및 닫기
        conn.commit()
        conn.close()

    def get_todo_list(self, user_no):
        """
        투두리스트 목록 반환
        :param user_no: 유저 고유번호
        :return: results: 할일목록, 체크여부 반환. 예 - [('프로필 창 만들어야 함', 0), ('공지창도 띄워야 함', 0)]
        """
        # db 연결
        c = self.start_conn()

        # 조건
        sql_query = f"SELECT \"TODO_ID\", \"TODO_TITLE\", \"TODO_LIST\", \"TODO_CHECKED\", \"TODO_TIME\" " \
                    f"FROM \"TB_TODO_LIST\" WHERE \"USER_NO\" = {user_no}"
        c.execute(sql_query)

        # 결과 가져오기
        results = c.fetchall()
        print('[db_connector.py - get_todo_list]: ', results)
        # 연결 종료
        self.end_conn()
        return results

    # db에 있는 팀명들 반환
    def return_team_name(self):
        c = self.start_conn()
        query = "SELECT \"TEAM_NAME\" FROM \"TB_TEAM\" GROUP BY \"TEAM_NAME\";"
        c.execute(query)

        # 결과 가져오기
        results = [row[0] for row in c.fetchall()]
        print('[db_connector.py - return_team_name]: ', results)
        # 연결 종료 및 반환
        self.end_conn()
        return results

    def return_team_num(self, team_name):
        """팀 이름을 넣으면 팀 번호를 반환함"""
        self.start_conn()
        con = f"\"TEAM_NAME\" = '{team_name}'"
        team_no = self.return_specific_data(column='TEAM_NO', table_name='TB_TEAM', condition=con)
        print("팀 번호:", team_no)
        return team_no

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
        print(query)

        # 쿼리 실행
        c.execute(query)

        # results = c.fetchall()
        results = [row[0] for row in c.fetchall()]
        print('[db_connector.py - return_team_members]: ', results)

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

    def return_specific_data(self, column, table_name, condition=None, type=None):
        """특정 열 데이터만 반환합니다."""
        c = self.start_conn()

        query = f"SELECT \"{column}\" FROM public.\"{table_name}\""
        if condition is not None:
            query += f" WHERE {condition}"
        print(query)

        c.execute(query)
        r_data = c.fetchall()
        # print('데이터', r_data)
        if type is None:
            return r_data[0][0]
        return r_data


if __name__ == '__main__':
    pass
    # d = DBConnector()
    # # # query = '\"USER_NAME\"=\'박소연\''
    # # # a = d.return_specific_data(table_name='TB_USER', column='USER_NAME', condition=query)
    # # # d.insert_login_log('admin')
    # #
    # # d.insert_user('user_id', 'join_name', 'join_pw', 'join_nickname')
    # # d.insert_notice_data('admin', '테스트 제목제목', '테스트 내용 내용')
    # # condition = "\"USER_NAME\" = '박소연'"
    # # d.insert_specific_data('TB_USER', 'USER_MESSAGE', '관리자는 바빠요', condition)
    #
    # d.get_notice_list(7)
    # result = d.return_team_num('개발부')
    # print(result)
    # print(r_)
