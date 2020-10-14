import os, json, requests

def book_get(db, isbn):
    row = db.execute("SELECT isbn, title, author, year FROM books WHERE isbn = '%s'" % isbn)
    bookInfo = row.fetchall()

    """ GOODREADS reviews """

    # Read API key from env variable
    key = os.getenv("GOODREADS_KEY")
    
    # Query the api with key and ISBN as parameters
    query = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": key, "isbns": isbn})

    # Convert the response to JSON
    response = query.json()['books'][0]

    # Append it as the second element on the list. [1]
    bookInfo.append(response)

    """ Users reviews """

    # Fetch book reviews
    # Date formatting (https://www.postgresql.org/docs/9.1/functions-formatting.html)
    results = db.execute("SELECT username, comment, rating, \
                        to_char(time, 'DD Mon YY - HH24:MI:SS') as time \
                        FROM users \
                        INNER JOIN reviews \
                        ON users.id = reviews.user_id \
                        WHERE isbn = '%s' \
                        ORDER BY time" % isbn)

    reviews = results.fetchall()

    return bookInfo, reviews