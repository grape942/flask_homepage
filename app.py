from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_session import Session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'

Session(app)

# 사용자 데이터베이스 설정
USERS_DATABASE = 'users.db'

# 게시물 데이터베이스 설정
POSTS_DATABASE = 'posts.db'

# 데이터베이스 초기화 함수
def initialize_users_db():
    with sqlite3.connect(USERS_DATABASE) as connection:
        cursor = connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            username TEXT NOT NULL,
                            password TEXT NOT NULL)''')
        connection.commit()

def initialize_posts_db():
    with sqlite3.connect(POSTS_DATABASE) as connection:
        cursor = connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS posts (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            title TEXT NOT NULL,
                            content TEXT NOT NULL)''')
        connection.commit()

initialize_users_db()
initialize_posts_db()

# 게시물 추가 함수
def add_post(title, content):
    with sqlite3.connect(POSTS_DATABASE) as connection:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO posts (title, content) VALUES (?, ?)", (title, content))
        connection.commit()

# 게시물 조회 함수
def get_posts():
    with sqlite3.connect(POSTS_DATABASE) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM posts ORDER BY id DESC")
        posts = cursor.fetchall()
        return posts

@app.route("/")
def home():
    query_name = request.args.get('username', 'Guest')
    posts = get_posts()
    return render_template("index.html", name=query_name, posts=posts)

@app.route("/signup", methods=["POST"])
def signup():
    username = request.form.get("username")
    password = request.form.get("password")

    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()

        # 사용자 이름 중복 확인
        cursor.execute(f"SELECT * FROM users WHERE username='{username}'")
        existing_user = cursor.fetchone()

        if existing_user:
            flash("이미 존재하는 사용자 이름입니다.")
            return redirect(url_for("home"))

        # 비밀번호 해싱
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        # 사용자 정보 저장
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password)) #### 여기 수정
        connection.commit()

        flash("회원가입이 완료되었습니다. 로그인해주세요.")
        return redirect(url_for("home"))

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()

        # 사용자 정보 확인
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        user = cursor.fetchone()

        if user and check_password_hash(user[2], password):
            # 로그인 성공 시 세션 생성
            session['user_id'] = user[0]
            session['username'] = user[1]
            flash(f"로그인 성공! 환영합니다, {username}님.")
            return redirect(url_for("dashboard"))
        else:
            flash("로그인 실패. 사용자 이름 또는 비밀번호를 확인하세요.")
            return redirect(url_for("home"))

@app.route("/dashboard")
def dashboard():
    if 'user_id' in session:
        return f"안녕하세요, {session['username']}님. 이것은 대시보드입니다."
    else:
        flash("로그인이 필요합니다.")
        return redirect(url_for("home"))

@app.route("/logout")
def logout():
    # 로그아웃 시 세션 제거
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for("home"))



@app.route("/add_post", methods=["GET", "POST"])
def add_post_page():
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        add_post(title, content)
        flash("게시물이 추가되었습니다.")
        return redirect(url_for("view_posts"))
    return render_template("add_post.html")

@app.route("/posts")
def view_posts():
    posts = get_posts()
    return render_template("post.html", posts=posts)

if __name__ == "__main__":

    app.run(host="0.0.0.0", port=8000, debug=True)