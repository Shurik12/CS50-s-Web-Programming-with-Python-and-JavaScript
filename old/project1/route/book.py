from flask import Blueprint, session, render_template, request, redirect, flash 
from route.db import db
from route.book_post import book_post
from route.book_get import book_get
from route.login_required import login_required

book_api = Blueprint('book_api', __name__)

@book_api.route("/book/<isbn>", methods=['GET','POST'])
@login_required
def book(isbn):
    """ Save user review and load same page with reviews updated."""

    if request.method == "POST":
        book_post(db, isbn, session)

        flash('Review submitted!', 'info')
        return redirect("/book/" + isbn)
    
    # Take the book ISBN and redirect to his page (GET)
    else:
        bookInfo, reviews = book_get(db, isbn)
        return render_template("book.html", bookInfo=bookInfo, reviews=reviews)