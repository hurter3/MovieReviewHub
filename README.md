# Code Institute


# **Table of Contents**

- [**Table of Contents**](#table-of-contents)
	- [**Movie Review Hub**](#moviereviewhub)
	- [**Project Requirement**](#project-requirement)
	- [**UX**](#ux)
	- [**Project Overview**](#project-overview)
			- [Database](#database)
			- [Pages](#pages)
    - [**Testing**](#testing)
			- [Code inspection](#code-inspection)
			- [Navigational testing](#navigational-testing)
            - [Database updates](#database-updates)
			- [General Testing](#general-testing)
     - [**Deployment**](#deployment)
     - [**Credits**](#credits)
<hr />

## **Movie Review Hub**

Welcome to my Data Centric Development Milestone project as part of my [Code Institute (CI)](https://courses.codeinstitute.net/) Full Stack Web Development course.<br>
Final deployed site is here: https://movie-review-hub.herokuapp.com/
<hr />

## **Project Requirements**

- **Main Technologies**
  - HTML, CSS, JavaScript, Python+Flask, MongoDB.
  - Additional libraries and external APIs. 

- **Mandatory Requirements**
  - Data handling: Build a MongoDB-backed Flask project for a web application that allows users to store and manipulate data records about a particular domain. If you are considering using a different database, please discuss that with your mentor first and inform Student Care.
  - Database structure: Put some effort into designing a database structure well-suited for your domain. Make sure to put some thought into the nesting relationships between records of different entities.
  - User functionality: Create functionality for users to create, locate, display, edit and delete records (CRUD functionality).
  - Use of technologies: Use HTML and custom CSS for the website's front-end.
  - Structure: Incorporate a main navigation menu and structured layout (you might want to use Materialize or Bootstrap to accomplish this).
  - Documentation: Write a README.md file for your project that explains what the project does and the value that it provides to its users.
  - Version control: Use Git & GitHub for version control.
  - Attribution: Maintain clear separation between code written by you and code from external sources (e.g. libraries or tutorials). Attribute any code from external sources to its source via comments above the code and (for larger dependencies) in the README.
  - Deployment: Deploy the final version of your code to a hosting platform such as Heroku.
  - Make sure to not include any passwords or secret keys in the project repository. a username field to the recipe creation form, without a password (for this project only, this is not expected to be secure)

- **Important Notes**
  - No authentication is expected for this project. The focus is on the data, rather than any business logic.

- **CREATE YOUR OWN PROJECT**
  - If you choose to create your project outside the brief, the scope should be similar to that of the example brief above.

<hr />

## **UX**

*After a busy day I usually watch any sport going and the news. Failing that I scan for a Movie but end up flicking through the channels and invariably don't manage to find an appropriate movie to watch.*
*When I am scanning movies I generally read overviews of movie I recognise or if a favourite actor/actoress is in the cast. Today we face an ubandance of various media types which creates a movie selection minefield (Movies channels / Netflix / Amazon / catchup etc..) *
*With this in mind I decided to build a Movie Review Hub so you could go to ONE site and get the reviews from the people not just the critics and the ability to search for all movies a person acted in.*

## **Project overview**

*The Movie Review Hub is ALL about movies on or have been screened.*
*The landing page will display list of movies that have reviews sorted in the most recent reviews. Anyone can read reviews or search for movies/people without needing to logon. If you want to write a review you would register, select a movie and write a review. A use will only be able to edit or delete their own reviews. The logon and registration process is basic with no authentification (as per project requirement) but gives the abilty to restrict users from editing and deleting other reviews.*

### Database

- There are 5 collections, Users / Movies / Reviews / Categories & Ratings.
- I decided to split Movies and Reviews to create a parent/children relationship which could also have been achieved by having a sub array of reviews within movies but not as manageable.

### Pages

- There are 9 pages to the project.

  - **Navigation**
    - The same Navbar and feel is used for all the pages
    - Browse the home page and select a movie to review
    - Search for movies and select to see reviews
    - Register/Login to add/edit/delete reviews
    - Every page uses the base.html extended capaabilty that has the 8 - 4 grid design. The 8, is the injection from all other html pages and the 4 is the 'Hall of fame' that will the image with the most reviews and a users leader bord for most reviews made. The image will also change when a user selects a movie to review / add / edit or delete to give them a beeter UI/UX experience.
    - The add, edit and cancel screens have a cancel button incase the user changes their mind.
 
  - **Landing page (home.html)**
    - The user is presented with a listing of all movies that have reviews with the most recent being on the top. 
    - The green badge on each movie represent the review count and increases or decreases depending if a review is added or deleted.
  
  - **Reviews page (reviews.html)**
    - A list of ALL reviews for the selected movie.
    - Each review will have the username date/time and review score with an accordian to dislay the review idf selected to save real estate on the screen and provide a better UX.
    - A user will need to login to add, edit or delete their own reviews. 

  - **Add page (addreview.html)**
    - The username and movie title will be prepopulated and read only fields.
    - The Genre and rating selection boxes are mongoDB collections.
    - The Add review will add the review to the reviews collections and display the reviews screen.
    - When the user navigates to the home page the movie they reviewed will be the FIRST in the listing and badge count will be incremented.

  - **Edit page (editreview.html)**
    - This presents the user with the ability of changing their review or rating.

  - **Delete page (deletereview.html)**
    - The user can only delete their own review and will be presented a confirm / cancel modal **still to be built**.

  - **Delete Confirm page (deletconfirm.html)**
    - Confirm or cancel the delete functionality.
  
  - **Search page (search.html)**
    - The user can search for a title or part of a tile / person that does a API get to TMDB (The Movie Data Base - open) and present the user with a listing. If they select a movie that has is has reviews in the mongoDB collection then they will be presented the reviews page otherwise they will be display the addreview screen to entice the user to write a review.
  
  - **Login page (login.html)**
    - Displays the login screen for a username and password that has appropriate flash messages.

  - **Register page (register.html)**
    - Displays a basic register page username,password and confirm password that has appropriate flash messages but the password is just a visible string in the users collection and merely used to control the ability for users to add, edit or delete reviews.


<hr />

## **Testing**

### Code inspection 

  - [W3C Markup Validation Service](https://validator.w3.org/)
    Due to using Flask I needed to run the app and then view the page source to cut and paste the code into the validator to check. 
    - Output : Document checking completed. No errors or warnings to show.

  - [JSHint](https://jshint.com/) 
    - Output :

    There are 5 functions in main.js.
    Function with the largest signature take 1 arguments, while the median is 1.
    Largest function has 26 statements in it, while the median is 4.
    The most complex function has a cyclomatic complexity value of 7 while the median is 1.
    26 warnings.

#### Navigational Testing

<table>
    <tr>
        <th>Action</th>
        <th>Status</th>
    </tr>
    <tr>
        <td>Clicking on Movie Review Hub title takes user to homepage</td>
        <td>Successful</td>
    </tr>
    <tr>
        <td>Clicking on Home tab takes user to homepage</td>
        <td>Successful</td>
    </tr>
    <tr>
        <td>Clicking on Search takes user to search form</td>
        <td>Successful</td>
    </tr>
    <tr>
        <td>Click on Access provides the Login and Register dropdown to relevant pages.</td>
        <td>Successful</td>
    </tr>
    <tr>
        <td>On home page clicking on any movie will take you to the reviews page.</td>
        <td>Successful</td>
    </tr>
    <tr>
        <td>On reviews page clicking on 'add' will take you to add review page with 2 buttons.</td>
        <td>Successful</td>
    </tr>
    <tr>
        <td>On reviews page there will be a edit and delete button for all reviews made by the user and NOT for any other user.</td>
        <td>Successful</td>
    </tr>
    <tr>
        <td>The delete button will take you to a delete confirmation screen.</td>
        <td>Successful</td>
    </tr>
</table>

#### Database updates

<table>
    <tr>
        <th>Collections</th>
        <th>Movie</th>
        <th>Reviews</th>
        <th>Users</th>
        <th>Categories</th>
        <th>Ratings</th>
    </tr>
    <tr>
        <td>Initial DB data</td>
        <td> - </td>
        <td> - </td>
        <td> - </td>
        <td>Selection List</td>
        <td>Selection List</td>
    </tr>
    <tr>
        <td>Register</td>
        <td> - </td>
        <td> - </td>
        <td>Insert</td>
        <td> - </td>
        <td> - </td>
    </tr>
    <tr>
        <td>Add review</td>
        <td>Insert reviews_count set to 1</td>
        <td>Insert</td>
        <td>Update review_made incremented</td>
        <td> - </td>
        <td> - </td>
    </tr>
    <tr>
        <td>Add 2nd review</td>
        <td>Update reviews_count incremented</td>
        <td>Insert</td>
        <td>Update review_made incremented</td>
        <td> - </td>
        <td> - </td>
    </tr>
    <tr>
        <td>Delete review</td>
        <td>Update reviews_count decreased</td>
        <td>Delete</td>
        <td>Update review_made decreased</td>
        <td> - </td>
        <td> - </td>
    </tr>
    <tr>
        <td>Delete 2nd review</td>
        <td>Delete</td>
        <td>Delete</td>
        <td>Update review_made decreased</td>
        <td> - </td>
        <td> - </td>
    </tr>
</table>


#### General Testing

While developing I used DEBUG=TRUE to help iron out all the routing and undefined issues.
Print and console.log were extensively used to ensure the correct data was being passed.
The developer tool was used to test various media sizes so the elements gave a good UX.  
Tested with different input data and selections to ensure the appropriate FLASH messages were displayed.

[**To top**](#Table-of-Contents)


<hr />

## **Deployment**

In your Heroku account, create a new app.
GitHub has been used throughout this project to maintain version control as feature are added. After adding a new feature, the code is pushed to GitHub.
The site has been deployed using Heroku. The process for deploying to Heroku is as follows:

  - created [requirements.txt](https://github.com/Hurter3/MovieReviewHub/requirements.txt) that **Heroku** knows which packages are required for the application to run and install them.
  - created [Procfile](https://github.com/Hurter3/MovieReviewHub/master/Procfile) that **Heroku**  knows what kind of application is this.

  - **Settings**
    - Added **Config Vars**
      - IP `0.0.0.0`
      - PORT `5000`
      - MONGO_URI
      - SECRET_KEY
      - APIKEY

    - **Deploy**

Ensure in your app you have in your app files in GitHub a Procfile with the following: 'web: python app.py', and you project requirements in a requirements.txt file.
In Heroku, in your app and under the 'deploy' tab, choose the GitHub deployment method. In the app connected to GitHub section find and select the app you wish to deploy.
Choose either automatic or manual deploys.

Install requirements with $ pip3 install -r requirements.txt
Run the app with $ python3 app.py
          
[**To top**](#Table-of-Contents)

<hr />

## **Future Enhancments**

ERROR handling and introduce TV programs.

<hr />


[**To top**](#Table-of-Contents)

## **Credits**

The code instute tutors must be mentioned for their valuable recomendations and patience.<br>
Appreciation must also be said to The Movie DataBase (TMDB) for their open API data which was used for this project.
I used www.w3schools.com and www.stackoverflow in conjuction with the Task manager mini project for the accordian effect.

<hr />


[**To top**](#Table-of-Contents)