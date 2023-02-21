from flask import Flask
from flask_cors import CORS

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager 

app = Flask(__name__)



app.config['SECRET_KEY'] = 'secret-key-goes-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://movierecommender_user:CGdtNqRjii9ZuCF3EQuwSTzGH55rXFSF@dpg-cfpri0h4rebfdaveb890-a/movierecommender'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False


cors = CORS(app)
db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'






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
