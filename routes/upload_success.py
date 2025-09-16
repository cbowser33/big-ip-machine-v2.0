"""
Upload Success Splash Screen System for The Big IP Machine v1.3
Handles congratulatory splash screens with token breakdown and email notifications
"""

from flask import Blueprint, request, jsonify, session
import json
import os
from datetime import datetime
import sqlite3

upload_success_bp = Blueprint('upload_success', __name__)

def calculate_token_breakdown(file_info, category, file_size_mb):
    """Calculate detailed token breakdown based on content analysis"""
    
    # Ensure file_size_mb is a float
    file_size_mb = float(file_size_mb)
    
    # Base token calculation
    base_tokens = 1000  # Base tokens for any IP
    
    # Category multipliers
    category_multipliers = {
        'film_cinema': 5.0,
        'animation': 4.5,
        'screenplay': 3.0,
        'book_writing': 3.5,
        'digital_art': 2.5,
        'photography': 2.0,
        'music': 3.0,
        'podcast': 2.5,
        'software': 4.0,
        'video_games': 4.5
    }
    
    # File size bonus (per MB)
    size_bonus = min(file_size_mb * 0.1, 500)  # Cap at 500 bonus tokens
    
    # Quality factors
    quality_multiplier = 1.0
    if file_size_mb > 100:  # High quality/large files
        quality_multiplier = 1.2
    elif file_size_mb > 1000:  # Very large files (movies, etc.)
        quality_multiplier = 1.5
    
    # Calculate total tokens
    category_multiplier = category_multipliers.get(category, 2.0)
    total_tokens = int((base_tokens * category_multiplier + size_bonus) * quality_multiplier)
    
    # Token distribution breakdown
    breakdown = {
        'total_tokens': total_tokens,
        'base_tokens': base_tokens,
        'category_bonus': int(base_tokens * (category_multiplier - 1)),
        'size_bonus': int(size_bonus),
        'quality_bonus': int(total_tokens * (quality_multiplier - 1)),
        'category': category,
        'category_multiplier': category_multiplier,
        'file_size_mb': file_size_mb,
        'estimated_value': round(total_tokens * 0.01, 2)  # $0.01 per token estimate
    }
    
    return breakdown

def generate_success_message(filename, category, token_breakdown):
    """Generate personalized success message"""
    
    category_messages = {
        'film_cinema': "🎬 Your cinematic masterpiece has been successfully tokenized!",
        'animation': "🎨 Your animated creation is now ready for the blockchain!",
        'screenplay': "📝 Your screenplay has been professionally tokenized!",
        'book_writing': "📚 Your literary work is now blockchain-ready!",
        'digital_art': "🖼️ Your digital artwork has been successfully tokenized!",
        'photography': "📸 Your photograph is now part of the IP marketplace!",
        'music': "🎵 Your musical composition has been tokenized!",
        'podcast': "🎙️ Your podcast content is now blockchain-ready!",
        'software': "💻 Your software has been successfully tokenized!",
        'video_games': "🎮 Your game content is now ready for licensing!"
    }
    
    base_message = category_messages.get(category, "🚀 Your intellectual property has been successfully tokenized!")
    
    return {
        'title': 'Congratulations!',
        'message': base_message,
        'subtitle': f'"{filename}" is now protected and ready for fractional ownership.',
        'tokens_created': token_breakdown['total_tokens'],
        'estimated_value': f"${token_breakdown['estimated_value']}"
    }

@upload_success_bp.route('/upload-success', methods=['POST'])
def handle_upload_success():
    """Handle upload success and generate splash screen data"""
    try:
        data = request.get_json()
        
        # Extract upload information
        filename = data.get('filename', 'Unknown File')
        category = data.get('category', 'unknown')
        file_size_mb = float(data.get('file_size_mb', 0))  # Convert to float
        user_id = data.get('user_id') or session.get('user_id')
        upload_id = data.get('upload_id')
        
        # Additional file information
        file_info = {
            'filename': filename,
            'category': category,
            'file_size_mb': file_size_mb,
            'upload_timestamp': datetime.now().isoformat(),
            'user_id': user_id
        }
        
        # Calculate token breakdown
        token_breakdown = calculate_token_breakdown(file_info, category, file_size_mb)
        
        # Generate success message
        success_message = generate_success_message(filename, category, token_breakdown)
        
        # Create comprehensive response
        response_data = {
            'success': True,
            'splash_screen': {
                **success_message,
                'file_info': {
                    'filename': filename,
                    'category': category.replace('_', ' ').title(),
                    'file_size': f"{file_size_mb:.1f} MB",
                    'upload_time': datetime.now().strftime('%B %d, %Y at %I:%M %p')
                },
                'token_breakdown': {
                    'total_tokens': token_breakdown['total_tokens'],
                    'breakdown_details': [
                        {
                            'label': 'Base Tokens',
                            'value': token_breakdown['base_tokens'],
                            'description': 'Standard tokens for IP registration'
                        },
                        {
                            'label': 'Category Bonus',
                            'value': token_breakdown['category_bonus'],
                            'description': f'Bonus for {category.replace("_", " ").title()} content'
                        },
                        {
                            'label': 'Size Bonus',
                            'value': token_breakdown['size_bonus'],
                            'description': f'Bonus for {float(file_size_mb):.1f} MB file size'
                        },
                        {
                            'label': 'Quality Bonus',
                            'value': token_breakdown['quality_bonus'],
                            'description': 'Bonus for high-quality content'
                        }
                    ],
                    'estimated_value': token_breakdown['estimated_value'],
                    'blockchain_network': 'Polygon',
                    'token_standard': 'ERC-1155'
                },
                'next_steps': [
                    {
                        'icon': '🏪',
                        'title': 'List in Marketplace',
                        'description': 'Make your IP available for licensing'
                    },
                    {
                        'icon': '📊',
                        'title': 'Track Performance',
                        'description': 'Monitor your IP portfolio analytics'
                    },
                    {
                        'icon': '💰',
                        'title': 'Earn Royalties',
                        'description': 'Receive payments from IP licensing'
                    },
                    {
                        'icon': '🤝',
                        'title': 'Connect with Buyers',
                        'description': 'Network with potential licensees'
                    }
                ]
            },
            'email_notification': {
                'should_send': True,
                'user_id': user_id,
                'notification_type': 'upload_success'
            }
        }
        
        # Store upload success record
        if user_id:
            store_upload_success_record(user_id, filename, category, token_breakdown)
        
        return jsonify(response_data), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to generate upload success data: {str(e)}'
        }), 500

def store_upload_success_record(user_id, filename, category, token_breakdown):
    """Store upload success record in database"""
    try:
        # Database path
        db_path = os.path.join(os.path.dirname(__file__), '..', 'database', 'uploads.db')
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Create uploads table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS upload_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                filename TEXT NOT NULL,
                category TEXT NOT NULL,
                tokens_created INTEGER NOT NULL,
                estimated_value REAL NOT NULL,
                file_size_mb REAL NOT NULL,
                upload_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                blockchain_status TEXT DEFAULT 'pending',
                marketplace_listed BOOLEAN DEFAULT FALSE
            )
        ''')
        
        # Insert upload record
        cursor.execute('''
            INSERT INTO upload_records (
                user_id, filename, category, tokens_created, estimated_value, file_size_mb
            ) VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            user_id,
            filename,
            category,
            token_breakdown['total_tokens'],
            token_breakdown['estimated_value'],
            token_breakdown['file_size_mb']
        ))
        
        conn.commit()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"Error storing upload record: {str(e)}")
        return False

@upload_success_bp.route('/user-uploads/<int:user_id>', methods=['GET'])
def get_user_uploads(user_id):
    """Get user's upload history"""
    try:
        db_path = os.path.join(os.path.dirname(__file__), '..', 'database', 'uploads.db')
        
        if not os.path.exists(db_path):
            return jsonify({
                'success': True,
                'uploads': []
            }), 200
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT filename, category, tokens_created, estimated_value, 
                   file_size_mb, upload_timestamp, blockchain_status, marketplace_listed
            FROM upload_records 
            WHERE user_id = ? 
            ORDER BY upload_timestamp DESC
        ''', (user_id,))
        
        uploads = []
        for row in cursor.fetchall():
            uploads.append({
                'filename': row[0],
                'category': row[1].replace('_', ' ').title(),
                'tokens_created': row[2],
                'estimated_value': row[3],
                'file_size_mb': row[4],
                'upload_timestamp': row[5],
                'blockchain_status': row[6],
                'marketplace_listed': row[7]
            })
        
        conn.close()
        
        return jsonify({
            'success': True,
            'uploads': uploads,
            'total_uploads': len(uploads),
            'total_tokens': sum(upload['tokens_created'] for upload in uploads),
            'total_estimated_value': sum(upload['estimated_value'] for upload in uploads)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to retrieve uploads: {str(e)}'
        }), 500

@upload_success_bp.route('/upload-stats', methods=['GET'])
def get_upload_stats():
    """Get platform-wide upload statistics"""
    try:
        db_path = os.path.join(os.path.dirname(__file__), '..', 'database', 'uploads.db')
        
        if not os.path.exists(db_path):
            return jsonify({
                'success': True,
                'stats': {
                    'total_uploads': 0,
                    'total_tokens': 0,
                    'total_value': 0,
                    'categories': {}
                }
            }), 200
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get overall stats
        cursor.execute('''
            SELECT COUNT(*), SUM(tokens_created), SUM(estimated_value)
            FROM upload_records
        ''')
        
        total_uploads, total_tokens, total_value = cursor.fetchone()
        
        # Get category breakdown
        cursor.execute('''
            SELECT category, COUNT(*), SUM(tokens_created)
            FROM upload_records
            GROUP BY category
        ''')
        
        categories = {}
        for row in cursor.fetchall():
            categories[row[0]] = {
                'count': row[1],
                'tokens': row[2]
            }
        
        conn.close()
        
        return jsonify({
            'success': True,
            'stats': {
                'total_uploads': total_uploads or 0,
                'total_tokens': total_tokens or 0,
                'total_value': total_value or 0,
                'categories': categories
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to retrieve stats: {str(e)}'
        }), 500

