import pytest
from flask import Flask, jsonify

from src.extensions import db


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SECRET_KEY"] = "never-said-never-never-ever-here-we-go"
    db.init_app(app)

    @app.route("/")
    def index():
        return "OK", 200

    @app.route("/health")
    def health_check():
        return jsonify({
            "status": "good",
            "message": "Backend đã chạy"
        }), 200

    return app


@pytest.fixture
def test_app():
    app = create_app()

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()
        db.engine.dispose()


@pytest.fixture
def test_session(test_app):
    with test_app.app_context():
        yield db.session
        db.session.rollback()
        db.session.remove()
