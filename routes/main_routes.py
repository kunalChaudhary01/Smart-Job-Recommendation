from flask import Blueprint, render_template, session, redirect

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def landing():
    """Public landing page; redirects authenticated users to dashboard."""
    if "user_id" in session:
        return redirect("/dashboard")
    return render_template("landing.html")
