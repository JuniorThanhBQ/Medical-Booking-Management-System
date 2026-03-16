from flask import Blueprint, flash, render_template, request

from modules.users.services import login

users_bp = Blueprint("users", __name__)


@users_bp.route("/login", methods=["GET", "POST"])
def login_view():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = login(username, password)

        if user:
            return render_template("index.html")

        flash("Sai tài khoản hoặc mật khẩu!")

    return render_template("login.html")
