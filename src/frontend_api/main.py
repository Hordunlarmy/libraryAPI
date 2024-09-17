from decouple import config
from flask import Flask

app = Flask(__name__)


@app.route("/")
def read_root():
    return {"Hello": "This is the frontend API"}


if __name__ == "__main__":

    debug = config("DEBUG", default=False, cast=bool)
    app.run(debug=debug, host="0.0.0.0", port=8001)
