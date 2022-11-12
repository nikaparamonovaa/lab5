import requests
from flask import Flask, render_template, request
import psycopg2

app = Flask(__name__)

conn = psycopg2.connect(database="service_db",
                        user="postgres",
                       password="sql2004Nika",
                      host="localhost",
                     port="5432")

cursor = conn.cursor()

@app.route('/login/', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    cursor.execute("SELECT * FROM service.users WHERE login=%s AND password=%s", (str(username), str(password)))
    records = list(cursor.fetchall())

    if len("".join(username.split())) == 0 and len("".join(password.split())) == 0:
        error3 = 'Введите данные (логин и пароль)'
        return render_template('login.html', error3=error3)

    if len("".join(password.split())) == 0:
        error2 = 'Введите пароль'
        return render_template('login.html', error2=error2)

    elif len("".join(username.split())) == 0:
            error1 = 'Введите логин'
            return render_template('login.html', error1=error1)

    if len(records) == 0:
        errorUser = 'В базе нет такого юзера'
        return render_template('login.html', errorUser=errorUser)

    return render_template('account.html', full_name=records[0][1], username=records[0][2], password=records[0][3])

@app.route('/login/', methods=['GET'])
def index():
    return render_template('login.html')