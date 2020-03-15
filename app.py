import os
from flask import Flask, render_template, redirect, request, url_for, session, flash
from forms import RegistrationForm, LoginForm
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from datetime import datetime
from os import path
if path.exists("env.py"):
    import env

app = Flask(__name__)
# MongoDB config

app.config["MONGO_DBNAME"] = os.environ.get('MONGO_DBNAME') 
app.config["MONGO_URI"] = os.environ.get('MONGO_URI')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

mongo = PyMongo(app)

# Index and Home page to display a list of movies that have reviews 
@app.route('/')
@app.route("/home")
def home():
    if 'user' in session:
        profile_id = session['user']
    else:
        session['user'] = 'Guest'
    return render_template('home.html', 
                           first_movie=mongo.db.movies.find_one(), 
                           movies=mongo.db.movies.find().sort("last_updated", -1),
                           top_user=mongo.db.users.find().limit(1).sort("reviews_made", -1))

# About page 
@app.route("/about")
def about():
    return render_template('about.html',
                            first_movie=mongo.db.movies.find_one(),
                            top_user=mongo.db.users.find().limit(1).sort("reviews_made", -1))

# Reviews for a selected move from the home or search pages, if no reviews have been made you are taken to addreviews.
@app.route('/reviews/')
def reviews():
    tmdb_id = request.args.get('tmdb_id')
    reviews_exist = mongo.db.reviews.find_one({"tmdb_id" : tmdb_id})
    if reviews_exist:
        flash('You are logged on as ' + session['user'] , 'warning')
        return render_template("reviews.html", 
            tmdb_id=tmdb_id,
            profile_id = session['user'], 
            movie=mongo.db.movies.find_one({"tmdb_id" : tmdb_id}),
            reviews=mongo.db.reviews.find( { 'tmdb_id': tmdb_id }).sort("review_date", -1))
    else:
        flash('No reviews have been added, be the first.', 'warning')
        return render_template('addreview.html', 
            tmdb_id=tmdb_id,
            profile_id = session['user'],
            movie=mongo.db.movies.find_one({"tmdb_id" : tmdb_id}),
            categories=mongo.db.categories.find().sort("category_name", 1),
            ratings=mongo.db.ratings.find())

# Add review page has 2 collections used for select item listings
@app.route("/addreview/<tmdb_id>")
def addreview(tmdb_id):
    return render_template('addreview.html', 
            tmdb_id=tmdb_id,
            profile_id = session['user'],
            movie=mongo.db.movies.find_one({"tmdb_id" : tmdb_id}),
            categories=mongo.db.categories.find().sort("category_name", 1),
            ratings=mongo.db.ratings.find())
    
# One review is inserted to the reviews collection. The movie review count is incremented with the datetime stamp.
# The users collection reviews_made is alo increemented
@app.route("/insertreview", methods=["POST"])
def insertreview():
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
    mongo.db.users.update_one (
        {'username': session['user']},
        {'$inc': {'reviews_made': 1}}
    )
    flash('Review added successfully!', 'success')
    return render_template("reviews.html", 
        tmdb_id=tmdb_id,
        profile_id = session['user'], 
        movie=mongo.db.movies.find_one({"tmdb_id" : tmdb_id}),
        reviews=mongo.db.reviews.find( { 'tmdb_id': tmdb_id }).sort("review_date", -1))

# Edit review can only be access for your own reviews   
@app.route('/editreview/<review_id>/<tmdb_id>')
def editreview(review_id,tmdb_id):
    the_review =  mongo.db.reviews.find_one({"_id": ObjectId(review_id)})
    return render_template('editreview.html',
                    review=the_review,
                    tmdb_id=tmdb_id,
                    movie=mongo.db.movies.find_one({"tmdb_id" : tmdb_id}),
                    categories=mongo.db.categories.find().sort("category_name", 1),
                    ratings=mongo.db.ratings.find())
    
# Update review is triggered from the edit review page
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
    flash('Review updated successfully', 'success')
    return render_template("reviews.html", tmdb_id=tmdb_id,
                        profile_id = session['user'],
                        movie=mongo.db.movies.find_one({"tmdb_id" : tmdb_id}),
                        reviews=mongo.db.reviews.find( { 'tmdb_id': tmdb_id }).sort("review_date", -1))

# Delete confirm screen to ensure the review is not accidentally deleted
@app.route('/deleteconfirm/<review_id>/<tmdb_id>')
def deleteconfirm(review_id,tmdb_id):
    the_review =  mongo.db.reviews.find_one({"_id": ObjectId(review_id)})
    return render_template('deleteconfirm.html',
                    review=the_review,
                    tmdb_id=tmdb_id,
                    movie=mongo.db.movies.find_one({"tmdb_id" : tmdb_id}),
                    categories=mongo.db.categories.find().sort("category_name", 1),
                    ratings=mongo.db.ratings.find())

# The delete review is only displayed for your own reviews.
# The review is deleted from the reviews collection and movies collection count is reduced.
# The users reviews_made is also reduced, if no mre reviews exist then the movie is also deleted from the movies collection
@app.route('/deletereview/<review_id>/<tmdb_id>', methods=["POST"])
def deletereview(review_id,tmdb_id):
    the_review =  mongo.db.reviews.find_one({"_id": ObjectId(review_id)})
    mongo.db.reviews.delete_one({'_id': ObjectId(review_id)})
    mongo.db.movies.find_one_and_update(
        {'tmdb_id': tmdb_id},
        {'$inc': {'review_count': -1}}
    )
    mongo.db.users.find_one_and_update(
        {'username': session['user']},
        {'$inc': {'reviews_made': -1}}
    )
    reviews_exist = mongo.db.reviews.find_one({"tmdb_id" : tmdb_id})
    if reviews_exist:
        flash('Review deleted successfully!', 'success')
        return render_template("reviews.html", 
            tmdb_id=tmdb_id,
            profile_id = session['user'], 
            movie=mongo.db.movies.find_one({"tmdb_id" : tmdb_id}),
            reviews=mongo.db.reviews.find( { 'tmdb_id': tmdb_id }).sort("review_date", -1))
    else:
        flash('The last review was deleted succesfully!', 'success')
        mongo.db.movies.remove({'tmdb_id': tmdb_id})
        return render_template('home.html', 
            first_movie=mongo.db.movies.find_one(), 
            movies=mongo.db.movies.find().sort("last_updated", -1))

# Insert to the movies collection is made when a movie is selected and there are no reviews yet.
@app.route('/insertmovie', methods=['GET', 'POST'])
def insertmovie():
    tmdb_id = request.form.get('form_tmdb_id')
    movie_url = request.form.get('form_poster_url')
    movie_in_collection = mongo.db.movies.find_one({"tmdb_id" : tmdb_id})
    reviews_exist = mongo.db.reviews.find_one({"tmdb_id" : tmdb_id})
    if movie_in_collection:
        if reviews_exist:
            return render_template("reviews.html", 
                           tmdb_id=tmdb_id,
                           profile_id = session['user'], 
                           movie=mongo.db.movies.find_one({"tmdb_id" : tmdb_id}),
                           reviews=mongo.db.reviews.find( { 'tmdb_id': tmdb_id }).sort("review_date", -1))    
        else:
            flash('You are logged on as ' + session['user']+ ' there are no reviews, be the first.', 'warning')
            return render_template('addreview.html', 
                            tmdb_id=tmdb_id,
                            profile_id=session['user'],
                            movie=mongo.db.movies.find_one({"tmdb_id" : tmdb_id}),
                            categories=mongo.db.categories.find().sort("category_name", 1),
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
        flash('You logged on as ' + session['user'] + ' there are no reviews, be the first.', 'warning')
        return render_template('addreview.html', 
                            tmdb_id=tmdb_id,
                            profile_id= session['user'],
                            movie=mongo.db.movies.find_one({"tmdb_id" : tmdb_id}),
                            categories=mongo.db.categories.find().sort("category_name", 1),
                            ratings=mongo.db.ratings.find())  
    
# The cancelreview is reached from the addreview screen but the user decides not to add a review.
# If reviews exist then the reviews screen is displayed but if no reviews exist then the
# movie needs to be deleted from the movies collection .
@app.route('/cancelreview/<tmdb_id>')
def cancelreview(tmdb_id):
    reviews_exist = mongo.db.reviews.find_one({"tmdb_id" : tmdb_id})
    if reviews_exist:
        return render_template("reviews.html", 
            tmdb_id=tmdb_id, 
            profile_id=session['user'],
            movie=mongo.db.movies.find_one({"tmdb_id" : tmdb_id}),
            reviews=mongo.db.reviews.find( { 'tmdb_id': tmdb_id }).sort("review_date", -1))
    else:
        mongo.db.movies.remove({'tmdb_id': tmdb_id})
        return render_template('home.html', 
            first_movie=mongo.db.movies.find_one(), 
            movies=mongo.db.movies.find().sort("last_updated", -1))

# Search sets a default Guest login profile for anonymous users
@app.route("/search", methods=["GET"])
def search():
    if 'user' in session:
        profile_id = session['user']
    else:
        profile_id = 'Guest'
        session['user'] = 'Guest'
    return render_template('search.html',
                        first_movie=mongo.db.movies.find_one(),
                        top_user=mongo.db.users.find().limit(1).sort("reviews_made", -1))

#register page pops the user if the user wants to register as i decided to remove the logout functionality
@app.route("/register")
def register():
    if 'user' in session:
        session.pop('user')
    return render_template('register.html',
                            first_movie=mongo.db.movies.find_one(),
                            top_user=mongo.db.users.find().limit(1).sort("reviews_made", -1))

#registercheck does user validation and no password encryption is used as the project does not required authentification
@app.route('/registercheck', methods=['GET', 'POST'])
def registercheck():
    username = request.form.get('username')
    user_exists = mongo.db.users.find_one({"username" : username})
    if user_exists:
        flash('Username already exists, register with another username or go to Login' , 'danger')
        return render_template('register.html', 
            first_movie=mongo.db.movies.find_one(),
            top_user=mongo.db.users.find().limit(1).sort("reviews_made", -1))
    else:
        if request.form.get('password') == request.form.get('confirm_password'):
            users = mongo.db.users
            post = {'username': request.form.get('username'), 
                'password': request.form.get('password')
                }
            users.insert_one(post)
            session['user'] = username
            flash('Registered successfully and logged in as : ' + username, 'success')
            return render_template('home.html', 
                           first_movie=mongo.db.movies.find_one(), 
                           movies=mongo.db.movies.find().sort("last_updated", -1),
                           top_user=mongo.db.users.find().limit(1).sort("reviews_made", -1))
        else:
            flash('Login Unsuccessful. Both passwords need to match', 'danger')
            return render_template('register.html',
                            first_movie=mongo.db.movies.find_one(),
                            top_user=mongo.db.users.find().limit(1).sort("reviews_made", -1))


#login page pops the user if the user wants to register as i decided to remove the logout functionality
@app.route("/login")
def login():
    if 'user' in session:
        session.pop('user')
    return render_template('login.html',
                            first_movie=mongo.db.movies.find_one(),
                            top_user=mongo.db.users.find().limit(1).sort("reviews_made", -1))

#logincheck does user validation and no password encryption is used as the project does not required authentification
@app.route('/logincheck', methods=['GET', 'POST'])
def logincheck():
    username = request.form.get('username')
    password = request.form.get('password')
    user_exists = mongo.db.users.find_one({"username" : username})
    if user_exists:
        if user_exists['password'] == request.form.get('password'):
                session['user'] = username
                flash('Logged in successfully as : ' + username, 'success')
                return render_template('home.html', 
                        first_movie=mongo.db.movies.find_one(), 
                        movies=mongo.db.movies.find().sort("last_updated", -1),
                        top_user=mongo.db.users.find().limit(1).sort("reviews_made", -1))
        else:
            flash('Login Unsuccessful. Please check password', 'danger')
            return render_template('login.html',
                            first_movie=mongo.db.movies.find_one(),
                            top_user=mongo.db.users.find().limit(1).sort("reviews_made", -1)) 
    else:
        flash('Login Unsuccessful. Please check username and password', 'danger')
        return render_template('login.html',
                            first_movie=mongo.db.movies.find_one(),
                            top_user=mongo.db.users.find().limit(1).sort("reviews_made", -1)) 

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=5000,
            debug=True)