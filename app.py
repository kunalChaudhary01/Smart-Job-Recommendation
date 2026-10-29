from flask import Flask, render_template
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv
import os

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config["UPLOAD_FOLDER"] = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads")
    app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024
    app.secret_key = os.getenv("SECRET_KEY", "dev-secret-key")
    
    csrf = CSRFProtect(app)
    
    from routes.auth_routes import auth_bp
    from routes.resume_routes import resume_bp
    from routes.recommendation_routes import recommendation_bp
    from routes.history_routes import history_bp
    from routes.admin_routes import admin_bp
    from routes.main_routes import main_bp
    from routes.dashboard_routes import dashboard_bp
    from routes.profile_routes import profile_bp
    from routes.saved_jobs_routes import saved_jobs_bp
    from routes.job_routes import job_bp
    from routes.application_routes import application_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(resume_bp)
    app.register_blueprint(recommendation_bp)
    app.register_blueprint(history_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(saved_jobs_bp)
    app.register_blueprint(job_bp)
    app.register_blueprint(application_bp)
    
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    
    # Exempt multipart upload from CSRF (file uploads)
    csrf.exempt(resume_bp)
    csrf.exempt(admin_bp)
    
    @app.errorhandler(404)
    def not_found(e):
        return render_template("404.html"), 404
    
    @app.errorhandler(500)
    def server_error(e):
        return render_template("500.html"), 500
    
    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
