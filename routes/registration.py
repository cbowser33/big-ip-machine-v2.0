"""
User Registration System for The Big IP Machine v1.3
Handles user sign-up with username, password, email validation and additional criteria
"""

from flask import Blueprint, request, jsonify, session
import re
import hashlib
import secrets
import sqlite3
import os
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

registration_bp = Blueprint('registration', __name__)

# Database setup
DATABASE_PATH = os.path.join(os.path.dirname(__file__), '..', 'database', 'users.db')

def init_user_database():
    """Initialize the user database with enhanced schema for v1.3"""
    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
    
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Enhanced user table for v1.3
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL,
            full_name TEXT,
            company_name TEXT,
            user_type TEXT DEFAULT 'creator',
            email_verified BOOLEAN DEFAULT FALSE,
            verification_token TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP,
            profile_complete BOOLEAN DEFAULT FALSE,
            email_notifications BOOLEAN DEFAULT TRUE,
            marketing_emails BOOLEAN DEFAULT FALSE,
            terms_accepted BOOLEAN DEFAULT FALSE,
            privacy_accepted BOOLEAN DEFAULT FALSE,
            account_status TEXT DEFAULT 'active'
        )
    ''')
    
    # Email verification tokens table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS email_verifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            token TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP NOT NULL,
            used BOOLEAN DEFAULT FALSE,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # User sessions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            session_token TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP NOT NULL,
            ip_address TEXT,
            user_agent TEXT,
            active BOOLEAN DEFAULT TRUE,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """Validate password strength"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    
    if not re.search(r'\d', password):
        return False, "Password must contain at least one number"
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Password must contain at least one special character"
    
    return True, "Password is valid"

def validate_username(username):
    """Validate username format"""
    if len(username) < 3:
        return False, "Username must be at least 3 characters long"
    
    if len(username) > 30:
        return False, "Username must be no more than 30 characters long"
    
    if not re.match(r'^[a-zA-Z0-9_-]+$', username):
        return False, "Username can only contain letters, numbers, underscores, and hyphens"
    
    return True, "Username is valid"

def hash_password(password):
    """Hash password with salt"""
    salt = secrets.token_hex(32)
    password_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000)
    return password_hash.hex(), salt

def verify_password(password, password_hash, salt):
    """Verify password against hash"""
    computed_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000)
    return computed_hash.hex() == password_hash

def generate_verification_token():
    """Generate secure verification token"""
    return secrets.token_urlsafe(32)

def send_verification_email(email, username, token):
    """Send email verification email"""
    try:
        # Email configuration (using environment variables for security)
        smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        smtp_port = int(os.getenv('SMTP_PORT', '587'))
        smtp_username = os.getenv('SMTP_USERNAME', 'noreply@bigip-machine.com')
        smtp_password = os.getenv('SMTP_PASSWORD', 'demo_password')
        
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = 'Welcome to The Big IP Machine - Verify Your Email'
        msg['From'] = f'The Big IP Machine <{smtp_username}>'
        msg['To'] = email
        
        # HTML email content
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: 'Inter', Arial, sans-serif; background: #f8f9fa; margin: 0; padding: 20px; }}
                .container {{ max-width: 600px; margin: 0 auto; background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }}
                .header {{ background: linear-gradient(135deg, #8b5cf6 0%, #c084fc 100%); padding: 40px 30px; text-align: center; }}
                .header h1 {{ color: white; margin: 0; font-size: 28px; font-weight: 700; }}
                .header p {{ color: rgba(255,255,255,0.9); margin: 10px 0 0 0; font-size: 16px; }}
                .content {{ padding: 40px 30px; }}
                .welcome {{ font-size: 20px; font-weight: 600; color: #1f2937; margin-bottom: 20px; }}
                .message {{ color: #4b5563; line-height: 1.6; margin-bottom: 30px; }}
                .verify-btn {{ display: inline-block; background: #8b5cf6; color: white; padding: 15px 30px; text-decoration: none; border-radius: 8px; font-weight: 600; font-size: 16px; }}
                .verify-btn:hover {{ background: #7c3aed; }}
                .footer {{ background: #f9fafb; padding: 30px; text-align: center; color: #6b7280; font-size: 14px; }}
                .features {{ background: #f8fafc; padding: 20px; border-radius: 8px; margin: 20px 0; }}
                .feature {{ display: flex; align-items: center; margin: 10px 0; }}
                .feature-icon {{ color: #8b5cf6; margin-right: 10px; font-size: 18px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🎉 Welcome to The Big IP Machine!</h1>
                    <p>Professional IP Tokenization Platform</p>
                </div>
                <div class="content">
                    <div class="welcome">Hello {username}!</div>
                    <div class="message">
                        Thank you for joining The Big IP Machine, the premier platform for fractional ownership of intellectual property on the blockchain.
                    </div>
                    <div class="message">
                        To complete your registration and start tokenizing your intellectual property, please verify your email address by clicking the button below:
                    </div>
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="http://localhost:5000/verify-email?token={token}" class="verify-btn">Verify Email Address</a>
                    </div>
                    <div class="features">
                        <div class="feature">
                            <span class="feature-icon">🚀</span>
                            <span>Upload and tokenize your IP with 94.4% smart detection accuracy</span>
                        </div>
                        <div class="feature">
                            <span class="feature-icon">💎</span>
                            <span>Create ERC-1155 tokens on Polygon blockchain</span>
                        </div>
                        <div class="feature">
                            <span class="feature-icon">📊</span>
                            <span>Track your IP portfolio with real-time analytics</span>
                        </div>
                        <div class="feature">
                            <span class="feature-icon">🏪</span>
                            <span>Access the IP marketplace for licensing opportunities</span>
                        </div>
                    </div>
                    <div class="message">
                        If you didn't create an account with us, please ignore this email.
                    </div>
                </div>
                <div class="footer">
                    <p>© 2024 The Big IP Machine. All rights reserved.</p>
                    <p>Professional Intellectual Property Tokenization Platform</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Attach HTML content
        html_part = MIMEText(html_content, 'html')
        msg.attach(html_part)
        
        # For demo purposes, we'll simulate sending the email
        print(f"[EMAIL SIMULATION] Verification email sent to {email}")
        print(f"[EMAIL SIMULATION] Verification token: {token}")
        print(f"[EMAIL SIMULATION] Verification URL: http://localhost:5000/verify-email?token={token}")
        
        return True
        
    except Exception as e:
        print(f"Error sending verification email: {str(e)}")
        return False

@registration_bp.route('/register', methods=['POST'])
def register_user():
    """Handle user registration"""
    try:
        data = request.get_json()
        
        # Extract registration data
        username = data.get('username', '').strip()
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        full_name = data.get('full_name', '').strip()
        company_name = data.get('company_name', '').strip()
        user_type = data.get('user_type', 'creator')
        terms_accepted = data.get('terms_accepted', False)
        privacy_accepted = data.get('privacy_accepted', False)
        marketing_emails = data.get('marketing_emails', False)
        
        # Validation
        if not username or not email or not password:
            return jsonify({
                'success': False,
                'error': 'Username, email, and password are required'
            }), 400
        
        if not terms_accepted or not privacy_accepted:
            return jsonify({
                'success': False,
                'error': 'You must accept the Terms of Service and Privacy Policy'
            }), 400
        
        # Validate username
        username_valid, username_msg = validate_username(username)
        if not username_valid:
            return jsonify({
                'success': False,
                'error': username_msg
            }), 400
        
        # Validate email
        if not validate_email(email):
            return jsonify({
                'success': False,
                'error': 'Please enter a valid email address'
            }), 400
        
        # Validate password
        password_valid, password_msg = validate_password(password)
        if not password_valid:
            return jsonify({
                'success': False,
                'error': password_msg
            }), 400
        
        # Initialize database
        init_user_database()
        
        # Check if user already exists
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute('SELECT id FROM users WHERE username = ? OR email = ?', (username, email))
        existing_user = cursor.fetchone()
        
        if existing_user:
            conn.close()
            return jsonify({
                'success': False,
                'error': 'Username or email already exists'
            }), 409
        
        # Hash password
        password_hash, salt = hash_password(password)
        
        # Generate verification token
        verification_token = generate_verification_token()
        
        # Insert new user
        cursor.execute('''
            INSERT INTO users (
                username, email, password_hash, salt, full_name, company_name,
                user_type, verification_token, terms_accepted, privacy_accepted,
                marketing_emails, email_notifications
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            username, email, password_hash, salt, full_name, company_name,
            user_type, verification_token, terms_accepted, privacy_accepted,
            marketing_emails, True
        ))
        
        user_id = cursor.lastrowid
        
        # Create email verification record
        expires_at = datetime.now() + timedelta(hours=24)
        cursor.execute('''
            INSERT INTO email_verifications (user_id, token, expires_at)
            VALUES (?, ?, ?)
        ''', (user_id, verification_token, expires_at))
        
        conn.commit()
        conn.close()
        
        # Send verification email
        email_sent = send_verification_email(email, username, verification_token)
        
        return jsonify({
            'success': True,
            'message': 'Registration successful! Please check your email to verify your account.',
            'user_id': user_id,
            'email_sent': email_sent,
            'verification_required': True
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Registration failed: {str(e)}'
        }), 500

@registration_bp.route('/verify-email', methods=['GET', 'POST'])
def verify_email():
    """Handle email verification"""
    try:
        token = request.args.get('token') or (request.get_json() or {}).get('token')
        
        if not token:
            return jsonify({
                'success': False,
                'error': 'Verification token is required'
            }), 400
        
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        # Find verification record
        cursor.execute('''
            SELECT ev.user_id, ev.expires_at, ev.used, u.username, u.email
            FROM email_verifications ev
            JOIN users u ON ev.user_id = u.id
            WHERE ev.token = ?
        ''', (token,))
        
        verification = cursor.fetchone()
        
        if not verification:
            conn.close()
            return jsonify({
                'success': False,
                'error': 'Invalid verification token'
            }), 400
        
        user_id, expires_at, used, username, email = verification
        
        # Check if token is expired
        if datetime.now() > datetime.fromisoformat(expires_at):
            conn.close()
            return jsonify({
                'success': False,
                'error': 'Verification token has expired'
            }), 400
        
        # Check if already used
        if used:
            conn.close()
            return jsonify({
                'success': False,
                'error': 'Verification token has already been used'
            }), 400
        
        # Mark email as verified
        cursor.execute('''
            UPDATE users SET email_verified = TRUE WHERE id = ?
        ''', (user_id,))
        
        # Mark token as used
        cursor.execute('''
            UPDATE email_verifications SET used = TRUE WHERE token = ?
        ''', (token,))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': f'Email verified successfully! Welcome to The Big IP Machine, {username}!',
            'user_id': user_id,
            'username': username,
            'email': email
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Email verification failed: {str(e)}'
        }), 500

@registration_bp.route('/resend-verification', methods=['POST'])
def resend_verification():
    """Resend verification email"""
    try:
        data = request.get_json()
        email = data.get('email', '').strip().lower()
        
        if not email:
            return jsonify({
                'success': False,
                'error': 'Email address is required'
            }), 400
        
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        # Find user
        cursor.execute('''
            SELECT id, username, email_verified FROM users WHERE email = ?
        ''', (email,))
        
        user = cursor.fetchone()
        
        if not user:
            conn.close()
            return jsonify({
                'success': False,
                'error': 'No account found with this email address'
            }), 404
        
        user_id, username, email_verified = user
        
        if email_verified:
            conn.close()
            return jsonify({
                'success': False,
                'error': 'Email is already verified'
            }), 400
        
        # Generate new verification token
        verification_token = generate_verification_token()
        expires_at = datetime.now() + timedelta(hours=24)
        
        # Insert new verification record
        cursor.execute('''
            INSERT INTO email_verifications (user_id, token, expires_at)
            VALUES (?, ?, ?)
        ''', (user_id, verification_token, expires_at))
        
        conn.commit()
        conn.close()
        
        # Send verification email
        email_sent = send_verification_email(email, username, verification_token)
        
        return jsonify({
            'success': True,
            'message': 'Verification email sent! Please check your inbox.',
            'email_sent': email_sent
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to resend verification: {str(e)}'
        }), 500

@registration_bp.route('/check-availability', methods=['POST'])
def check_availability():
    """Check username/email availability"""
    try:
        data = request.get_json()
        username = data.get('username', '').strip()
        email = data.get('email', '').strip().lower()
        
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        result = {
            'username_available': True,
            'email_available': True
        }
        
        if username:
            cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
            if cursor.fetchone():
                result['username_available'] = False
        
        if email:
            cursor.execute('SELECT id FROM users WHERE email = ?', (email,))
            if cursor.fetchone():
                result['email_available'] = False
        
        conn.close()
        
        return jsonify({
            'success': True,
            **result
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Availability check failed: {str(e)}'
        }), 500

# Initialize database when module is imported
init_user_database()

