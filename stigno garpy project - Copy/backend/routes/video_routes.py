# backend/routes/video_routes.py
from flask import Blueprint, request, current_app, jsonify, url_for
from werkzeug.utils import secure_filename
import os
import secrets
from backend.utils.video_tool import encrypt_video_file, decrypt_video_file

video_bp = Blueprint('video_bp', __name__)

ALLOWED_EXTENSIONS = {'avi', 'mov', 'mp4'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@video_bp.route('/video/encode', methods=['POST'])
def encode_video():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not allowed'}), 400

    # Save file in Flask static folder
    filename = secure_filename(file.filename)
    upload_folder = os.path.join(current_app.static_folder, 'uploads')
    os.makedirs(upload_folder, exist_ok=True)
    filepath = os.path.join(upload_folder, filename)
    file.save(filepath)

    # Generate password if not provided
    password = request.form.get('password') or secrets.token_urlsafe(12)

    try:
        output_filename = f"enc_{filename}"
        output_path = os.path.join(upload_folder, output_filename)
        encrypt_video_file(filepath, output_path, password)

        # Return file URL and password
        file_url = url_for('static', filename=f'uploads/{output_filename}', _external=True)
        return jsonify({
            "file_url": file_url,
            "password": password
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@video_bp.route('/video/decode', methods=['POST'])
def decode_video():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    password = request.form.get('password')
    if not password:
        return jsonify({'error': 'Password required for decryption'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not allowed'}), 400

    # Save file in Flask static folder
    filename = secure_filename(file.filename)
    upload_folder = os.path.join(current_app.static_folder, 'uploads')
    os.makedirs(upload_folder, exist_ok=True)
    filepath = os.path.join(upload_folder, filename)
    file.save(filepath)

    try:
        output_filename = f"dec_{filename}"
        output_path = os.path.join(upload_folder, output_filename)
        decrypt_video_file(filepath, output_path, password)

        # Return file URL
        file_url = url_for('static', filename=f'uploads/{output_filename}', _external=True)
        return jsonify({
            "file_url": file_url
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500
