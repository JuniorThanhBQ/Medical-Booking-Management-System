from flask import flash, jsonify, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user
from werkzeug.security import check_password_hash

from src import create_app, login
from src.extensions import db
from src.modules.auth_profiles.models import User
from src.utils.utils import check_xss_violation, validate_email_password

app = create_app()


@login.user_loader
def load_user(user_id):
    try:
        return db.session.get(User, int(user_id))
    except (ValueError, TypeError):
        return None


@app.route("/")
def index():
    return render_template("index.html")


@app.route('/login', methods=['GET', 'POST'])
def login_view():
    if request.method == 'POST':
        target = 'login_view'
        email = request.form.get('email')
        password = request.form.get('password')

        err_response = validate_email_password(email, password)
        user = User.query.filter(User.email == email).first()

        if check_xss_violation([email, password]):
            flash("Dữ liệu đầu vào chứa ký tự không hợp lệ.")

        elif err_response and isinstance(err_response, dict):
            flash(err_response.get("message", "Đã có lỗi xảy ra."))

        elif not user or not check_password_hash(user.password, password):
            flash("Tài khoản hoặc mật khẩu không đúng.")
        elif not user.is_active:
            flash("Tài khoản đang bị khóa.")
        else:
            login_user(user)
            target = 'admin.index' if (user.role and user.role.name == "ADMIN") else 'index'

        return redirect(url_for(target))

    return render_template('login.html')


@login_required
@app.route('/logout', methods=['GET', 'POST'])
def logout_view():
    logout_user()
    flash("Đăng xuất thành công.")
    return redirect(url_for('login_view'))


@app.route("/health")
def health_check():
    return jsonify({
        "status": "healthy",
        "message": "Backend đang chạy"
    }), 200


if __name__ == "__main__":
    app.run(host=app.config.get("HOST"), port=app.config.get("PORT"),
            debug=app.config.get("DEBUG"))
