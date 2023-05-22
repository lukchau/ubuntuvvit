from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)

conn = psycopg2.connect(database="serice_db",
                        user="postgres",
                        password="MY_PASSWORD",
                        host="localhost",
                        port="5432")
cursor = conn.cursor()


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
            if request.form.get("login"):
                username = request.form.get('username')
                password = request.form.get('password')
                cursor.execute("SELECT * FROM service.users WHERE login=%s AND password=%s", (str(username), str(password)))
                records = list(cursor.fetchall())
                if len(records) != 0:
                    return render_template('account.html', full_name=records[0][1], login=records[0][2], password=records[0][3])
                if username == '' and password == '':
                    return render_template('login.html', empty='Поляяяяя не могут быть пустыми')
                return render_template('login.html', empty='Таких мы не знаем')
            elif request.form.get("registration"):
                return redirect("/registration/")
    return render_template('login.html')


@app.route('/registration/', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        name = request.form.get('name')
        login = request.form.get('login')
        password = request.form.get('password')
        cursor.execute("SELECT * FROM service.users WHERE login=%s", (str(login), ))
        check = len(cursor.fetchall())
        if check != 0:
            return render_template('registration.html', flag='Такой пользователь уже существует!!!')
        if name == '' or login == '' or password == '':
            return render_template('registration.html', flag='Поля не могут быть пустыми')
        cursor.execute('INSERT INTO service.users (full_name, login, password) VALUES (%s, %s, %s);', (str(name), str(login), str(password)))
        conn.commit()
        return redirect('/login/')
    return render_template('registration.html')