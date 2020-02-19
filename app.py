import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from datetime import datetime
from os import path
if path.exists("env.py"):
    import env

app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get('MONGO_DBNAME') 
app.config["MONGO_URI"] = os.environ.get('MONGO_URI')
app.config["API_KEY"] = os.environ.get('API_KEY') 

mongo = PyMongo(app)

@app.route('/')
@app.route("/home")
def home():
    return render_template('home.html', 
                           movies=mongo.db.movies.find())


@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route('/reviews/<movie_id>', methods=["GET"])
def reviews(movie_id):
    return render_template("reviews.html", 
                           movie_id=movie_id, 
                           reviews=mongo.db.reviews.find( { 'movie_id': movie_id }))

@app.route("/addreview/<movie_id>")
def addreview(movie_id):
    return render_template('addreview.html', 
                            movie_id=movie_id,
                            categories=mongo.db.categories.find(),
                            ratings=mongo.db.ratings.find())

@app.route('/insertreview/<movie_id>', methods=["POST"])
def insertreview(movie_id):
    reviews = mongo.db.reviews
    post = {'username': request.form.get('username'),
            'movie_name': request.form.get('movie_name'),
            'category_name': request.form.get('category_name'),
            'description': request.form.get('description'),
            'review_rating': request.form.get('review_rating'),
            'review_date': datetime.now().strftime('%m/%d/%Y, %H:%M:%S'),
            'movie_id':  movie_id}
    reviews.insert_one(post)
    return render_template("reviews.html", movie_id=movie_id,
                           reviews=mongo.db.reviews.find( { 'movie_id': movie_id }))
    # return redirect(url_for("reviews"), reviews=mongo.db.reviews.find())

@app.route('/editreview/<review_id>/<movie_id>')
def editreview(review_id,movie_id):
    the_review =  mongo.db.reviews.find_one({"_id": ObjectId(review_id)})
    all_categories =  mongo.db.categories.find()
    return render_template('editreview.html', review=the_review, movie_id=movie_id,
                           categories=all_categories,
                           ratings=mongo.db.ratings.find())

@app.route('/updatereview/<review_id>/<movie_id>', methods=["POST"])
def updatereview(review_id,movie_id):
    reviews = mongo.db.reviews
    reviews.replace_one( {'_id': ObjectId(review_id)},
    {
        'username': request.form.get('username'),
        'movie_name': request.form.get('movie_name'),
        'category_name': request.form.get('category_name'),
        'description': request.form.get('description'),
        'review_rating': request.form.get('review_rating'),
        'review_date': datetime.now().strftime('%m/%d/%Y, %H:%M:%S'),
        'movie_id':  movie_id})
    return render_template("reviews.html", movie_id=movie_id,
                           reviews=mongo.db.reviews.find( { 'movie_id': movie_id }))

@app.route('/deletereview/<review_id>/<movie_id>')
def deletereview(review_id,movie_id):
    mongo.db.reviews.remove({'_id': ObjectId(review_id)})
    return render_template("reviews.html", movie_id=movie_id,
                           reviews=mongo.db.reviews.find( { 'movie_id': movie_id }))

@app.route("/search", methods=["GET"])
def search():
    return render_template('search.html', title='Search')

@app.route("/login")
def login():
    return render_template('login.html', title='Login')

@app.route("/signup")
def signup():
    return render_template('signup.html', title='Sign Up')


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=5000,
            debug=True)