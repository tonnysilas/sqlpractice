from enum import unique
from flask import Flask
import os
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from flask import request
app = Flask(__name__)

project_dir = os.path.dirname(os.path.abspath(__file__)) #finding the current app path. (Location of this file)

database_file = "sqlite:///{}".format(os.path.join(project_dir, "formdatabase.db")) # creating a database file (formdatabase.db) in the above found path.

app.config["SQLALCHEMY_DATABASE_URI"] = database_file # connecting the database file (formdatabase.db) to the sqlalchemy dependency.

db = SQLAlchemy(app) # connecting this app.py file to the sqlalchemy

@app.before_first_request
def create_table():
     db.create_all()

class Book(db.Model): #creating a model for the cell called title in the form
    title = db.Column(db.String(80), unique = True, nullable = False, primary_key = True) #this means that the cell will only accept 80 string characters at max without repeating any. It can not be empty and is a mandatory field

    def __repr__(self):
        return "<Title: {}>".format(self.title)

@app.route('/', methods=["GET", "POST"])
def home():
     # validating the content of the form. This condition shall be false if the request.form list is empty
    if request.form:
        title_from_form = request.form.get('title') # assigns the content of the title field to the variable
        book = Book(title=title_from_form) # instance of the Book class. assigned to the 'book' variable
        db.session.add(book) # adds the data to the session
        db.session.commit() # this commits the data to the database
    books = Book.query.all() # this retrieves all the contents of the book table.
    return render_template('form.html', iwe = books) # rendering the html page alongside the queried books to the browser.

    if __name__=="__main__":
        app.run(debug=True)
