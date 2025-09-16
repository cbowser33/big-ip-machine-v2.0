from flask import Blueprint, jsonify, request, session
import hashlib
import time

auth_bp = Blueprint('auth', __name__)

# Simple in-memory user store for demo
DEMO_USERS = {
    'ui_test_creator': {
        'password': 'UITest2024!',
        'email': 'test@bigip.com',
        'created_at': '2024-08-19',
        'role': 'creator'
    },
    'demo_user': {
        'password': 'Demo123!',
        'email': 'demo@bigip.com', 
        'created_at': '2024-08-19',
        'role': 'user'
    }
}

@auth_bp.route('/login', methods=['POST'])
def login():
    """Handle user login"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'message': 'No data provided'}), 400
            
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        
        if not username or not password:
            return jsonify({'success': False, 'message': 'Username and password required'}), 400
        
        # Check against demo users
        if username in DEMO_USERS:
            if DEMO_USERS[username]['password'] == password:
                # Successful login
                session['user_id'] = username
                session['logged_in'] = True
                session['login_time'] = time.time()
                
                return jsonify({
                    'success': True,
                    'message': 'Login successful',
                    'user': {
                        'username': username,
                        'email': DEMO_USERS[username]['email'],
                        'role': DEMO_USERS[username]['role']
                    }
                }), 200
            else:
                return jsonify({'success': False, 'message': 'Invalid password'}), 401
        else:
            return jsonify({'success': False, 'message': 'User not found'}), 401
            
    except Exception as e:
        return jsonify({'success': False, 'message': f'Login error: {str(e)}'}), 500

@auth_bp.route('/logout', methods=['POST'])
def logout():
    """Handle user logout"""
    try:
        session.clear()
        return jsonify({'success': True, 'message': 'Logged out successfully'}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': f'Logout error: {str(e)}'}), 500

@auth_bp.route('/register', methods=['POST'])
def register():
    """Handle user registration"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'message': 'No data provided'}), 400
            
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        email = data.get('email', '').strip()
        
        if not username or not password or not email:
            return jsonify({'success': False, 'message': 'Username, password, and email required'}), 400
        
        # Check if user already exists
        if username in DEMO_USERS:
            return jsonify({'success': False, 'message': 'Username already exists'}), 409
        
        # Add new user (in production, hash the password!)
        DEMO_USERS[username] = {
            'password': password,
            'email': email,
            'created_at': time.strftime('%Y-%m-%d'),
            'role': 'user'
        }
        
        return jsonify({
            'success': True,
            'message': 'Registration successful',
            'user': {
                'username': username,
                'email': email,
                'role': 'user'
            }
        }), 201
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Registration error: {str(e)}'}), 500

@auth_bp.route('/profile', methods=['GET'])
def get_profile():
    """Get current user profile"""
    try:
        if not session.get('logged_in'):
            return jsonify({'success': False, 'message': 'Not logged in'}), 401
        
        username = session.get('user_id')
        if username and username in DEMO_USERS:
            return jsonify({
                'success': True,
                'user': {
                    'username': username,
                    'email': DEMO_USERS[username]['email'],
                    'role': DEMO_USERS[username]['role'],
                    'created_at': DEMO_USERS[username]['created_at']
                }
            }), 200
        else:
            return jsonify({'success': False, 'message': 'User not found'}), 404
            
    except Exception as e:
        return jsonify({'success': False, 'message': f'Profile error: {str(e)}'}), 500

@auth_bp.route('/check-auth', methods=['GET'])
def check_auth():
    """Check if user is authenticated"""
    try:
        if session.get('logged_in'):
            username = session.get('user_id')
            return jsonify({
                'success': True,
                'authenticated': True,
                'username': username
            }), 200
        else:
            return jsonify({
                'success': True,
                'authenticated': False
            }), 200
            
    except Exception as e:
        return jsonify({'success': False, 'message': f'Auth check error: {str(e)}'}), 500

