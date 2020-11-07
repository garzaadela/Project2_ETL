import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from config import postrespw
from flask import Flask, jsonify

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
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/names<br/>"
        f"/api/v1.0/passengers"
    )


@app.route("/api/v1.0/names")
def names():
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


if __name__ == '__main__':
    app.run(debug=True)
