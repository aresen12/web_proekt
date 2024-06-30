import os
from flask import Flask, request, render_template, redirect, abort
import json
from forms.login_form import LoginForm
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data import db_session
from data.user import User
from data.message import Message
from data.product import Product
from forms.register_form import RegisterForm
from podsob import load_json_config, load_json_config_restv
from forms.edit_email_form import EditEmailName
from forms.password_form import EditPassword
import hashlib
import csv

app = Flask(__name__)

app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
hash_password = '7cb8fa366d774761d198d3dc6244740c'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.get(User, user_id)


@app.route("/")
@app.route("/main")
def main_2():
    return render_template("main.html", title='главная')


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


@app.route('/api')
def api():
    return redirect('/')


@app.route('/carousel/<icon_name>')
def carousel(icon_name):
    file = open("config.csv", encoding="utf-8")
    reader = csv.DictReader(file, delimiter=';', quotechar='"')
    data = list(reader)
    index = 0
    n = len(data)
    for i in range(n):
        if data[i]['file'] == icon_name:
            index = i
    left = index - 1
    if index + 1 < n:
        right = index + 1
    else:
        right = 0
    file.close()
    return render_template("carousel.html", title='Иконы', name=icon_name, left=data[left]['file'],
                           right=data[right]['file'])


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
        user.name = form.name.data
        user.email = form.email.data
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
        return render_template('icon_base.html', title='иконы', icons=news_list)


@app.route("/restv")
def restv():
    file = open('config_rest.json', encoding='utf-8')
    work_list = json.loads(file.read())
    print(work_list)
    file.close()
    return render_template('restv.html', restv=work_list, title='реставрация')


@app.route("/available")
def available():
    db_sess = db_session.create_session()
    data = db_sess.query(Product).all()
    return render_template("available.html", title='В наличии', icons=data)


@app.route("/product/<name>", methods=['GET'])
def product_watch(name):
    db_sess = db_session.create_session()
    item = db_sess.query(Product).filter(Product.main_img == name).first()
    item: Product
    if not item.img_list is None:
        list_img = item.img_list.split()
    else:
        list_img = []
    return render_template("product.html", item=item, title=item.name, list_img=list_img)


@app.route("/del_got/<icon_>", methods=["DELETE", 'GET'])
def del_got(icon_):
    if current_user.is_authenticated and current_user.admin:
        db_sess = db_session.create_session()
        pr = db_sess.query(Product).filter(Product.main_img == icon_).first()
        db_sess.delete(pr)
        db_sess.commit()
        return redirect("/available")
    abort(404)


@app.route("/forms", methods=["GET", "POST"])
def form_st():
    if request.method == 'GET':
        if not current_user.is_authenticated:
            return render_template("forms.html", title='Заказать')
        if current_user.is_authenticated and current_user.admin:
            db_sess = db_session.create_session()
            emails = db_sess.query(User.email).all()
            print(emails)
            return render_template("form_admin.html", title='ответить', emails=emails)
        db_sess = db_session.create_session()
        message = db_sess.query(Message).filter(Message.email_recipient == current_user.email).all()
        mes2 = db_sess.query(Message).filter(Message.email_sender == current_user.email).all()
        message = message + mes2
        message.sort(key=lambda x: x.time)
        return render_template("forms.html", title='Заказать', message=message, email_recipient="evnomiya@yandex.ru")
    elif request.method == "POST":
        if request.form["about"].strip() == "":
            return redirect('/forms')
        db_sess = db_session.create_session()
        mess = Message()
        db_sess.query(User).filter(User.email == current_user.email)
        mess.name_sender = current_user.name
        mess.email_sender = current_user.email
        mess.message = request.form["about"]
        mess.email_recipient = "evnomiya@yandex.ru"
        db_sess.add(mess)
        db_sess.commit()
        if current_user.email != "evnomiya@yandex.ru":
            from send import get_text_messages
            log = get_text_messages(
                f'заказ\nИмя: {current_user.name} \nemail: {current_user.email}\n сообщение: {request.form["about"]}')
            print(log)
        return redirect('/forms')


@app.route("/forms/<email_recipient>", methods=["GET", "POST"])
def form_admin(email_recipient):
    if request.method == 'GET':
        if current_user.admin:
            db_sess = db_session.create_session()
            emails = db_sess.query(User.email).all()
            print(emails)
            message = db_sess.query(Message).filter(Message.email_recipient == current_user.email).all()
            mes2 = db_sess.query(Message).filter(Message.email_sender == current_user.email).all()
            message = message + mes2
            # print(request.form["about"])
            print(message)
            message.sort(key=lambda x: x.time)
            return render_template("form_admin.html", title='ответить', emails=emails, message=message,
                                   email_recipient=email_recipient)
        return render_template("forms.html", title='Заказать')
    elif request.method == "POST":
        db_sess = db_session.create_session()
        if request.form["about"].strip() == "":
            return redirect('/forms')
        mess = Message()
        db_sess.query(User).filter(User.email == current_user.email)
        mess.name_sender = current_user.name
        mess.email_sender = current_user.email
        mess.message = request.form["about"]
        mess.email_recipient = email_recipient
        db_sess.add(mess)
        db_sess.commit()
        if current_user.email != "evnomiya@yandex.ru":
            from send import get_text_messages
            log = get_text_messages(
                f'заказ\nИмя: {current_user.name} \nemail: {current_user.email}\n сообщение: {request.form["about"]}')
            print(log)
        return redirect(f'/forms/{email_recipient}')


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
    return render_template("edit_name.html", form=form, title='Профиль')


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
    return render_template("edit_name.html", form=form, title='Профиль')


@app.route("/edit/password", methods=["GET", "POST"])
def edit_password():
    form = EditPassword()
    db_sess = db_session.create_session()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('edit_password.html', title='Изменение пароля',
                                   form=form,
                                   message="Пароли не совпадают")
    if form.validate_on_submit():
        user = db_sess.query(User).filter(User.id == current_user.id).first()
        if not user.check_password(form.st_password.data):
            return render_template("edit_password.html", form=form, title='профиль',
                                   message="Неправильный старый пароль")
        if user is None:
            return redirect("/login")
        user.set_password(form.password.data)
        db_sess.commit()
        return redirect('/profile')
    return render_template("edit_password.html", form=form, title='Изменение пароля')


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


@app.route("/api/add_got_icon/<int:i>", methods=["GET", "POST"])
def add_work_got(i):
    if not current_user.admin:
        abort(404)
    if request.method == 'POST':
        db_sess = db_session.create_session()
        pr = Product()
        list_img = ''
        for j in range(i):
            f = request.files[f'file{j}']
            os.chdir('static/img')
            dd = len(os.listdir())
            os.chdir("..")
            os.chdir("..")
            file_out = open(f"static/img/product{dd}.jpg", mode='wb')
            file_out.write(f.read())
            file_out.close()
            if j == 0:
                pr.main_img = f'product{dd}'
                list_img += f'product{dd}'
            else:
                list_img += f' product{dd}'
        pr.about = request.form['about']
        pr.img_list = list_img
        pr.prise = request.form['prise']
        pr.name = request.form['name']
        db_sess.add(pr)
        db_sess.commit()
        return render_template("ansver_work.html")
    if request.method == 'GET':
        return render_template('add_product.html', title="Добавление продукта", i=i)


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
    db_sess = db_session.create_session()
    message = db_sess.query(Message).filter(
        Message.email_recipient == current_user.email).all()
    mes2 = db_sess.query(Message).filter(Message.email_sender == current_user.email).all()
    message = message + mes2
    print(message)
    return render_template("profile.html", title='Профиль', message=message)


@app.route("/api/add_admin/<password>")
def add_admin(password):
    salt = "5gz"
    data_base_password = password + salt
    hashed = hashlib.md5(data_base_password.encode())
    password = hashed.hexdigest()
    if password == hash_password and current_user.is_authenticated:
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == current_user.id).first()
        user.admin = 1
        db_sess.commit()
        return {"log": 'True'}


if __name__ == "__main__":
    db_session.global_init('db/icon_master.db')
    app.run(host='192.168.43.170', debug=True)  # 192.168.43.170
