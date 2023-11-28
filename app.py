# app.py
from flask import *
# from flask_migrate import Migrate
# from flask_sqlalchemy import SQLAlchemy
# import os

# BASE_DIR = os.path.dirname(__file__)

# SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'pybo.db'))
# SQLALCHEMY_TRACK_MODIFICATIONS = False

app = Flask(__name__)

@app.route('/') # 접속하는 url
def index():
  #return "hello Flask!"
  return render_template('index.html')

@app.route('/hello') # 접속하는 url
def hello1():
  #return "hello Flask!"
  return render_template('hello.html')
  
@app.route('/profile') # 접속하는 url
def show_profile():
  return render_template('profile.html')

if __name__=="__main__":
  app.run(host="0.0.0.0", port="8000", debug=True)