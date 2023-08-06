from flask import Flask,render_template
import requests
from flask_caching import Cache

api_url = "https://jsonplaceholder.typicode.com/posts"

config = {
    "DEBUG": False,          # some Flask specific configs
    "CACHE_TYPE": "FileSystemCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300,
    "CACHE_DIR":"cache"
}

app = Flask(__name__)

app.config.from_mapping(config)
cache = Cache(app)

# GET - получение
# POST - отправка
# PUT - бновление
# DELETE - удаление

@app.route("/")
@cache.cached(timeout=60*60*24)
def index():
    posts = requests.get(api_url).json()
    return render_template("index.html",posts=posts)

@app.route("/<post_number>")
@cache.cached(timeout=60*60*24)
def one_post(post_number):
    post = requests.get(f'{api_url}/{post_number}').json()
    return render_template("post.html",post=post)

app.run()
