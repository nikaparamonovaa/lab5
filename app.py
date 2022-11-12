import requests
from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)

conn = psycopg2.connect(database="service_db",
                        user="postgres",
                       password="sql2004Nika",
                      host="localhost",
                     port="5432")

cursor = conn.cursor()

@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if request.form.get("login"):
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
                errorUser = 'Такой пользователь не зарегистрирован'
                return render_template('login.html', errorUser=errorUser)

            return render_template('account.html', full_name=records[0][1],username=records[0][2], password=records[0][3])
        elif request.form.get("registration"):
            return redirect("/registration/")

    return render_template('login.html')

@app.route('/registration/', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        name = request.form.get('name')
        login = request.form.get('login')
        password = request.form.get('password')

        cursor.execute("SELECT * FROM service.users WHERE login=%s", (str(login),))
        records = list(cursor.fetchall())

        if len(records) > 0:
            errorAlreadyUser = 'Пользователь с таким логином уже зарегистрирован. Придумайте другой'
            return render_template('registration.html', errorAlreadyUser=errorAlreadyUser)

        if len("".join(name.split())) == 0 or len("".join(login.split())) == 0 or len("".join(password.split())) == 0:
            error4 = 'Введите все поля ввода данных'
            return render_template('registration.html', error4=error4)

            cursor.execute('INSERT INTO service.users (full_name, login, password) VALUES (%s, %s, %s);',
                           (str(name), str(login), str(password)))
            conn.commit()
        return redirect('/login/')
    return render_template('registration.html')