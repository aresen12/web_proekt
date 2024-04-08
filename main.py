from flask import Flask, url_for, request, render_template
import json

app = Flask('213.87.139.94')


@app.route("/")
@app.route("/main.html")
def main_2():
    print(request.remote_addr)
    return render_template("main.html")


@app.route("/icon.html")
def icon():
    with open('config.json', encoding='utf-8') as file:
        news_list = json.loads(file.read())
        print(news_list)
        return render_template('icon_base.html', icons=news_list)


@app.route("/restv.html")
def restv():
    with open('restv.html', encoding='utf-8') as restv_f:
        return restv_f.read()


@app.route("/available.html")
def available():
    return render_template("available.html")


@app.route("/forms.html", methods=["GET", "POST"])
def form():
    if request.method == 'GET':
        return render_template("forms.html")
    elif request.method == "POST":
        from send import get_text_messages
        print(request.remote_addr)
        get_text_messages(
            f'заказ\nИмя: {request.form["name"]}\nemail: {request.form["email"]}\n сообщение: {request.form["about"]}')
        with open('ansver.html', encoding='utf-8') as file:
            return file.read()


if __name__ == "__main__":
    app.run(host='192.168.43.170')
