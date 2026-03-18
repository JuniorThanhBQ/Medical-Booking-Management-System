from flask import Flask
from src.modules.users.models import db
from src.modules.users.views import api

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3' # sẽ update migrate sau
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
app.register_blueprint(api)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True,port="5050")