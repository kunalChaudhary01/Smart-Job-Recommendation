from functools import wraps
from flask import session, redirect, flash


def login_required(f):
    """Decorator to require login for protected routes."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function
