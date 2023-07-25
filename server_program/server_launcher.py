import sys

from code.domain.class_db_connector import DBConnector
from server_program.class_server_1 import Server

if __name__ == '__main__':
    conn = DBConnector()
    conn.create_tables()

    server = Server(conn)
    server.start()
