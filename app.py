import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from config import postrespw
from flask import Flask, jsonify, render_template
#################################################
# Database Setup
#################################################
rds_connection_string = (f"postgres:{postrespw}@localhost:5432/project2")
engine = create_engine(f'postgresql://{rds_connection_string}')
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# Save reference to the table
Nyt_data = Base.classes.nyt_data
Books_data = Base.classes.books_data
Ratings_data = Base.classes.ratings_data
All_books = Base.classes.all_books
#################################################
# Flask Setup
#################################################
app = Flask(__name__)
#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return render_template("index.html")
# (
#         f"Available Routes:<br/>"
#         f"/api/v1.0/archvisdata<br/>"
#         f"/api/v1.0/scattervisdata<br/>"
#         f"/api/v1.0/adelavisdata<br/>"
#         f"/api/v1.0/table<br/>"
#         f"/api/v1.0/adelavisscatterdata<br/>"
#         f"/api/v1.0/scatter<br/>"
#         f"/api/v1.0/wordcloudvisdata"
#     )
@app.route("/api/v1.0/archvisdata")
def arch():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    """Return a list of all passenger names"""
    # Query all passengers
    results = session.query(All_books.author, All_books.publisher).all()
    session.close()
    # Convert list of tuples into normal list
    authors_publishers = []
    for author, publisher in results:
        ap_dict = {}
        ap_dict["author"] = author
        ap_dict["publisher"] = publisher
        authors_publishers.append(ap_dict)
    return jsonify(authors_publishers)
@app.route("/api/v1.0/wordcloudvisdata")
def wordcloud():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    """Return a list of all passenger names"""
    # Query all passengers
    results = session.query(Nyt_data.description).all()
    session.close()
    # Convert list of tuples into normal list
    descriptions = list(np.ravel(results))
    return jsonify(descriptions)

@app.route("/api/v1.0/adelavisdata")
def dropdown():
    # Create our session 
    session = Session(engine)
    """Return a list of all passenger names"""
    # Query all 
    results = session.query(All_books.title, All_books.description, All_books.author, All_books.publisher).all()
    session.close()
    # Convert list of tuples into normal list
    title_data = []
    for title, descriptions, author, publisher in results:
        table_dict = {}
        table_dict["title"] = title
        table_dict["descriptions"] = descriptions
        table_dict["author"] = author
        table_dict["publisher"] = publisher
        title_data.append(table_dict)
    return jsonify(title_data)

# @app.route("/api/v1.0/table")
# def tabledata():
#     return render_template("index.html")

@app.route("/api/v1.0/adelavisscatterdata")
def scatterdata():
   
    # Create our session  
    session = Session(engine)
    """Return a list of all passenger names"""
    # Query all 
    results = session.query(All_books.weeks_on_list, All_books.title, All_books.whole_rating).all()
    session.close()
    # Convert list of tuples into normal list
    scatter_data = []
    for weeks_on_list, title, whole_rating in results:
        scatter_dict = {}
        scatter_dict["weeks_on_list"] = weeks_on_list
        scatter_dict["title"] = title
        scatter_dict["whole_rating"] = whole_rating
        scatter_data.append(scatter_dict)
    return jsonify(scatter_data)

# @app.route("/api/v1.0/scatter")
# def scatter():
#     """List all available api routes."""
#     return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)



