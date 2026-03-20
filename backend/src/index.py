from flask import render_template
from src import create_app, login
from src.modules.users.services import get_user_loader

app = create_app()


@login.user_loader
def load_user(user_id):
    return get_user_loader(user_id)


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(
        host=app.config.get("HOST"),
        port=app.config.get("PORT"),
        debug=app.config.get("RUN_MODE"),
    )
