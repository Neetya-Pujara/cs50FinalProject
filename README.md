# N-News
> News Portal
### *Video Demo* : [CS50 Final Project - N-News](https://youtu.be/SJx0xNWRpjw)
&nbsp;
## **Description** :

Fundamentally, my final project is a news portal in the form of a Flask application where users can browse news articles they are interested in. Users are not required to create an account to avail this facility. On top of that, they can like and comment on those articles to express their opinion.

News articles are published by journalists who are registered on our application. There is a robust process where we background-check the journalist before confirming their registration so that our users get reliable information. Additionally, the news articles submitted by registered journalists are scrutinized against our portal's ethics and guidelines before they get published.

Let's move on to the file structure, what they contain and their functionality.

### ***flask_session***

Considering the functionality of sessions, I used it for registered journalists to stay logged in the portal. To use session, I had to import ```Session``` from the ```flask_session``` library, in the file *app.py*. The directory of **```flask session```** stores the unique session of each user (Every user is logged in with a different session).

### ***neetya_news.db***

The SQL database where the application **stores all the data** about the users, articles and other factors, is called **neetya_news.db**. It is comprised of three tables, namely 'users', 'comments' and 'own_news'.

'Users' consists of vital information about the registered journalists, such as their username, hashed password, unique id, request or if their profile is approved by the admin, and lastly the education field they filled out in the registration form.

As for 'own_news', it contains the news article, unique article id, user_id, request or if the article is approved by the admin, name of the journalist who wrote the article, title, number of views, likes, and lastly, time the article was published.

The column 'request' is especially important because it is used to identify which profiles or articles are approved or published.

In the 'comments' table, there is the news_id column or the id of the news article, unique id for comment itself, comment, and the adjective or name of the person posting the comment.

Using ```db.execute```, the application can execute SQL commands through app.py to automate the manual process.

### ***static***

The static directory of the Flask application structure is empty. This is because I have reused Bootstrap code for all of my styles and designing of the application, and I haven't used any images for my news portal.

## **Templates**

The ```templates``` directory contains all my HTML files that form all the pages of my application.

### ***layout.html***

This file is pretty self-explanatory. It **defines the layout** of all the other templates. As you can see, I've used Jinja syntax to connect the structure of all the other templates with this file. This file also contains the requirements to use Bootstrap code, along with the 'navbar'. I've used Jinja conditionals to make sure users have access to the right pages. For example, a user that is not a registered journalist shouldn't have access to the 'Add News' page. At the end of the file comes the 'main block' which is extended in the other templates according to the functionality of each page.

### ***news.html***

This file forms the most fundamental page of my application. It **displays all the news articles** whose request columns are 'Approved' or in simple words, approved by the admin to be published on the news portal, and the page is accessible to both, users and registered journalists. I also implemented a search bar to fasten the process of finding a particular news article. news.html, like every other template, is an extension of layout.html. As you can see, first, a ```<div>``` tag is used for the search bar. The code gets a little complicated after that becuase the HTML file is reused for multiple routes.

For instance, if the news.html template is rendered by the "/" route, it will skip the code indented after ```{% if not rows %}``` because the route "/" has sent information about data called 'rows'. However, if the template is rendered by the "/search" route, it will follow that code because it, at that moment, doesn't have any info about data called 'rows'. I used this strategy to reuse this template while ensuring I don't mix up the purposes of different routes rendering the same template.

In simple words, I specified conditionals in Jinja syntax to achieve the purpose of the accurate route rendering the template.

As for presenting news articles, I used Bootstrap for organization and design, and Jinja ```for``` loops to iterate through the articles stored in the SQL database. A decent table divides the information about each article into the title, name of journalist, a read button to view the article, and finally, the number of views. Moreover, I went further to make two catergories of news articles namely 'Popular News' and 'Latest News' so that users can make a more decisive choice. Under the category of 'Popular News', come the 5 most viewed articles, and under 'Latest News' come other articles ordered by the date they were posted on.

At the end of the page is a footer stating that 'If you are a journalist you can apply to create an account' .

### ***read_news.html***

The routes '/like', '/read_news', and '/comment' in app.py can render the template of read_news.html. This HTML file mainly **exhibits the corresponding news article**. However, when rendered by the like and comment routes, it is re-rendered after updating **like** and **comment** info on the SQL database.

If you go through app.py, you would notice some repition of code in '/comment', '/like', and '/read_news'. This is because I thought it was a more simplistic approach to create new routes namely like and comment instead of reusing the read_news route.

To ensure that if the article is not published, the admin is not able to comment or like on it when approving or denying the article, I specified a Jinja conditional stating that if the article is not published yet, it should not show the option to comment or like even for the admin. (Admin meaning the controller of the portal)

Otherwise, when the article is approved by the admin or published, I have provided the ability for users to comment on news articles or like them. However, to monitor that inappropriate comments are not being posted on our portal, the admin has the power to delete comments.

### ***apology.html***

This HTML file is used to represent a specific **error**. I reused this file in every possible scenario of an error, however, passed in a different message to ensure the user understands what went wrong, and how they can re-attempt their action.

### ***register.html***

```register.html``` is a template essesntially demonstrating a **registration form** prompting for the full name of the journalist, education, and password for their account.

To prevent future misunderstandings, I have included a terms and conditions required checkbox in order to get confirmation from the user that they will accept the admin's final decision. For instance, if their article isn't approved by the admin, the user has to respect their decision.

When they click on the button 'Validate Profile', their profile is submitted to the admin and thus, appears on the admin's 'Profile Submission' page that we will be discussing about later. When the admin approves their profile, they will be able to log into the news portal as a registered journalist. This process is automated through the '/approval' route which makes the required changes in *```neetya_news.db```*. Until the admin approves the profile, it is said to be 'On Hold' in the database.

### ***login.html***

login.html, as its name indicates, is a HTML file for presenting a login form through which a registered journalist can log in the portal. The form asks for the journalist's full name and password they entered in their registration form. The data is 'POST'ed to the route '/login' where the journalist is provided their 'session'.

### ***add_news.html***

This 'Add News' page is only accessible to registered journalists. To safeguard this restriction, I used **```@login_required```** to ensure no one can possibly fiddle with the portal's accessibility. This template's purpose is to allow the journalist to submit their written article to the admin. The admin reviews the article in a consistent and unbiased manner in line with the defined guidelines of the portal.

The HTML file displays a form asking for the news article's title, and then a text box is provided to write the article itself. As soon as the article is approved by the admin, it is available for users to read, comment and like. The request column, thus, is updated to 'Approved' from 'On Hold'.

### ***index.html***
```index.html``` is like the homepage of a registered journalist. In a table established using Boootstrap's code, it exhibits the journalist's news articles that are 'On Hold' and the ones which are 'Approved'. This helps the journalist organize its status. To be precise, the table's data includes the title of the news article, the jorunalist's name, and if the article is 'Approved' or 'On Hold'.

### ***list_news.html*** & ***profile.html***
These pages are only accessbile to the admin. They obtain the admin with the power to delete articles and remove profiles. For example, as time passes, the admin may want to remove obsolete news articles.

### ***owner.html*** & ***owner2.html***
Just like the previous pages were expounded to be only accessible to the admin, the same goes for ```owner.html``` and ```owner2.html``` that are named as 'Profile Submissions' and 'Article Submissions', respectively, on the portal. These pages, again, in tables display data about profiles and articles 'On Hold'. In other words, when users register for a journalist account or a registered journalist submits their news article, their or their articles' information is displayed on the admin's screen as 'On Hold' so that the admin can approve or deny their articles or profiles as per the portal's guidelines. I automated this process by programming the application to execute SQL commands that update the request column from 'On Hold' to 'Approved'. However, if the admin denied the profile or article, I send the data to routes called '/delete_news' or '/delete_profile' which execute required SQL commands.

## **```app.py```**

app.py, like in every other Flask application, contains the Python code for my application. It can also be described as the file comprised of routes that anchor the user through the website, or as the main control center.

The first few lines of the file are dedicated to import particular functions from their libraries, that are going to be used in the code further. Then, I make this entire directory into the programming of a Flask application using the ```Flask()``` function.

After this, begin the routes. They render specific templates according to their functionality and provide them with the required information to display and use. However, this is only when the method 'GET' is used. When the method 'POST' is used, mostly the application executes SQL commands to make required changes in the database as per the data it recieves from the user's inputs.

The names of all the routes are :-

All Users : */like, /comment, /read_news, /search, ***/****

Registered Journalist Options : */login, /register, /add_news, /logout, /approval, /home*

Admin ONLY : */delete_news, /delete_profile, /list_news, /delete_comment, /profiles, /profile2, /home1*

### ***helpers.py***

I created this Python file to help me organize and store all the functions I'll need to code myself, that will be useful for my application. The functions I coded in this file are **```apology()```** & **```@login_required```** using the libraries of ```flask``` and ```functools```.

##### 1. **@login_required**
##### 2. **apology()**

&nbsp;

### ***requirements.txt***

Since I didn't use that many libraries and functions, and didn't as such need to organize them in a file, I left the requirements.txt file empty.
