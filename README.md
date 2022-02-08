REQUIREMENTS:

Note: I was unable to connect my backend to the database because of the following Flask error: ImportError: No module named flask_sqlalchemy. I am getting this error even after dowanloading flask, SQLAlchemy, sqlalchemy, and flask_sqlalchemy.
That being said, I still coded all the things needed to connect the back end so please look through my code and mark accordingly.

1. I took the structure of creating folders and files inspiration from my friend Chris Benard.
2. Templates folder contains all the html webpages that I needed to create.
    a. Inside the templates folder, there is a file called 'template.html' which contains the main template I created that all my html pages refer to.
3. Static folder contains pictures and css file
4. .pylintrc folder was created to make python ignore an error I was receiving with db.session
5. application.py is the main file that connects to the backend, create website routes, and integrated the api as well as book.cvs file
6. create.py file create the tables on the database 
7. import2.py file has a function that imports the book.csv content to the database
8. models.py creates all the different table models



