from flask import Blueprint, session, render_template, request 
from route.db import db
from route.login_required import login_required

search_api = Blueprint('search_api', __name__)

@search_api.route("/search", methods=["GET"])
@login_required
def search():
    """ Get books results """

    # Check book id was provided
    book = request.args.get("book")

    if not book: return render_template("error.html", message="you must provide a book.")

    # Take input and add a wildcard
    query = "%" + book + "%"

    # Capitalize all words of input for search
    # https://docs.python.org/3.7/library/stdtypes.html?highlight=title#str.title
    #query = query.title()
    
    rows = db.execute(" SELECT isbn, title, author, year \
                        FROM books \
                        WHERE isbn LIKE '%s' OR title LIKE '%s' OR author LIKE '%s' \
                        LIMIT 15" % (query, query, query))    
    # Books not founded
    if rows.rowcount == 0: return render_template("error.html", message="we can't find books with that description.")
    
    # Fetch all the results
    books = rows.fetchall()

    return render_template("results.html", books=books)