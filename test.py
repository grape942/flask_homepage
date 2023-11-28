import sqlite3

# SQLite 데이터베이스 연결
conn = sqlite3.connect('your_database.db')  # 'your_database.db'는 사용할 데이터베이스 파일명입니다.

# 커서 생성
cursor = conn.cursor()

# 테이블 생성
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT NOT NULL
    )
''')

# 연결 종료
conn.close()
