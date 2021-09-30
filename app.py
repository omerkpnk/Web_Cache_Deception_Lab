from flask import Flask,redirect, render_template,session,request
from flask_caching import Cache
from random import randint
from werkzeug.routing import BaseConverter
from datetime import timedelta
import flask
cache = Cache()

app = Flask(__name__)
app.config['CACHE_TYPE'] = 'simple'
app.secret_key = "SuperSecretKey!"
app.permanent_session_lifetime = timedelta(minutes=5)

cache.init_app(app)


class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


app.url_map.converters['regex'] = RegexConverter

@app.route('/login', methods=["POST", "GET"])
def index():
    if request.method == "POST":
        session.permanent = True
        user = request.form["username"]
        session["user"] = user 
        return redirect("/profile")
    else:
        if "user" in session:
            return redirect("/profile")
    return render_template("login.html")

@app.route('/profile')
def profile():
    if "user" in session:
        user = session["user"]
        random = randint(1, 100)
        resp = flask.Response(render_template("profile.html", balance = random, username = user))
        resp.headers["Cache-Control"] = "no-store, no-cache"
        return resp    
    else:
        return redirect("/login")

@app.route('/<regex("profile.*"):url>')
@cache.cached()
def cached(url):
    if "user" in session:
        user = session["user"]
        random = randint(1, 100)
        resp = flask.Response(render_template("profile.html", balance = random, username = user))
        resp.headers["Cache-Control"] = "no-store, no-cache"
        return resp    
    else:
        return redirect("/login")

@app.route('/')
def main():
    return redirect("/login")

if __name__ == '__main__':
    app.run(debug=True)
