from flask import Flask, url_for

app = Flask(__name__)


@app.route("/")
def main():
    with open('main.html', encoding='utf-8') as file:
        return file.read()


@app.route("/main.html")
def main_2():
    with open('main.html', encoding='utf-8') as file:
        return file.read()


@app.route("/icon.html")
def icon():
    with open('icon.html', encoding='utf-8') as file:
        return file.read()


@app.route("/restv.html")
def restv():
    with open('restv.html', encoding='utf-8') as restv_f:
        return restv_f.read()


@app.route("/available.html")
def available():
    with open('available.html', encoding='utf-8') as available_f:
        return available_f.read()


@app.route("/forms.html")
def form():
    with open('forms.html', encoding='utf-8') as file:
        return file.read()


if __name__ == "__main__":
    app.run()
