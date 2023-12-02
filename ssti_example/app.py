# app.py

from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    user_input = request.args.get('user_input', 'Default User')
    #eval(user_input)
    return render_template('index.html', user_input=user_input)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)
