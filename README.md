# Code Institute


# **Table of Contents**

- [**Table of Contents**](#table-of-contents)
	- [**Movie Review Hub**](#moviereviewhub)
	- [**Project Requirement**](#project-requirement)
	- [**UX**](#ux)
	- [**Project Overview**](#project-overview)
			- [Database](#database)
			- [Pages](#pages)

<hr />

## **Movie Review Hub**

Welcome to my Data Centric Development Milestone project as part of my [Code Institute (CI)](https://courses.codeinstitute.net/) Full Stack Web Development course.

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

- There are 5 collections, Users / Movies / Reviews / Genre & Ratings.
- I decided to split Movies and Reviews to create a parent/children relationship which could also have been achieved by having a sub array of reviews within movies but not as manageable.

### Pages

- There are 7 pages to the project.

- **All page**
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
  
  - **Search page (search.html)**
   - The user can search for a title or part of a tile / person that does a API get to TMDB (The Movie Data Base - open) and present the user with a listing. If they select a movie that has is has reviews in the mongoDB collection then they will be presented the reviews page otherwise they will be display the addreview screen to entice the user to write a review.
  
  - **Login page (login.html)**
   - Displays the login screen for a username and password that has appropriate flash messages.

   - **Register page (register.html)**
   - Displays a basic register page username,password and confirm password that has appropriate flash messages but the password is just a visible string in the users collection and merely used to control the ability for users to add, edit or delete reviews.




