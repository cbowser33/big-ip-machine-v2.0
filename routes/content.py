"""
Content Upload Routes for Large File Support
Handles uploads up to 50GB for full-length movies
"""

from flask import Blueprint, request, jsonify, current_app
import os
import hashlib
import time
import uuid
import logging
from werkzeug.utils import secure_filename
from typing import Dict, Any

content_bp = Blueprint('content', __name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Allowed file extensions for different media types
ALLOWED_EXTENSIONS = {
    'video': {'mp4', 'mov', 'avi', 'mkv', 'wmv', 'flv', 'webm', 'm4v'},
    'image': {'jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'webp'},
    'audio': {'mp3', 'wav', 'aac', 'flac', 'ogg', 'm4a', 'wma'},
    'document': {'pdf', 'txt', 'doc', 'docx', 'rtf', 'odt'}
}

def allowed_file(filename: str) -> bool:
    """Check if file extension is allowed"""
    if '.' not in filename:
        return False
    
    ext = filename.rsplit('.', 1)[1].lower()
    for category, extensions in ALLOWED_EXTENSIONS.items():
        if ext in extensions:
            return True
    return False

def get_file_category(filename: str) -> str:
    """Determine file category based on extension"""
    if '.' not in filename:
        return 'other'
    
    ext = filename.rsplit('.', 1)[1].lower()
    for category, extensions in ALLOWED_EXTENSIONS.items():
        if ext in extensions:
            return category
    return 'other'

def generate_streaming_hash(file_path: str) -> str:
    """Generate SHA-256 hash using streaming for large files"""
    hash_sha256 = hashlib.sha256()
    try:
        with open(file_path, 'rb') as f:
            # Read file in 64KB chunks to handle very large files efficiently
            for chunk in iter(lambda: f.read(65536), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()
    except Exception as e:
        logger.error(f"Streaming hash generation failed: {str(e)}")
        return hashlib.sha256(str(time.time()).encode()).hexdigest()

def generate_optimized_fingerprint(file_path: str, file_size: int) -> Dict[str, Any]:
    """Generate optimized fingerprint based on file size"""
    try:
        fingerprint = {
            'file_hash': generate_streaming_hash(file_path),
            'file_size': file_size,
            'timestamp': int(time.time()),
            'processing_method': 'optimized' if file_size > 1024*1024*1024 else 'standard'
        }
        
        # For very large files (>1GB), use simplified additional hashing
        if file_size > 1024 * 1024 * 1024:  # 1GB
            logger.info(f"Large file detected ({file_size} bytes) - using optimized processing")
            file_stats = os.stat(file_path)
            fingerprint['metadata_hash'] = hashlib.md5(
                f"{file_stats.st_size}_{file_stats.st_mtime}_{os.path.basename(file_path)}".encode()
            ).hexdigest()
        else:
            # For smaller files, add more detailed fingerprinting
            try:
                with open(file_path, 'rb') as f:
                    sample = f.read(8192)  # Read first 8KB for sample hash
                    fingerprint['sample_hash'] = hashlib.sha1(sample).hexdigest()
            except:
                fingerprint['sample_hash'] = 'unavailable'
        
        return fingerprint
        
    except Exception as e:
        logger.error(f"Fingerprint generation error: {str(e)}")
        return {
            'file_hash': generate_streaming_hash(file_path),
            'error': str(e),
            'timestamp': int(time.time()),
            'file_size': file_size
        }

@content_bp.route('/upload', methods=['POST'])
def upload_content():
    """Upload content with support for very large files (up to 50GB)"""
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No file provided'
            }), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No file selected'
            }), 400
        
        # Validate file extension
        if not allowed_file(file.filename):
            return jsonify({
                'success': False,
                'error': f'File type not supported. Allowed types: {", ".join([ext for exts in ALLOWED_EXTENSIONS.values() for ext in exts])}'
            }), 400
        
        # Get form data
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        creator = request.form.get('creator', 'anonymous').strip()
        
        if not title:
            return jsonify({
                'success': False,
                'error': 'Title is required'
            }), 400
        
        # Generate unique content ID
        content_id = str(uuid.uuid4())
        
        # Prepare file path and ensure upload directory exists
        upload_folder = current_app.config['UPLOAD_FOLDER']
        os.makedirs(upload_folder, exist_ok=True)
        
        filename = secure_filename(file.filename)
        file_extension = filename.rsplit('.', 1)[1].lower()
        safe_filename = f"{content_id}.{file_extension}"
        file_path = os.path.join(upload_folder, safe_filename)
        
        # Log upload start
        logger.info(f"Starting upload: {filename} -> {safe_filename}")
        logger.info(f"Upload folder: {upload_folder}")
        logger.info(f"Full file path: {file_path}")
        start_time = time.time()
        
        # Save file with streaming for large files
        try:
            file.save(file_path)
            file_size = os.path.getsize(file_path)
            upload_time = time.time() - start_time
            
            logger.info(f"Upload completed: {file_size:,} bytes in {upload_time:.2f} seconds ({file_size/upload_time/1024/1024:.2f} MB/s)")
            
        except Exception as e:
            logger.error(f"File save failed: {str(e)}")
            return jsonify({
                'success': False,
                'error': f'File save failed: {str(e)}'
            }), 500
        
        # Generate fingerprint
        logger.info("Generating content fingerprint...")
        fingerprint_start = time.time()
        
        try:
            fingerprint_data = generate_optimized_fingerprint(file_path, file_size)
            fingerprint_time = time.time() - fingerprint_start
            logger.info(f"Fingerprint generated in {fingerprint_time:.2f} seconds")
            
        except Exception as e:
            logger.error(f"Fingerprint generation failed: {str(e)}")
            fingerprint_data = {
                'file_hash': 'error',
                'error': str(e),
                'timestamp': int(time.time())
            }
        
        # Create metadata
        metadata = {
            'content_id': content_id,
            'title': title,
            'description': description,
            'creator': creator,
            'filename': filename,
            'safe_filename': safe_filename,
            'file_path': file_path,
            'file_size': file_size,
            'file_category': get_file_category(filename),
            'upload_timestamp': int(time.time()),
            'upload_duration': upload_time,
            'fingerprint': fingerprint_data
        }
        
        logger.info(f"Content upload successful: {content_id}")
        
        return jsonify({
            'success': True,
            'message': 'File uploaded successfully',
            'content_id': content_id,
            'file_size': file_size,
            'file_size_mb': round(file_size / 1024 / 1024, 2),
            'upload_time': round(upload_time, 2),
            'metadata': metadata
        })
        
    except Exception as e:
        logger.error(f"Upload error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@content_bp.route('/status/<content_id>', methods=['GET'])
def get_content_status(content_id):
    """Get status of uploaded content"""
    try:
        # In a real implementation, this would query a database
        # For testing, we'll check if the file exists
        upload_folder = current_app.config['UPLOAD_FOLDER']
        
        # Find file with this content_id
        for filename in os.listdir(upload_folder):
            if filename.startswith(content_id):
                file_path = os.path.join(upload_folder, filename)
                file_size = os.path.getsize(file_path)
                
                return jsonify({
                    'success': True,
                    'content_id': content_id,
                    'status': 'uploaded',
                    'file_size': file_size,
                    'file_size_mb': round(file_size / 1024 / 1024, 2),
                    'filename': filename
                })
        
        return jsonify({
            'success': False,
            'error': 'Content not found'
        }), 404
        
    except Exception as e:
        logger.error(f"Status check error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@content_bp.route('/list', methods=['GET'])
def list_content():
    """List all uploaded content"""
    try:
        upload_folder = current_app.config['UPLOAD_FOLDER']
        files = []
        
        for filename in os.listdir(upload_folder):
            file_path = os.path.join(upload_folder, filename)
            file_size = os.path.getsize(file_path)
            
            files.append({
                'filename': filename,
                'file_size': file_size,
                'file_size_mb': round(file_size / 1024 / 1024, 2),
                'upload_time': os.path.getctime(file_path)
            })
        
        # Sort by upload time (newest first)
        files.sort(key=lambda x: x['upload_time'], reverse=True)
        
        return jsonify({
            'success': True,
            'files': files,
            'total_files': len(files),
            'total_size_mb': sum(f['file_size_mb'] for f in files)
        })
        
    except Exception as e:
        logger.error(f"List content error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

