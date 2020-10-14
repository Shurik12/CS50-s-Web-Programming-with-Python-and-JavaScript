from flask import Blueprint, session, render_template, request, redirect, flash
import os, json, requests

def book_post(db, isbn, session):
	# Save current user info
    currentUser = session["user_id"]
    
    # Fetch form data
    rating = request.form.get("rating")
    comment = request.form.get("comment")

    # Check for user submission (ONLY 1 review/user allowed per book)
    row = db.execute("SELECT * FROM reviews WHERE user_id = '%s' AND isbn = '%s' " % (currentUser, isbn))

    # A review already exists
    if row.rowcount == 1:
        
        flash('You already submitted a review for this book', 'warning')
        return redirect("/book/" + isbn)

    # Convert to save into DB
    rating = int(rating)

    db.execute("INSERT INTO reviews (user_id, isbn, comment, rating)\
    			VALUES (%d, '%s', '%s', %d)" % (currentUser, isbn, comment, rating)
    			)

    # Commit transactions to DB and close the connection
    db.commit()
