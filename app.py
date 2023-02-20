from re import A
from flask import Flask, render_template
from flask import jsonify, request
from flask_cors import CORS
import json
import requests
from flask_sqlalchemy import SQLAlchemy

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager 
from flask_avatars import Avatars

from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)


ENV="dev"

if ENV=="dev":
    app.debug=True
else:
    app.debug=False

app.debug=True    


app.config['SECRET_KEY'] = 'secret-key-goes-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:12345678@localhost/movie'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['DEBUG'] = True

avatars = Avatars(app)

cors = CORS(app)
db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'


app.app_context().push()




from models import User



def fetchdata():
    db.drop_all()
    print("Dropped all Tables")
    db.create_all()
    print("Created new Tables")
    db.session.commit()


@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))

from auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

# blueprint for non-auth parts of app
from main import main as main_blueprint
app.register_blueprint(main_blueprint)


from models import User 


if __name__ == '__main__':
    app.run(host="127.0.0.1", port="8080", threaded=True)
