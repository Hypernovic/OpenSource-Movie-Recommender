from flask import Blueprint, render_template
from flask_login import login_required, current_user
from flask import jsonify, request
from models import User,MovieList
from flask_sqlalchemy import SQLAlchemy
from app import db
import recommendation

main = Blueprint('main', __name__)
@main.route('/')
def index():
    return render_template('base.html')



@main.route('/recommended', methods=['GET'])
@login_required
def recommended():
    list=MovieList.query.filter_by(userId=current_user.id).all()
    movieDict = []
    for movie in list:
        movieDict.append(movie.movieName)
    res = recommendation.results(movieDict)
    return jsonify(res)


@main.route('/favourites', methods=['GET'])
@login_required
def favourites():
    list=MovieList.query.filter_by(userId=current_user.id).all()
    movieDict = []
    for movie in list:
        movieDict.append(movie.toDict())
    return jsonify(movieDict)


@main.route('/dummy', methods=['GET'])
@login_required
def dummy():
    res = recommendation.giveDummy()
    return jsonify(res)

@main.route('/search',methods=["GET"])
@login_required
def search():
    res =recommendation.search(request.args.get('title'))
    print(res)
    return jsonify(res)


@main.route('/add', methods=["POST"])
@login_required
def add():
    movieName=(request.get_json("movieName")).get('movieName')
    moviePic=(request.get_json("moviePic")).get('moviePic')
    add= MovieList(userId=current_user.id, movieName=movieName.lower(),pic=moviePic)
    db.session.add(add)
    db.session.commit()
    return jsonify(status=200)


@main.route('/remove', methods=["POST"])
@login_required
def remove():
    movieName=(request.get_json("movieName")).get('movieName')
    MovieList.query.filter_by(userId=current_user.id,movieName=movieName.lower()).delete()
    db.session.commit()
    return jsonify(status=200)




