import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
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
    return render_template('home.html')


@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route('/reviews')
def reviews():
    return render_template("reviews.html", 
                           reviews=mongo.db.reviews.find())

@app.route("/addreview")
def addreview():
    return render_template('addreview.html',
                           categories=mongo.db.categories.find())

@app.route('/insertreview', methods=['POST'])
def insertreview():
    reviews = mongo.db.reviews
    reviews.insert_one(request.form.to_dict())
    return redirect(url_for('reviews'))

@app.route('/editreview/<review_id>')
def editreview(review_id):
    the_review =  mongo.db.reviews.find_one({"_id": ObjectId(review_id)})
    all_categories =  mongo.db.categories.find()
    return render_template('editreview.html', review=the_review,
                           categories=all_categories)    

@app.route("/search")
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