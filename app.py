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

app.config["MONGO_DBNAME"] = os.environ.get('MONGO_DBNAME') 
app.config["MONGO_URI"] = os.environ.get('MONGO_URI')
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

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

@app.route('/reviews/')
def reviews():
    tmdb_id = request.args.get('tmdb_id')
    reviews_exist = mongo.db.reviews.find_one({"tmdb_id" : tmdb_id})
    if reviews_exist:
        return render_template("reviews.html", 
            tmdb_id=tmdb_id, 
            movie=mongo.db.movies.find_one({"tmdb_id" : tmdb_id}),
            reviews=mongo.db.reviews.find( { 'tmdb_id': tmdb_id }).sort("review_date", -1))
            
    else:
        flash('No reviews have been added, be the first.', 'warning')
        return render_template('addreview.html', 
            tmdb_id=tmdb_id,
            movie=mongo.db.movies.find_one({"tmdb_id" : tmdb_id}),
            categories=mongo.db.categories.find(),
            ratings=mongo.db.ratings.find())

@app.route("/addreview/<tmdb_id>")
def addreview(tmdb_id):
    if 'user' in session:
        flash('Logged in successfully as : ' + session['user'], 'success')
        return render_template('addreview.html', 
            tmdb_id=tmdb_id,
            movie=mongo.db.movies.find_one({"tmdb_id" : tmdb_id}),
            categories=mongo.db.categories.find(),
            ratings=mongo.db.ratings.find())
    else:
        flash('Login or Sign up to add a review!', 'warning')
        return render_template('login.html',
                            first_movie=mongo.db.movies.find_one())


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
    flash('Review added successfully!', 'success')
    return render_template("reviews.html", 
        tmdb_id=tmdb_id, 
        movie=mongo.db.movies.find_one({"tmdb_id" : tmdb_id}),
        reviews=mongo.db.reviews.find( { 'tmdb_id': tmdb_id }).sort("review_date", -1))
    

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
    flash('Review updated successfully', 'success')
    return render_template("reviews.html", tmdb_id=tmdb_id,
                           movie=mongo.db.movies.find_one({"tmdb_id" : tmdb_id}),
                           reviews=mongo.db.reviews.find( { 'tmdb_id': tmdb_id }))

@app.route('/deletereview/<review_id>/<tmdb_id>', methods=["POST"])
def deletereview(review_id,tmdb_id):
    mongo.db.reviews.delete_one({'_id': ObjectId(review_id)})

    mongo.db.movies.find_one_and_update(
        {'tmdb_id': tmdb_id},
        {'$inc': {'review_count': -1}}
    )
    reviews_exist = mongo.db.reviews.find_one({"tmdb_id" : tmdb_id})
    if reviews_exist:
        flash('Review deleted successfully!', 'success')
        return render_template("reviews.html", 
            tmdb_id=tmdb_id, 
            movie=mongo.db.movies.find_one({"tmdb_id" : tmdb_id}),
            reviews=mongo.db.reviews.find( { 'tmdb_id': tmdb_id }).sort("review_date", -1))
    else:
        flash('The last review was deleted', 'success')
        mongo.db.movies.remove({'tmdb_id': tmdb_id})
        return render_template('home.html', 
            first_movie=mongo.db.movies.find_one(), 
            movies=mongo.db.movies.find().sort("last_updated", -1))

    
    
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
                           movie=mongo.db.movies.find_one({"tmdb_id" : tmdb_id}),
                           reviews=mongo.db.reviews.find( { 'tmdb_id': tmdb_id }).sort("review_date", -1))    
        else:
            flash('No reviews have been added, be the first.', 'warning')
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
        flash('No reviews have been added, be the first.', 'warning')
        return render_template('addreview.html', 
                            tmdb_id=tmdb_id,
                            movie=mongo.db.movies.find_one({"tmdb_id" : tmdb_id}),
                            categories=mongo.db.categories.find(),
                            ratings=mongo.db.ratings.find())  
    

@app.route('/cancelreview/<tmdb_id>')
def cancelreview(tmdb_id):
    reviews_exist = mongo.db.reviews.find_one({"tmdb_id" : tmdb_id})
    if reviews_exist:
        return render_template("reviews.html", 
            tmdb_id=tmdb_id, 
            movie=mongo.db.movies.find_one({"tmdb_id" : tmdb_id}),
            reviews=mongo.db.reviews.find( { 'tmdb_id': tmdb_id }).sort("review_date", -1))
    else:
        mongo.db.movies.remove({'tmdb_id': tmdb_id})
        return render_template('home.html', 
            first_movie=mongo.db.movies.find_one(), 
            movies=mongo.db.movies.find().sort("last_updated", -1))


@app.route("/search", methods=["GET"])
def search():

    return render_template('search.html',
                        first_movie=mongo.db.movies.find_one(),
                        title='Search')

@app.route("/register")
def register():
   return render_template('register.html',
                            first_movie=mongo.db.movies.find_one())

@app.route('/registercheck', methods=['GET', 'POST'])
def registercheck():
    username = request.form.get('username')
    user_exists = mongo.db.users.find_one({"username" : username})
    if user_exists:
        flash('Username already exists, register with another username or go to Login' , 'danger')
        return render_template('register.html', 
            first_movie=mongo.db.movies.find_one())   

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
                           movies=mongo.db.movies.find().sort("last_updated", -1))
   
        else:
            flash('Login Unsuccessful. Both passwords need to match', 'danger')
            return render_template('register.html',
                            first_movie=mongo.db.movies.find_one()) 



@app.route("/login")
def login():
   return render_template('login.html',
                            first_movie=mongo.db.movies.find_one())

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
                        movies=mongo.db.movies.find().sort("last_updated", -1))   
        else:
            flash('Login Unsuccessful. Please check password', 'danger')
            return render_template('login.html',
                            first_movie=mongo.db.movies.find_one())        
    else:
        flash('Login Unsuccessful. Please check username and password', 'danger')
        return render_template('login.html',
                            first_movie=mongo.db.movies.find_one())

@app.route('/logout')
def logout():
    if 'user' in session:
        session.pop('user')
        flash("Successfully logged out!", 'success')                        
        return render_template('home.html', 
                           first_movie=mongo.db.movies.find_one(), 
                           movies=mongo.db.movies.find().sort("last_updated", -1))
    else:
        flash("No user logged on!", 'warning')                        
        return render_template('home.html', 
                           first_movie=mongo.db.movies.find_one(), 
                           movies=mongo.db.movies.find().sort("last_updated", -1))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=5000,
            debug=True)