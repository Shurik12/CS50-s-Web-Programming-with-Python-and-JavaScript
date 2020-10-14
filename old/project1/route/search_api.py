from flask import Blueprint, session, render_template, request, redirect, flash, jsonify
from route.db import db
from route.book_post import book_post
from route.book_get import book_get
from route.login_required import login_required

my_api = Blueprint('my_api', __name__)

@my_api.route("/api/<isbn>", methods=['GET'])
@login_required
def api_call(isbn):

    # COUNT returns rowcount
    # SUM returns sum selected cells' values
    # INNER JOIN associates books with reviews tables

    row = db.execute("SELECT title, author, year, reviews.isbn, \
                    COUNT(reviews.id) as review_count, \
                    AVG(reviews.rating) as average_score \
                    FROM books \
                    INNER JOIN reviews \
                    ON books.isbn = reviews.isbn \
                    WHERE reviews.isbn = '%s'\
                    GROUP BY title, author, year, reviews.isbn" % isbn)

    # Error checking
    if row.rowcount != 1:
        return jsonify({"Error": "Invalid book ISBN"}), 422

    # Fetch result from RowProxy    
    tmp = row.fetchone()

    # Convert to dict
    result = dict(tmp.items())

    # Round Avg Score to 2 decimal. This returns a string which does not meet the requirement.
    # https://floating-point-gui.de/languages/python/
    result['average_score'] = float('%.2f'%(result['average_score']))

    return jsonify(result)