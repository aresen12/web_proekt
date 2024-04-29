from flask import Flask, request, render_template, redirect, abort
import json
from forms.login_form import LoginForm
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data import db_session
from data.user import User
from forms.register_form import RegisterForm
from podsob import load_json_config, load_json_config_restv
from forms.edit_email_form import EditEmailName
from forms.password_form import EditPassword

app = Flask(__name__)

app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.get(User, user_id)


@app.route("/")
@app.route("/main")
def main_2():
    return render_template("main.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User()
        user.name = form.name.data,
        user.email = form.email.data,
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route("/icon")
def icon():
    with open('config.json', encoding='utf-8') as file:
        news_list = json.loads(file.read())
        print(news_list)
        return render_template('icon_base.html', icons=news_list)


@app.route("/restv")
def restv():
    file = open('config_rest.json', encoding='utf-8')
    work_list = json.loads(file.read())
    print(work_list)
    file.close()
    return render_template('restv.html', restv=work_list)


@app.route("/available")
def available():
    return render_template("available.html")


@app.route("/forms", methods=["GET", "POST"])
def form_st():
    if request.method == 'GET':
        return render_template("forms.html")
    elif request.method == "POST":
        from send import get_text_messages
        get_text_messages(
            f'заказ\nИмя: {current_user.name} \nemail: {current_user.email}\n сообщение: {request.form["about"]}')
        return render_template("ansver.html")


@app.route("/edit/email", methods=["GET", "POST"])
def edit_email():
    form = EditEmailName()
    db_sess = db_session.create_session()
    if form.validate_on_submit():
        user = db_sess.query(User).filter(User.id == current_user.id).first()
        user.email = form.email.data
        user.name = form.name.data
        db_sess.commit()
        return redirect('/profile')
    else:
        form.email.data = current_user.email
        form.name.data = current_user.name
    return render_template("edit_name.html", form=form)


@app.route("/edit/name", methods=["GET", "POST"])
def edit_name():
    form = EditEmailName()
    db_sess = db_session.create_session()
    if form.validate_on_submit():
        user = db_sess.query(User).filter(User.id == current_user.id).first()
        user.email = form.email.data
        user.name = form.name.data
        db_sess.commit()
        return redirect('/profile')
    else:
        form.email.data = current_user.email
        form.name.data = current_user.name
    return render_template("edit_name.html", form=form)


@app.route("/edit/password", methods=["GET", "POST"])
def edit_password():
    form = EditPassword()
    db_sess = db_session.create_session()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('edit_password.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
    if form.validate_on_submit():
        user = db_sess.query(User).filter(User.id == current_user.id).first()
        if user.password != form.st_password.data:
            return render_template("edit_password.html", form=form, message="Неправильный старый пароль")
        if user is None:
            return redirect("/login")
        user.password = form.password.data
        db_sess.commit()
        return redirect('/profile')
    return render_template("edit_password.html", form=form)


@app.route("/api/add_work", methods=["GET", "POST"])
def add_work():
    if not current_user.admin:
        abort(404)
    if request.method == 'POST':
        f = request.files['file']
        csv_file = open("config.csv", encoding='utf-8')
        data = csv_file.readlines()
        file_out = open(f"static/img/icon{len(data)}.jpg", mode='wb')
        file_out.write(f.read())
        file_out.close()
        data.append(f"\nicon{len(data)};{request.form['about']};")
        csv_file.close()
        csv_file = open("config.csv", encoding='utf-8', mode="w", newline="")
        for _ in data:
            csv_file.writelines(_)
        csv_file.close()
        load_json_config()
        return render_template("ansver_work.html")
    if request.method == 'GET':
        return render_template('ad_work.html')


@app.route("/api/add_restv", methods=["GET", "POST"])
def add_retsv():
    if not current_user.admin:
        abort(404)
    if request.method == 'POST':
        f = request.files['file']
        f2 = request.files['file2']
        csv_file = open("config_rest.csv", encoding='utf-8')
        data = csv_file.readlines()
        file_out = open(f"static/img/restv{len(data)}.1.jpg", mode='wb')
        file_out.write(f.read())
        file_out.close()
        file_out = open(f"static/img/restv{len(data)}.2.jpg", mode='wb')
        file_out.write(f2.read())
        file_out.close()
        data.append(f"\nrestv{len(data)}.2.jpg;restv{len(data)}.1.jpg")
        csv_file.close()
        csv_file = open("config_rest.csv", encoding='utf-8', mode="w", newline="")
        for _ in data:
            csv_file.writelines(_)
        csv_file.close()
        load_json_config_restv()
        return render_template("add_restv.html")
    if request.method == 'GET':
        return render_template('add_restv.html')


@app.route("/profile")
def profile():
    return render_template("profile.html")


if __name__ == "__main__":
    db_session.global_init('db/icon_master.db')
    app.run(host='127.0.0.1')  # 192.168.43.170
    salt = "5gz"
    password = "raketa675"
    import hashlib

    data_base_password = password + salt
    hashed = hashlib.md5(data_base_password.encode())
    password = hashed.hexdigest()
