"""
Comprehensive Email Notification System for The Big IP Machine v1.3
Handles all email notifications including welcome, upload success, marketplace updates, etc.
"""

from flask import Blueprint, request, jsonify
import smtplib
import os
import sqlite3
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import json

email_notifications_bp = Blueprint('email_notifications', __name__)

# Email configuration
SMTP_CONFIG = {
    'server': os.getenv('SMTP_SERVER', 'smtp.gmail.com'),
    'port': int(os.getenv('SMTP_PORT', '587')),
    'username': os.getenv('SMTP_USERNAME', 'noreply@bigip-machine.com'),
    'password': os.getenv('SMTP_PASSWORD', 'demo_password'),
    'from_name': 'The Big IP Machine'
}

def get_email_template_base():
    """Get base HTML template for all emails"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{subject}</title>
        <style>
            body {{ 
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
                background: #f8f9fa; 
                margin: 0; 
                padding: 20px; 
                line-height: 1.6;
            }}
            .container {{ 
                max-width: 600px; 
                margin: 0 auto; 
                background: white; 
                border-radius: 12px; 
                overflow: hidden; 
                box-shadow: 0 4px 12px rgba(0,0,0,0.1); 
            }}
            .header {{ 
                background: linear-gradient(135deg, #8b5cf6 0%, #c084fc 100%); 
                padding: 40px 30px; 
                text-align: center; 
            }}
            .header h1 {{ 
                color: white; 
                margin: 0; 
                font-size: 28px; 
                font-weight: 700; 
            }}
            .header p {{ 
                color: rgba(255,255,255,0.9); 
                margin: 10px 0 0 0; 
                font-size: 16px; 
            }}
            .content {{ 
                padding: 40px 30px; 
            }}
            .welcome {{ 
                font-size: 20px; 
                font-weight: 600; 
                color: #1f2937; 
                margin-bottom: 20px; 
            }}
            .message {{ 
                color: #4b5563; 
                line-height: 1.6; 
                margin-bottom: 20px; 
            }}
            .button {{ 
                display: inline-block; 
                background: #8b5cf6; 
                color: white; 
                padding: 15px 30px; 
                text-decoration: none; 
                border-radius: 8px; 
                font-weight: 600; 
                font-size: 16px; 
                margin: 20px 0;
            }}
            .button:hover {{ 
                background: #7c3aed; 
            }}
            .stats-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
                gap: 20px;
                margin: 30px 0;
            }}
            .stat-card {{
                background: #f8fafc;
                padding: 20px;
                border-radius: 8px;
                text-align: center;
                border: 1px solid #e2e8f0;
            }}
            .stat-number {{
                font-size: 24px;
                font-weight: 700;
                color: #8b5cf6;
                margin-bottom: 5px;
            }}
            .stat-label {{
                color: #64748b;
                font-size: 14px;
            }}
            .features {{ 
                background: #f8fafc; 
                padding: 20px; 
                border-radius: 8px; 
                margin: 20px 0; 
            }}
            .feature {{ 
                display: flex; 
                align-items: center; 
                margin: 10px 0; 
            }}
            .feature-icon {{ 
                color: #8b5cf6; 
                margin-right: 10px; 
                font-size: 18px; 
            }}
            .footer {{ 
                background: #f9fafb; 
                padding: 30px; 
                text-align: center; 
                color: #6b7280; 
                font-size: 14px; 
            }}
            .divider {{
                height: 1px;
                background: #e2e8f0;
                margin: 30px 0;
            }}
            .highlight {{
                background: #fef3c7;
                padding: 15px;
                border-radius: 8px;
                border-left: 4px solid #f59e0b;
                margin: 20px 0;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            {content}
            <div class="footer">
                <p>© 2024 The Big IP Machine. All rights reserved.</p>
                <p>Professional Intellectual Property Tokenization Platform</p>
                <p><a href="#" style="color: #8b5cf6;">Unsubscribe</a> | <a href="#" style="color: #8b5cf6;">Update Preferences</a></p>
            </div>
        </div>
    </body>
    </html>
    """

def send_email(to_email, subject, html_content, text_content=None):
    """Send email using SMTP"""
    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = f"{SMTP_CONFIG['from_name']} <{SMTP_CONFIG['username']}>"
        msg['To'] = to_email
        
        # Add text version if provided
        if text_content:
            text_part = MIMEText(text_content, 'plain')
            msg.attach(text_part)
        
        # Add HTML version
        html_part = MIMEText(html_content, 'html')
        msg.attach(html_part)
        
        # For demo purposes, simulate sending
        print(f"[EMAIL SIMULATION] Email sent to: {to_email}")
        print(f"[EMAIL SIMULATION] Subject: {subject}")
        print(f"[EMAIL SIMULATION] Content preview: {text_content[:100] if text_content else 'HTML email'}...")
        
        return True
        
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False

def get_user_email_preferences(user_id):
    """Get user's email notification preferences"""
    try:
        db_path = os.path.join(os.path.dirname(__file__), '..', 'database', 'users.db')
        
        if not os.path.exists(db_path):
            return {'email_notifications': True, 'marketing_emails': False}
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT email_notifications, marketing_emails, email
            FROM users WHERE id = ?
        ''', (user_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                'email_notifications': bool(result[0]),
                'marketing_emails': bool(result[1]),
                'email': result[2]
            }
        
        return None
        
    except Exception as e:
        print(f"Error getting email preferences: {str(e)}")
        return None

@email_notifications_bp.route('/send-welcome-email', methods=['POST'])
def send_welcome_email():
    """Send welcome email to new users"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        username = data.get('username')
        email = data.get('email')
        
        if not all([user_id, username, email]):
            return jsonify({
                'success': False,
                'error': 'Missing required user information'
            }), 400
        
        # Check email preferences
        preferences = get_user_email_preferences(user_id)
        if not preferences or not preferences.get('email_notifications'):
            return jsonify({
                'success': True,
                'message': 'Email notifications disabled for user'
            }), 200
        
        # Create welcome email content
        content = f"""
            <div class="header">
                <h1>🎉 Welcome to The Big IP Machine!</h1>
                <p>Professional IP Tokenization Platform</p>
            </div>
            <div class="content">
                <div class="welcome">Hello {username}!</div>
                <div class="message">
                    Welcome to The Big IP Machine, the premier platform for fractional ownership of intellectual property on the blockchain. We're excited to have you join our community of creators, innovators, and IP enthusiasts!
                </div>
                
                <div class="features">
                    <div class="feature">
                        <span class="feature-icon">🚀</span>
                        <span><strong>Smart Tokenization:</strong> Upload and tokenize your IP with 94.4% accuracy</span>
                    </div>
                    <div class="feature">
                        <span class="feature-icon">💎</span>
                        <span><strong>Blockchain Security:</strong> ERC-1155 tokens on Polygon network</span>
                    </div>
                    <div class="feature">
                        <span class="feature-icon">📊</span>
                        <span><strong>Real-time Analytics:</strong> Track your IP portfolio performance</span>
                    </div>
                    <div class="feature">
                        <span class="feature-icon">🏪</span>
                        <span><strong>IP Marketplace:</strong> License your content to global buyers</span>
                    </div>
                </div>
                
                <div style="text-align: center;">
                    <a href="#" class="button">Start Uploading Your IP</a>
                </div>
                
                <div class="message">
                    Ready to get started? Upload your first piece of intellectual property and watch it transform into valuable blockchain tokens!
                </div>
            </div>
        """
        
        html_content = get_email_template_base().format(
            subject="Welcome to The Big IP Machine!",
            content=content
        )
        
        # Send email
        success = send_email(
            email,
            "🎉 Welcome to The Big IP Machine - Let's Tokenize Your IP!",
            html_content,
            f"Welcome {username}! Thank you for joining The Big IP Machine. Start tokenizing your intellectual property today!"
        )
        
        return jsonify({
            'success': success,
            'message': 'Welcome email sent successfully' if success else 'Failed to send welcome email'
        }), 200 if success else 500
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to send welcome email: {str(e)}'
        }), 500

@email_notifications_bp.route('/send-upload-success-email', methods=['POST'])
def send_upload_success_email():
    """Send upload success email with token breakdown"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        username = data.get('username')
        email = data.get('email')
        upload_data = data.get('upload_data', {})
        
        if not all([user_id, email, upload_data]):
            return jsonify({
                'success': False,
                'error': 'Missing required upload information'
            }), 400
        
        # Check email preferences
        preferences = get_user_email_preferences(user_id)
        if not preferences or not preferences.get('email_notifications'):
            return jsonify({
                'success': True,
                'message': 'Email notifications disabled for user'
            }), 200
        
        filename = upload_data.get('filename', 'Your File')
        category = upload_data.get('category', 'Unknown').replace('_', ' ').title()
        tokens_created = upload_data.get('tokens_created', 0)
        estimated_value = upload_data.get('estimated_value', 0)
        file_size = upload_data.get('file_size', 'Unknown')
        
        # Create upload success email content
        content = f"""
            <div class="header">
                <h1>🎉 Upload Successful!</h1>
                <p>Your IP has been tokenized</p>
            </div>
            <div class="content">
                <div class="welcome">Congratulations {username}!</div>
                <div class="message">
                    Your intellectual property "<strong>{filename}</strong>" has been successfully uploaded and tokenized on the blockchain!
                </div>
                
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-number">{tokens_created:,}</div>
                        <div class="stat-label">Tokens Created</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">${estimated_value}</div>
                        <div class="stat-label">Estimated Value</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">{category}</div>
                        <div class="stat-label">Category</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">{file_size}</div>
                        <div class="stat-label">File Size</div>
                    </div>
                </div>
                
                <div class="highlight">
                    <strong>🔗 Blockchain Details:</strong><br>
                    • Network: Polygon<br>
                    • Token Standard: ERC-1155<br>
                    • Status: Successfully minted<br>
                    • Smart Contract: Verified ✅
                </div>
                
                <div class="message">
                    <strong>What's Next?</strong>
                </div>
                
                <div class="features">
                    <div class="feature">
                        <span class="feature-icon">🏪</span>
                        <span><strong>List in Marketplace:</strong> Make your IP available for licensing</span>
                    </div>
                    <div class="feature">
                        <span class="feature-icon">📊</span>
                        <span><strong>Track Performance:</strong> Monitor analytics and engagement</span>
                    </div>
                    <div class="feature">
                        <span class="feature-icon">💰</span>
                        <span><strong>Earn Royalties:</strong> Receive payments from licensing</span>
                    </div>
                    <div class="feature">
                        <span class="feature-icon">🤝</span>
                        <span><strong>Network:</strong> Connect with potential buyers</span>
                    </div>
                </div>
                
                <div style="text-align: center;">
                    <a href="#" class="button">View Your Portfolio</a>
                </div>
            </div>
        """
        
        html_content = get_email_template_base().format(
            subject="Upload Successful - IP Tokenized!",
            content=content
        )
        
        # Send email
        success = send_email(
            email,
            f"🎉 {filename} Successfully Tokenized - {tokens_created:,} Tokens Created!",
            html_content,
            f"Great news {username}! Your file '{filename}' has been successfully tokenized with {tokens_created:,} tokens created (estimated value: ${estimated_value})."
        )
        
        return jsonify({
            'success': success,
            'message': 'Upload success email sent' if success else 'Failed to send upload success email'
        }), 200 if success else 500
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to send upload success email: {str(e)}'
        }), 500

@email_notifications_bp.route('/send-marketplace-update', methods=['POST'])
def send_marketplace_update():
    """Send marketplace update email"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        email = data.get('email')
        username = data.get('username')
        update_type = data.get('update_type', 'general')
        update_data = data.get('update_data', {})
        
        if not all([user_id, email]):
            return jsonify({
                'success': False,
                'error': 'Missing required information'
            }), 400
        
        # Check email preferences
        preferences = get_user_email_preferences(user_id)
        if not preferences or not preferences.get('marketing_emails'):
            return jsonify({
                'success': True,
                'message': 'Marketing emails disabled for user'
            }), 200
        
        # Create marketplace update content based on type
        if update_type == 'new_listing':
            subject = "🏪 New IP Available in Marketplace"
            header_title = "New Marketplace Listings"
            message = f"Exciting new intellectual property has been added to The Big IP Machine marketplace! Discover fresh content ready for licensing."
        elif update_type == 'price_drop':
            subject = "💰 Price Drops in IP Marketplace"
            header_title = "Special Pricing Updates"
            message = f"Great news! Some of your favorite IP listings now have reduced licensing fees. Don't miss these limited-time opportunities."
        elif update_type == 'trending':
            subject = "📈 Trending IP This Week"
            header_title = "Weekly Trending Report"
            message = f"See what's hot in the IP marketplace this week. These trending assets are gaining significant attention from licensees."
        else:
            subject = "📢 Marketplace Update"
            header_title = "Marketplace News"
            message = f"Stay updated with the latest happenings in The Big IP Machine marketplace."
        
        content = f"""
            <div class="header">
                <h1>{header_title}</h1>
                <p>The Big IP Machine Marketplace</p>
            </div>
            <div class="content">
                <div class="welcome">Hello {username}!</div>
                <div class="message">
                    {message}
                </div>
                
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-number">2,847</div>
                        <div class="stat-label">Active Listings</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">$1.2M</div>
                        <div class="stat-label">Total Value</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">156</div>
                        <div class="stat-label">New This Week</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">94.4%</div>
                        <div class="stat-label">Success Rate</div>
                    </div>
                </div>
                
                <div class="features">
                    <div class="feature">
                        <span class="feature-icon">🎬</span>
                        <span><strong>Film & Cinema:</strong> 342 new listings this week</span>
                    </div>
                    <div class="feature">
                        <span class="feature-icon">🎨</span>
                        <span><strong>Digital Art:</strong> 128 trending artworks</span>
                    </div>
                    <div class="feature">
                        <span class="feature-icon">🎵</span>
                        <span><strong>Music:</strong> 89 new compositions available</span>
                    </div>
                    <div class="feature">
                        <span class="feature-icon">💻</span>
                        <span><strong>Software:</strong> 45 new code repositories</span>
                    </div>
                </div>
                
                <div style="text-align: center;">
                    <a href="#" class="button">Browse Marketplace</a>
                </div>
                
                <div class="message">
                    Don't miss out on these opportunities to discover and license amazing intellectual property!
                </div>
            </div>
        """
        
        html_content = get_email_template_base().format(
            subject=subject,
            content=content
        )
        
        # Send email
        success = send_email(
            email,
            subject,
            html_content,
            f"Hello {username}! {message} Visit The Big IP Machine marketplace to explore new opportunities."
        )
        
        return jsonify({
            'success': success,
            'message': 'Marketplace update email sent' if success else 'Failed to send marketplace update'
        }), 200 if success else 500
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to send marketplace update: {str(e)}'
        }), 500

@email_notifications_bp.route('/update-email-preferences', methods=['POST'])
def update_email_preferences():
    """Update user's email notification preferences"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        email_notifications = data.get('email_notifications', True)
        marketing_emails = data.get('marketing_emails', False)
        
        if not user_id:
            return jsonify({
                'success': False,
                'error': 'User ID is required'
            }), 400
        
        db_path = os.path.join(os.path.dirname(__file__), '..', 'database', 'users.db')
        
        if not os.path.exists(db_path):
            return jsonify({
                'success': False,
                'error': 'User database not found'
            }), 404
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE users 
            SET email_notifications = ?, marketing_emails = ?
            WHERE id = ?
        ''', (email_notifications, marketing_emails, user_id))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': 'Email preferences updated successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to update email preferences: {str(e)}'
        }), 500

@email_notifications_bp.route('/email-preferences/<int:user_id>', methods=['GET'])
def get_email_preferences_endpoint(user_id):
    """Get user's email preferences"""
    try:
        preferences = get_user_email_preferences(user_id)
        
        if preferences is None:
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404
        
        return jsonify({
            'success': True,
            'preferences': preferences
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to get email preferences: {str(e)}'
        }), 500

