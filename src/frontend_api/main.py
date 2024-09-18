from decouple import config
from flask import Flask
from modules.book.blueprint import book_blueprint
from modules.user.blueprint import user_blueprint

app = Flask(__name__)


@app.route("/")
def read_root():
    return {"Hello": "This is the frontend API"}


app.register_blueprint(user_blueprint, url_prefix="/api/users")
app.register_blueprint(book_blueprint, url_prefix="/api/books")


if __name__ == "__main__":

    debug = config("DEBUG", default=False, cast=bool)
    app.run(debug=debug, host="0.0.0.0", port=8001)
