from functools import wraps
from django.shortcuts import render

def login_required(function):
    @wraps(function)
    def decorated_function(*args, **kwargs):
        if not args[0].user.is_authenticated:
            return render(args[0], "auctions/login.html" , 
                {"message": "To use this method you must be logged in."})
        return function(*args, **kwargs)
    return decorated_function