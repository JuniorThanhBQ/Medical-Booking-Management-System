from flask import Flask, redirect, render_template, url_for

from modules.users.views import users_bp

app = Flask(__name__)
app.secret_key = "abc123"

app.register_blueprint(users_bp)


@app.route("/")
def index():
    return redirect(url_for("users.login_view"))


@app.route("/admin")
def admin():
    return render_template("admin/index.html")


if __name__ == "__main__":
    app.run(debug=True)
