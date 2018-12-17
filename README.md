# Verkefni 3 - SC-T-308-PRLA

## Folf App - FOLFWEB

A web based app to keep track of frisbee golf. It requires the user to sign in and then the user can keep track of games played, get information about local courses and log scores for each game played.

---

## Frameworks

The application uses these frameworks:

- Python Flask
- Google Firebase(BaaS)

---

## Download the App

**Clone Git Repository:**

```Bash
git clone git@github.com:peturo14/verkefni3.git
```

---

## Dependencies

**Python 3.X**

```Bash
python3 --version
> Python 3.6.7
```

**Flask:**

```Bash
pip3 install flask
```

**Pyrebase:**

```Bash
pip3 install pyrebase
```

**Flask-WTF:**

```Bash
pip3 install flask-wtf
```

**Green Unicorn:** _Required for deployment on Heroku_

```Bash
pip3 install gunicorn
```

---

## Run the application

There is a version we were able to deploy on Heroku:

[Folf App - FOLFWEB](https://folfapp.herokuapp.com/)

To run the application locally on port 5000:

```Bash
python3 app.py
```

Or alternatively using Gunicorn on port 8000:

```Bash
gunicorn app:app
```

Once the server is running and listening on its respective port you can open a web browser and enter the shorthand URL:

[localhost:5000](http://localhost:5000/) and [localhost:8000](http://localhost:8000/)

You are then greeted by the landing page of the application.

---

## Use the application

The application allows users to log plays and track games played on different courses. To utilize the application features the user must register and then sign in using e-mail.

### /Home

This is for all intense and purposes the first page. Here the application greets the user with the full name.

### /Courses

Here the user can select a courses to play and the starting point. Then the user is taken to the Play Sheet Form that accepts game data to be tracked. When the game is over the form can be posted and is written to the database.

### /Games

Here the user gets a rendered list of all games logged into the database.

### /Rules

Here the user get a rendered set of the rules. This part of the application is open for all user, not just the logged in members.

---

# Project Report

## Flask

Flask is a microframework for Python based on Werkzeug, Jinja 2 and good intentions. It's main appeal over other frameworks like Django is how very lightweight and higly modular it is. If the developer wants more freedom in putting together features for the application Flask is the way to go.

Flask-WTF is a third-party module for validating user input from HTML forms. It is designed to work well with Bootstrap 4 and is really convenient for rapid prototyping.

---

## Firebase(Backend as a service(BaaS))
Firebase is a mobile app development tool. It's an all inclusive service and helps teams get going quicker with rapid development.

What Firebase offers us is that we can use it in this project as an authentication service and NoSQL Document data store.

The Authentication service:

- User regiest with email and passord.
- User login.
- User password reset.
- LocalId for the session.

Database:

- Add game play data.
- Keep info about locations and courses.

---

## HTML JINJA 2

All the HTML is rendered with the Jinja 2 templateing engine. By using special syntax the template engine can render blocks of HTML based on conditional statements and use loops to render lists.

---

## Bootstrap and CSS

Because of how limited the time for the project was and how narrow the scope was, we chose to implement Bootstrap 4 for most of our styling needs. A few specialized CSS rules were added to a static CSS file but it uses mostly true and tried Bootstap classes.

We took great care of making the design responsive with the use of media queries. The application works equally well on a desktop computer and on mobile devices.

---

## Heroku Deployment

For heroku deployment we needed to keep our dependecies in a virtual enviroment.

Here are a few simple steps we followed to deploy on Heroku.

### Install the virtual enviroment

```Bash
python3 -m pip install --user virtualenv
```

### Create the virtual enviroment

```Bash
python3 -m virtualenv env
```

### Activate the virtual enviroment

```Bash
source env/bin/activate
```

### Install dependecies to the virtual enviroment

```Bash
pip3 install gunicorn flask pyrebase flask-wtf
```

### Create requirement text file with dependecies for heroku

```Bash
pip3 freeze > requirements.txt
```

### Install Heroku CLI on Linux

```Bash
sudo snap install --classic heroku

or

curl https://cli-assets.heroku.com/install-ubuntu.sh | sh
```

### Login to Heroku

```Bash
Heroku login
```

Go to www.heroku.com and create app named folfapp.

### Link our git repository with heroku

```Bash
heroku git:remote -a folfapp
```

### Add the project to the git repository

```Bash
git add .
```

### Commit the changes

```Bash
git commit -m "make first release of the folfapp live"
```

### Push it to the heroku

```Bash
git push heroku master
```

Now the app is live at:
[https://folfapp.herokuapp.com/](https://folfapp.herokuapp.com/)

---

## Graphic design

All the static PNG files were generated using GIMP for Linux, it's the open source equivalent to PhotoShop from Adobe.

The design guidelines were _Retro_ and _Flat_. We went with that yellow'ish color out of convenience because the color is defined as 'warning' in Bootstrap and was really simple to implement.

We also use two different Google Fonts. One is a nice looking sans-serif for basic text and the other has that pixlated look to it and in our opinion really ties the design together.

---

## General thoughts about the project

When we started working on the project we soon realized that its scope was really narrow and we would have to keep our expectations in check. Both of us have worked on projects before where scope creep became an issue and we really didn't want that this time around.

One thing we were trying to get away with was not writing any JavaScript our selfs. There are a few features in Bootstrap that rely on JavaScript but that is all included out of the box. If the scope would have been wider it would've been tempting to try and implement more asynchronous functionallity. That would have been reflected in less calls to the back-end and made everthing just that much quicker and more responsive.

We were also unable to use outside API's. There is a small learning curve when it comes to dealing with other API's. The documentation isn't always well written and if is not a true hypermedia driven API there can be compatibilty issues as well. Given the narrow scope we did not atempt to implement any such services.
