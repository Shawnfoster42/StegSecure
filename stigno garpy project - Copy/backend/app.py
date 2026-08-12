# backend/app.py
from flask import Flask, request, send_file, jsonify, render_template
from werkzeug.utils import secure_filename
import os

# Routes
from backend.routes.encode import encode_file
from backend.routes.decode import decode_file
from backend.routes.video_routes import video_bp  # Register blueprint

# Define key paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # backend/
ROOT_DIR = os.path.dirname(BASE_DIR)                   # project root
FRONTEND_DIR = os.path.join(ROOT_DIR, 'frontend')      # frontend/
STATIC_DIR = os.path.join(BASE_DIR, 'static')          # backend/static
UPLOAD_FOLDER = os.path.join(STATIC_DIR, 'uploads')

# Allowed extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp', 'wav', 'mp3', 'mp4', 'avi', 'mov'}

# Create Flask app
app = Flask(
    __name__,
    template_folder=os.path.join(ROOT_DIR, 'frontend'),
    static_folder=os.path.join(ROOT_DIR, 'frontend', 'static')
)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 * 1024  # 200MB max

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Register the video blueprint
app.register_blueprint(video_bp)

# ---------------- Helper Functions ----------------
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ---------------- Routes for Image/Audio ----------------
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/encode', methods=['POST'])
def encode():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    message = request.form.get('message', '')
    password = request.form.get('password', '')

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        try:
            output_path = encode_file(filepath, message, password)
            return send_file(output_path, as_attachment=True)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'File type not allowed'}), 400

@app.route('/decode', methods=['POST'])
def decode():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    password = request.form.get('password', '')

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        try:
            secret_message = decode_file(filepath, password)
            return jsonify({'message': secret_message})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'File type not allowed'}), 400

# ---------------- Run ----------------
if __name__ == "__main__":
    app.run(debug=True)
