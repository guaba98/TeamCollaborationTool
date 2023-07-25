import psycopg2

# PostgreSQL 데이터베이스 정보
host = '10.10.20.103'  # 데이터베이스 호스트 주소
database = 'data'  # 데이터베이스 이름
user = 'postgres'  # 데이터베이스 사용자 이름
password = '1234'  # 데이터베이스 비밀번호
port = 5432 # 포트번호

# 데이터베이스에 연결
conn = psycopg2.connect(host=host, database=database, user=user, password=password, port=port)

# 커서 생성
cur = conn.cursor()

# 예제 SQL 쿼리 실행
'''
SET search_path TO public;
SELECT * FROM "테이블이름";

'''
'''
query = f"SELECT * FROM TB_USER WHERE username = '{username}' AND password = '{password}'"
cursor.execute(query)

# 결과 가져오기
result = cursor.fetchall()
if result:
    print("로그인 성공")
else:
    print("아이디 또는 비밀번호가 일치하지 않습니다.")
'''
cur.execute('SELECT * FROM public."TB_USER"')
rows = cur.fetchall()

# 결과 출력
for row in rows:
    print(row)

# 커넥션과 커서 닫기
cur.close()
conn.close()