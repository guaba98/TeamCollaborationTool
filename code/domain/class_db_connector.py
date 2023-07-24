import sqlite3

# from Code.domain.class_user import User
# from Code.domain.class_user_talk_room import UserTalkRoom
# from Code.domain.class_talk_room import TalkRoom
# from Code.domain.class_message import Message
# from Code.domain.class_long_contents import LongContents

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
        if self.test_option is True:
            self.conn = sqlite3.connect('db_test.db')
        else:
            self.conn = sqlite3.connect('main_db.db')
        return self.conn.cursor()

    def end_conn(self):
        if self.conn is not None:
            self.conn.close()
            self.conn = None

    def commit_db(self):
        if self.conn is not None:
            self.conn.commit()
        else:
            raise f"cannot commit database! {self.__name__}"

    # CREATE TABLES =======================================================================
    def create_tables(self):
        c = self.start_conn()
        c.executescript("""
    DROP TABLE IF EXISTS character;
    CREATE TABLE "character" (
        "character_id"	INTEGER,
        "user_id"	INTEGER NOT NULL,
        "character_nickname"	TEXT,
        PRIMARY KEY("character_id" AUTOINCREMENT)
    );
    DROP TABLE IF EXISTS character_stat;    
    CREATE TABLE "character_stat" (
        "character_id"	INTEGER NOT NULL,
        "character_hunger"	INTEGER NOT NULL,
        "character_affection"	INTEGER NOT NULL,
        "character_health"	INTEGER NOT NULL,
        "character_exp"	INTEGER NOT NULL
    );
    DROP TABLE IF EXISTS inventory;
    CREATE TABLE "inventory" (
        "user_id"	INTEGER NOT NULL,
        "item_id"	INTEGER NOT NULL,
        "item_name"	TEXT NOT NULL,
        "item_num"	INTEGER NOT NULL
    );
    DROP TABLE IF EXISTS item_list;
    CREATE TABLE "item_list" (
        "item_id"	INTEGER NOT NULL,
        "item_name"	INTEGER NOT NULL UNIQUE,
        "hunger"	INTEGER NOT NULL,
        "affection"	INTEGER NOT NULL,
        "health"	INTEGER NOT NULL,
        "exp"	INTEGER NOT NULL,
        PRIMARY KEY("item_id" AUTOINCREMENT)
    );
    DROP TABLE IF EXISTS user;
    CREATE TABLE "user" (
        "user_id"	INTEGER,
        "user_name"	TEXT NOT NULL UNIQUE,
        "user_pw"	TEXT NOT NULL,
        "user_nickname"	TEXT NOT NULL,
        PRIMARY KEY("user_id" AUTOINCREMENT)
    );
    """)
        self.commit_db()
        self.end_conn()

    def find_all_shop_item(self):
        c = self.start_conn()
        item_data = c.execute('select * from item_list').fetchall()
        if item_data is None:
            return None
            # all_user_obj_list = list()
            # for row_user in item_data:
            #     all_user_obj_list.append(User(*row_user))
        self.end_conn()
        return item_data

    # 로그인
    def user_log_in(self, login_id, login_pw):
        c = self.start_conn()
        exist_user = c.execute('select * from user where user_name = ? and user_pw = ?',
                               (login_id, login_pw)).fetchone()
        self.end_conn()
        if exist_user is not None:
            print('로그인 성공')
            return exist_user
        else:
            print('아이디 혹은 비밀번호를 잘못 입력했습니다.')
            return False

    def assertu_username(self, join_username):
        c = self.start_conn()
        username_id = c.execute('select * from user where user_name = ?', (join_username,)).fetchone()
        self.end_conn()

        if username_id is None:
            print('사용 가능한 아이디 입니다.')  # 사용 가능 아이디
            return True
        else:
            print('사용 불가능한 아이디 입니다.')  # 사용불가
            return False

    def assert_same_login_id(self, inserted_id):
        c = self.start_conn()
        username_id = c.execute('select * from user where user_name = ?', (inserted_id,)).fetchone()
        if username_id is None:
            print('사용 가능한 아이디 입니다.')  # 사용 가능 아이디
            return True
        else:
            print('사용 불가능한 아이디 입니다.')  # 사용불가
            return False

    # 회원가입
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

    # 유저의 캐릭터 조회
    def find_user_character(self, user_id):
        c = self.start_conn()
        character_id = c.execute('select * from character where user_id = ?', (user_id,)).fetchone()

        if character_id is None:
            result = self.character_sign_up(user_id)
            return result
        else:
            return character_id

    # 캐릭터 관련 함수

    def character_sign_up(self, user_id):

        user_id = user_id
        c = self.start_conn()
        last_user_row = c.execute('select * from character order by character_id desc limit 1').fetchone()
        if last_user_row is None:
            character_id = 1
        else:
            character_id = last_user_row[0] + 1
        self.end_conn()
        sing_up_obj = self.insert_character(character_id, user_id)
        return sing_up_obj

    def insert_character(self, character_id, user_id):
        c = self.start_conn()
        user_id = user_id
        character_id = character_id

        users_id2 = c.execute('select * from character where character_id = ?', (character_id,)).fetchone()
        if users_id2 is None:
            c.execute('insert into character(character_id, user_id) values (?, ?)',
                      (character_id, user_id))
            self.commit_db()
            inserted_user_row = c.execute('select * from character order by character_id desc limit 1').fetchone()
            self.end_conn()
            return inserted_user_row
        else:
            print('pass')

    # 캐릭터 스탯 찾기
    def find_character_stat(self, character_id):
        c = self.start_conn()
        character_stat = c.execute('select * from character_stat where character_id = ?', (character_id,)).fetchone()
        if character_stat is None:
            result = self.insert_character_stat(character_id)
            return result
        else:
            return character_stat

    def insert_character_stat(self, character_id):

        character_id = character_id
        c = self.start_conn()
        users_id2 = c.execute('select * from character_stat where character_id = ?', (character_id,)).fetchone()

        if users_id2 is None:
            c.execute(
                'insert into character_stat(character_id, character_hunger, character_affection, character_health, character_exp) values (?, ?, ?, ?, ?)',
                (character_id, 50, 0, 100, 0))
            self.commit_db()
            inserted_user_row = c.execute('select * from character_stat where character_id = ?',
                                          (character_id,)).fetchone()
            self.end_conn()
            return inserted_user_row
        else:
            print('pass')

    # DB에 유저 추가
    def insert_user(self, user_id, join_name, join_pw, join_nickname):
        c = self.start_conn()
        user_id = user_id
        user_name = join_name
        password = join_pw
        nickname = join_nickname
        users_id = c.execute('select * from user where user_id = ?', (user_id,)).fetchone()
        if users_id is None:
            c.execute('insert into user(user_name, user_pw, user_nickname) values (?, ?, ?)',
                      (user_name, password, nickname))
            self.commit_db()
            inserted_user_row = c.execute('select * from user order by user_id desc limit 1').fetchone()
            # inserted_user_obj = User(*inserted_user_row)
            self.end_conn()
            # return inserted_user_obj
        else:
            print('pass')
            # updated_user_obj = self.update_user(user_object)
            # return updated_user_obj

    # 아이템 db추가
    def item_sign_up(self, item_info_list):
        item_name, hunger, affection, health, exp = item_info_list
        c = self.start_conn()
        last_user_row = c.execute('select * from item_list order by item_id desc limit 1').fetchone()
        if last_user_row is None:
            item_id = 1
        else:
            item_id = last_user_row[0] + 1
        self.end_conn()
        self.insert_item(item_id, item_name, hunger, affection, health, exp)
        # return sing_up_obj

    def insert_item(self, item_id, item_name, hunger, affection, health, exp):
        c = self.start_conn()
        users_id2 = c.execute('select * from item_list where item_id = ?', (item_id,)).fetchone()
        if users_id2 is None:
            c.execute(
                'insert into item_list(item_id, item_name, hunger, affection, health, exp) values (?, ?, ?, ?, ?, ?)',
                (item_id, item_name, hunger, affection, health, exp))
            self.commit_db()
            # inserted_user_row = c.execute('select * from item_list order by item_id desc limit 1').fetchone()
            self.end_conn()
            # return inserted_user_row
        else:
            print('pass')
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
