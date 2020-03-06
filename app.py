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

mongo = PyMongo(app)

@app.route('/')
@app.route("/home")
def home():
    return render_template('home.html', 
                           first_movie=mongo.db.movies.find_one(), 
                           movies=mongo.db.movies.find().sort("last_updated", -1))


@app.route("/about")
def about():
    return render_template('about.html',
                            first_movie=mongo.db.movies.find_one(),
                            title='About')

@app.route('/reviews/<tmdb_id>', methods=["GET"])
def reviews(tmdb_id):
    reviews_exist = mongo.db.reviews.find_one({"tmdb_id" : tmdb_id})
    if reviews_exist:
        return render_template("reviews.html", 
            tmdb_id=tmdb_id, 
            movie=mongo.db.movies.find_one({"tmdb_id" : tmdb_id}),
            reviews=mongo.db.reviews.find( { 'tmdb_id': tmdb_id }).sort("review_date", -1))
    else:
        return render_template('addreview.html', 
            tmdb_id=tmdb_id,
            movie=mongo.db.movies.find_one({"tmdb_id" : tmdb_id}),
            categories=mongo.db.categories.find(),
            ratings=mongo.db.ratings.find())

@app.route("/addreview/<tmdb_id>")
def addreview(tmdb_id):
    return render_template('addreview.html', 
        tmdb_id=tmdb_id,
        movie=mongo.db.movies.find_one({"tmdb_id" : tmdb_id}),
        categories=mongo.db.categories.find(),
        ratings=mongo.db.ratings.find())

@app.route("/insertreview/<tmdb_id>", methods=["POST"])
def insertreview(tmdb_id):
    reviews = mongo.db.reviews
    tmdb_id = request.form.get('tmdb_id')
    review_date = datetime.now().strftime('%d/%m/%Y, %H:%M:%S')
    post = {'username': request.form.get('username'),
            'movie_title': request.form.get('movie_title'),
            'category_name': request.form.get('category_name'),
            'description': request.form.get('description'),
            'review_rating': request.form.get('review_rating'),
            'review_date': review_date,
            'tmdb_id':  request.form.get('tmdb_id')}
    reviews.insert_one(post)

    mongo.db.movies.update_one (
        {'tmdb_id': tmdb_id},
        {'$inc': {'review_count': 1}}
    )
    mongo.db.movies.update_one (
        {'tmdb_id': tmdb_id},
        {'$set': {'last_updated': review_date}}
    )

    return render_template("reviews.html", 
        tmdb_id=tmdb_id, 
        movie=mongo.db.movies.find_one({"tmdb_id" : tmdb_id}),
        reviews=mongo.db.reviews.find( { 'tmdb_id': tmdb_id }).sort("review_date", -1))
    # return redirect(url_for("reviews"), reviews=mongo.db.reviews.find())

@app.route('/editreview/<review_id>/<tmdb_id>')
def editreview(review_id,tmdb_id):
    the_review =  mongo.db.reviews.find_one({"_id": ObjectId(review_id)})
    all_categories =  mongo.db.categories.find()
    return render_template('editreview.html',
                           review=the_review,
                           tmdb_id=tmdb_id,
                           movie=mongo.db.movies.find_one({"tmdb_id" : tmdb_id}),
                           categories=all_categories,
                           ratings=mongo.db.ratings.find())

@app.route('/updatereview/<review_id>/<tmdb_id>', methods=["POST"])
def updatereview(review_id,tmdb_id):
    reviews = mongo.db.reviews
    reviews.replace_one( {'_id': ObjectId(review_id)},
    {
        'username': request.form.get('username'),
        'movie_title': request.form.get('movie_title'),
        'category_name': request.form.get('category_name'),
        'description': request.form.get('description'),
        'review_rating': request.form.get('review_rating'),
        'review_date': datetime.now().strftime('%d/%m/%Y, %H:%M:%S'),
        'tmdb_id':  tmdb_id})
    return render_template("reviews.html", tmdb_id=tmdb_id,
                           reviews=mongo.db.reviews.find( { 'tmdb_id': tmdb_id }))

@app.route('/deletereview/<review_id>/<tmdb_id>')
def deletereview(review_id,tmdb_id):
    mongo.db.reviews.remove({'_id': ObjectId(review_id)})

    mongo.db.movies.find_one_and_update(
        {'tmdb_id': tmdb_id},
        {'$inc': {'review_count': -1}}
    )

    return render_template("reviews.html",
        tmdb_id=tmdb_id,
        reviews=mongo.db.reviews.find( { 'tmdb_id': tmdb_id }))

@app.route('/insertmovie', methods=["POST"])
def insertmovie():
    tmdb_id = request.form.get('form_tmdb_id')
    movie_url = request.form.get('form_poster_url')
    movie_in_collection = mongo.db.movies.find_one({"tmdb_id" : tmdb_id})
    reviews_exist = mongo.db.reviews.find_one({"tmdb_id" : tmdb_id})
    if movie_in_collection:
        if reviews_exist:
            return render_template("reviews.html", 
                           tmdb_id=tmdb_id, 
                           movie=mongo.db.movies.find_one({"tmdb_id" : tmdb_id}),
                           reviews=mongo.db.reviews.find( { 'tmdb_id': tmdb_id }).sort("review_date", -1))    
        else:
            return render_template('addreview.html', 
                            tmdb_id=tmdb_id,
                            movie=mongo.db.movies.find_one({"tmdb_id" : tmdb_id}),
                            categories=mongo.db.categories.find(),
                            ratings=mongo.db.ratings.find())        
    else:
        movies = mongo.db.movies
        post = {'tmdb_id': request.form.get('form_tmdb_id'), 
                'movie_title': request.form.get('form_movie_title'),
                'url': request.form.get('form_poster_url'),
                'overview': request.form.get('form_movie_overview'),
                'release_date': request.form.get('form_release_date'),
                'vote_average': request.form.get('form_vote_average'),
                'last_updated': datetime.now().strftime('%m/%d/%Y, %H:%M:%S'),
                'review_count':0
                }
        movies.insert_one(post)
        return render_template('addreview.html', 
                            tmdb_id=tmdb_id,
                            movie=mongo.db.movies.find_one({"tmdb_id" : tmdb_id}),
                            categories=mongo.db.categories.find(),
                            ratings=mongo.db.ratings.find())
    


@app.route("/search", methods=["GET"])
def search():

    return render_template('search.html',
                        first_movie=mongo.db.movies.find_one(),
                        title='Search')

@app.route("/login")
def login():
    return render_template('login.html',
                            first_movie=mongo.db.movies.find_one(),
                            title='Login')

@app.route("/signup")
def signup():
    return render_template('signup.html',
                            first_movie=mongo.db.movies.find_one(),
                            title='Sign Up')


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=5000,
            debug=True)