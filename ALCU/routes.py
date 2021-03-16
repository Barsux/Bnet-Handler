import os, json, time
from flask import Flask, render_template, request, redirect, flash, url_for
from fuzzywuzzy import process
from ALCU import db , app
from werkzeug.security import  check_password_hash
from ALCU.models import User
from flask_login import login_user, logout_user
power = [
            "включить компьютер",
            "включи компьютер",
            "я дома"
        ]
pcuseful = [
            'включи оперу',
            'включи дискорд',
            'включи стим',
            'включи ютуб',
            'выключи комп'
]
txt = ''
address = 0
num = 0
tie = 0
@app.route('/')
@app.route('/index')
def Center():
    return render_template("index.html")

@app.route('/IOTConnection',methods=['POST'])
def index():
    global txt,num,address, tie
    response = {
        'response': {
            'end_session': False
        }
    }
    response['response']['command'] = num
    response['response']['address'] = address
    response['response']['time'] = tie
    return json.dumps(response)


@app.route('/post', methods=['POST'])
def main():
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }
    handle_dialog(response, request.json)
    return json.dumps(response)

def handle_dialog(res,req):
    global address, num ,power, pcuseful, tie
    if req['request']['original_utterance']:
        s = req['request']['original_utterance'].lower()
        z = process.extractOne(s, power)
        if z[1] >= 80 and s != '':
            os.system("sudo etherwake -i enp3s0 70:85:c2:c8:bf:25 -D")
            print('Разбудил компьютер')
            res['response']['text'] = "Компьютер включен"
        else :
            z = process.extractOne(s, pcuseful)
            if z[1] >= 65:
                num = pcuseful.index(z[0])
                print(num, '  ', z[0])
                print(z[1])
                address = 1
                print('Пришло -', s, 'распознало -', z)
                res['response']['text'] = 'Распознано и принято'
                tie = time.time()
            else:
                print('Некорректный запрос')
                res['response']['text'] = 'Некорректный запрос'
@app.route('/login', methods=['GET','POST'])
def logins():
    login = request.form.get('login')
    psw = request.form.get('psw')
    if login and psw:
        user = User.query.filter_by(login = login).first()
        if user and psw:
            login_user(user)
            nextpage = request.args.get('next')
            redirect(nextpage)
            flash('Удача')
        else:
            flash("Логин или пароль некорректны")
    else:
        flash("Пожалуйста заполни все поля")
    return render_template('login.html')
@app.route('/logout', methods=['GET','POST'])
def logout():
    logout_user()
    return redirect(url_for('/'))

@app.route('/register', methods = ['GET','POST'])
def register():
    login = request.form.get('login')
    psw = request.form.get('psw')
    psw2 = request.form.get('psw2')
    email = request.form.get('email')
    if request.method == 'POST':
        if not (login or psw or psw2):
            flash('Пожалуйста заполни все поля')
        elif psw != psw2:
            flash('Пароли не совпадают')
        else:
            new_user = User(login = login,email = email, psw = psw)
            db.session.add(new_user)
            try : db.session.commit()
            except:
                flash('Схожие данные уже есть в системе')
            return redirect(url_for('logins'))
    return render_template('register.html')
@app.route('/profile', methods = ['GET','POST'])
def Profile():
    pass
@app.after_request
def redirect_to_singin(response):
    if response.status_code == 401:
        return redirect(url_for('logins') + '?next=' + request.url)
    return response