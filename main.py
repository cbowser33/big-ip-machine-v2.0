import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from models.user import db
from routes.user import user_bp
from routes.auth import auth_bp
from routes.content import content_bp
from routes.tokenization import tokenization_bp
from routes.tokenization_v11 import tokenization_v11_bp
from routes.registration import registration_bp
from routes.upload_success import upload_success_bp
from routes.email_notifications import email_notifications_bp
from routes.analysis import analysis_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'big-ip-machine-v2.0-secret-key-2024'

# Configure for large file uploads (50GB+ for full-length movies)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024 * 1024  # 50GB max file size
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # Disable caching for large files

# Enable CORS for all routes
CORS(app, origins="*")

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(auth_bp, url_prefix='/api')
app.register_blueprint(content_bp, url_prefix='/api/content')
app.register_blueprint(tokenization_bp, url_prefix='/api/tokenization')
app.register_blueprint(tokenization_v11_bp, url_prefix='/api/v1.1/tokenization')
app.register_blueprint(registration_bp, url_prefix='/api/registration')
app.register_blueprint(upload_success_bp, url_prefix='/api/upload')
app.register_blueprint(email_notifications_bp, url_prefix='/api/email')
app.register_blueprint(analysis_bp, url_prefix='/api/analysis')

# uncomment if you need to use database
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
with app.app_context():
    db.create_all()

@app.route('/')
def login_page():
    """Default landing page - Login"""
    static_folder_path = app.static_folder
    if static_folder_path is None:
        return "Static folder not configured", 404
    
    login_path = os.path.join(static_folder_path, 'login.html')
    if os.path.exists(login_path):
        return send_from_directory(static_folder_path, 'login.html')
    else:
        return "login.html not found", 404

@app.route('/dashboard')
def dashboard():
    """Main dashboard - accessible after login"""
    static_folder_path = app.static_folder
    if static_folder_path is None:
        return "Static folder not configured", 404
    
    index_path = os.path.join(static_folder_path, 'index.html')
    if os.path.exists(index_path):
        return send_from_directory(static_folder_path, 'index.html')
    else:
        return "index.html not found", 404

@app.route('/<path:path>')
def serve_static(path):
    """Serve static files"""
    static_folder_path = app.static_folder
    if static_folder_path is None:
        return "Static folder not configured", 404

    if os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        return "File not found", 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
