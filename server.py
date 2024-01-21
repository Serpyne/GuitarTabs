from flask import Flask, request, render_template
from flask_cors import CORS
import json
import requests
import re
import os
from threading import Thread
import logging

app = Flask(__name__)
CORS(app)

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


def site_url():
    repl_id = os.getenv("REPL_ID")
    return f"https://{repl_id}-00-1dv7zsxzm37hz.picard.replit.dev/tabs"


def is_url(text):
    if re.search(r"https://", text) or re.search(r"http://", text):
        return True
    if re.search(r"kemono.su/", text):
        return True
    if re.search(r"drive.google.com/", text):
        return True


def get_tabs_json():
    with open("static/tabs.json", "r") as f:
        data = json.load(f)

    return data


def add_tab(name, url):

    data = get_tabs_json()

    database = data["db"]

    if name not in database:
        database[name] = url
    data["db"] = database

    with open("static/tabs.json", "w") as f:
        json.dump(data, f, indent=4, sort_keys=True)


def find_tab_url(url):

    if re.search(r"drive.google.com/", url):
        response = requests.get(url)
        html = response.text

        title = re.search(r'<title>(.+?)</title>', html).group(1)
        return title, url

    elif re.search(r"kemono.su/", url):
        response = requests.get(url)
        html = response.text

        title = re.search("<span>(.+?)</span>", html).group(1)
        regex = re.search(r'"(https://drive.google.com/file.+?)"', html)
        if regex:
            pdf_url = regex.group(1)
        else:
            pdf_url = ""
            print(url + " is fucked")

        return title, pdf_url

    else:
        return None


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/tabs', methods=("GET", "POST"))
def tabs():

    with open("static/tabs.json", "r") as f:
        data = json.load(f)
        db = data["db"]

    if request.method == "POST":
        url = request.form["url"]

        if is_url(url):
            name, tab_url = find_tab_url(url)
            add_tab(name, tab_url)

            return render_template("tabs.html", tabs=db, success=True)

        else:
            return render_template("tabs.html", tabs=db, success=False)

    return render_template("tabs.html", tabs=db)


@app.route('/about')
def about():
    return render_template("about.html")


def run():
    app.run(host='0.0.0.0', debug=False)


def start():
    # thread = Thread(target=run)
    # thread.start()
    run()


if __name__ == "__main__":
    start()
