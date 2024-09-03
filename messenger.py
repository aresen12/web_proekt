import os
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from data import db_session
from data.user import User
from flask_login import current_user
from data.message import Message

mg = Blueprint('messenger', __name__, url_prefix='/m')


@mg.route("/<email_recipient>", methods=["GET", "POST"])
def m(email_recipient):
    if request.method == 'GET':
        if current_user.is_authenticated and current_user.admin:
            db_sess = db_session.create_session()
            emails = db_sess.query(User.email).all()
            print(emails)
            message = db_sess.query(Message).filter(Message.email_recipient == current_user.email).all()
            mes2 = db_sess.query(Message).filter(Message.email_sender == current_user.email).all()
            message = message + mes2
            # print(request.form["about"])
            print(message)
            message.sort(key=lambda x: x.time)
            for mess in message:
                if mess.email_recipient == current_user.email:
                    mess.read = True
            db_sess.commit()
            return render_template("form_admin.html", title='ответить', emails=emails, message=message,
                                   email_recipient=email_recipient)
        return render_template("forms.html", title='Заказать')
    elif request.method == "POST":
        f = request.files["img"]
        db_sess = db_session.create_session()
        if request.form["about"].strip() == "" and f.filename == "":
            return redirect('/m')
        mess = Message()
        db_sess.query(User).filter(User.email == current_user.email)
        mess.name_sender = current_user.name
        mess.email_sender = current_user.email
        mess.message = request.form["about"]
        if f.filename != "":
            os.chdir('static/img')
            dd = len(os.listdir())
            os.chdir("..")
            os.chdir("..")
            file = open(f"static/img/{dd}.jpg", mode="wb")
            file.write(f.read())
            file.close()
            mess.img = f"{dd}.jpg"
        mess.email_recipient = email_recipient
        db_sess.add(mess)
        db_sess.commit()
        if current_user.email != "evnomiya@yandex.ru":
            from send import get_text_messages
            log = get_text_messages(
                f'заказ\nИмя: {current_user.name} \nemail: {current_user.email}\n сообщение: {request.form["about"]}')
            print(log)
        return redirect(f'/m/{email_recipient}')


@mg.route("/update/<re>", methods=["GET", "POST"])
def m_update(re):
    if current_user.is_authenticated:
        db_sess = db_session.create_session()
        message = db_sess.query(Message).filter(Message.email_recipient == current_user.email).all()
        mes2 = db_sess.query(Message).filter(Message.email_sender == current_user.email).all()
        message = message + mes2
        message.sort(key=lambda x: x.time)
        print(message)
        return render_template("t.html", message=message, email_recipient=re)
    return render_template("t.html")


@mg.route("/", methods=["GET", "POST"])
def m_st():
    if request.method == 'GET':
        if not current_user.is_authenticated:
            return render_template("forms.html", title='Заказать')
        if current_user.is_authenticated and current_user.admin:
            db_sess = db_session.create_session()
            emails = db_sess.query(User.email).all()
            print(emails)
            return render_template("form_admin.html", title='ответить', emails=emails, email_recipient=0)
        db_sess = db_session.create_session()
        message = db_sess.query(Message).filter(Message.email_recipient == current_user.email).all()
        mes2 = db_sess.query(Message).filter(Message.email_sender == current_user.email).all()
        message = message + mes2
        message.sort(key=lambda x: x.time)
        for mess in message:
            if mess.email_recipient == current_user.email:
                mess.read = True
        db_sess.commit()
        return render_template("forms.html", title='Заказать', date="no date", message=message,
                               email_recipient="evnomiya@yandex.ru")
    elif request.method == "POST":
        print(str(
            request.files["img"]))
        if request.form["about"].strip() == "" and str(
                request.files["img"]) == "<FileStorage: '' (application/octet-stream)>":
            return redirect('/m')
        db_sess = db_session.create_session()
        mess = Message()
        db_sess.query(User).filter(User.email == current_user.email)
        mess.name_sender = current_user.name
        mess.email_sender = current_user.email
        mess.message = request.form["about"]
        print(request.files["img"])
        if str(request.files["img"]) != "<FileStorage: '' (application/octet-stream)>":
            os.chdir('static/img')
            dd = len(os.listdir())
            os.chdir("..")
            os.chdir("..")
            file = open(f"static/img/{dd}.jpg", mode="wb")
            file.write(request.files["img"].read())
            file.close()
            mess.img = f"{dd}.jpg"
        mess.email_recipient = "evnomiya@yandex.ru"
        db_sess.add(mess)
        db_sess.commit()
        if current_user.email != "evnomiya@yandex.ru":
            from send import get_text_messages
            log = get_text_messages(
                f'заказ\nИмя: {current_user.name} \nemail: {current_user.email}\n сообщение: {request.form["about"]}')
            print(log)
        return redirect('/m')