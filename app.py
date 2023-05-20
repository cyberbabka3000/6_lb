import psycopg2
from flask import Flask, render_template, request, redirect
import requests

app = Flask(__name__)

conn = psycopg2.connect(
    database='service_db',
    user='postgres',
    password='Dan12345',
    host='localhost',
    port='5432'
    )

cursor = conn.cursor()


@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.form.get('registration'):
        return redirect('/registration/')

    else:
        username = request.form.get('username')
        password = request.form.get('password')

    cursor.execute("SELECT * FROM users WHERE login=%s AND password=%s;", (str(username), str(password)))
    record = list(cursor.fetchall())

    if request.form.get('login'):
        if record:
            return render_template('account.html', full_name=record[0][1], login=record[0][2], password=record[0][3])
        else:
            if not username or not password:
                return render_template('login.html', error="Чо, самый умный?")
            else:
                return render_template('login.html', error="Пользователя не существует, либо пароль неверный")
    else:
        return render_template('login.html')


@app.route('/registration/', methods=['POST', 'GET'])
def registration():
    if request.method=='POST':
        full_name = request.form.get('name')
        login = request.form.get('login')
        password = request.form.get('password')

    if not full_name or not login or not password:
        return render_template('registration.html', error="Ну впиши хоть что-нибудь. ლಠ益ಠ)ლ")

    cursor.execute("SELECT * FROM users WHERE full_name=%s AND login=%s AND password=%s;", (str(full_name), str(login), str(password)))
    record = list(cursor.fetchall())

    if not record:
        cursor.execute('INSERT INTO users (full_name, login, password) VALUES (%s, %s, %s);', (str(full_name), str(login), str(password)))
        conn.commit()
        return redirect('/login/')
    else:
        return render_template('registration.html', error="Пользователь существует, иди на болото и кушай жабонят! ಠ_ಠ")

    return render_template('registration.html')
