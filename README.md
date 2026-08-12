Web Steganography Tool – Dependency Installation
1. Pre-requisites

Before installing the dependencies, ensure the following:

Python 3.11+ (preferably 3.12–3.13) is installed on your system.

Pip is installed and updated. You can check with:

python --version
pip --version


PowerShell (Windows) or Terminal (Linux/Mac) is available.

2. Virtual Environment Setup (Recommended)

Using a virtual environment ensures that all dependencies for this project are isolated from global Python packages:

Create a virtual environment in your project folder:

python -m venv venv


Activate the virtual environment:

Windows (PowerShell):

.\venv\Scripts\activate


Linux / Mac:

source venv/bin/activate


You should see (venv) at the start of your terminal prompt.

3. Install Dependencies

The project depends on several Python packages:

Flask – web framework

Werkzeug – Flask dependency

Cryptography – for optional message encryption

Pillow (PIL) – image processing

OpenCV (opencv-python) – video processing

NumPy – numerical computations

To install the latest compatible versions, run:

pip install --upgrade Flask Werkzeug cryptography numpy opencv-python Pillow --only-binary :all:


Notes:

--upgrade ensures the latest version compatible with your Python is installed.

--only-binary :all: ensures precompiled binaries are used for Pillow to avoid Windows build errors.

4. Verify Installation

After installing dependencies, run:

python -c "import flask, werkzeug, cryptography, PIL, cv2, numpy; print('All OK!')"


Expected output:

All OK!


This confirms that all required libraries are installed correctly.

5. Running the Application

Once dependencies are installed:

python backend\app.py


or using Flask CLI:

set FLASK_APP=backend\app.py
set FLASK_ENV=development
flask run


Open your browser at http://127.0.0.1:5000/ to access the Web Steganography Tool.

6. Optional Tips

Keep your virtual environment activated whenever working on this project.

To deactivate:

deactivate


Always install new Python packages inside the venv to avoid conflicts.


🔐 Project Overview

This is a Flask-based Steganography Web Application that allows users to hide secret messages in Image, Audio, and Video files.
✅ Supports Drag & Drop uploads
✅ Password-based encryption
✅ Works for Encoding & Decoding
✅ Shows video encryption password with View/Hide toggle

🛠 Features
Feature	Image	Audio	Video
Hide Text Message	✅	✅	✅
Extract Message	✅	✅	✅
Password Protection	✅	✅	✅
Live Preview	✅	✅	✅
Drag and Drop Support	✅	✅	✅
File Validation	✅ (JPEG/PNG)	✅ (WAV only)	✅ (MP4, AVI, MOV)
📁 Project Structure
project/
│
├─ backend/
│  ├─ app.py
│  ├─ routes/
│  │  ├─ image_routes.py
│  │  ├─ audio_routes.py
│  │  ├─ video_routes.py
│  ├─ utils/
│     ├─ image_tool.py
│     ├─ audio_tool.py
│     ├─ video_tool.py
│
├─ static/
│  ├─ style.css
│  ├─ script.js
│
└─ templates/
   └─ index.html

✅ Requirements

Install Python 3.9+ then run:

pip install -r requirements.txt


If you don’t have requirements.txt, install dependencies manually:

pip install Flask cryptography


📝 Flask — main backend
🔐 cryptography — secure AES-based encryption for video
📦 Werkzeug — filename security (comes with flask install)

▶️ How to Run the Application
cd stigno garpy project
python -m backend.app


Server Running At:

http://127.0.0.1:5000


Then visit the URL in a browser ✅

🔍 Usage Instructions
🖼 Image & 🔊 Audio

1️⃣ Upload a supported file
2️⃣ Enter message & password
3️⃣ Click Encode
4️⃣ Download the encrypted output file
5️⃣ To decode → upload the encrypted file, enter same password → Decode

✅ Decoded message appears on screen

🎥 Video Steganography

1️⃣ Upload MP4/AVI/MOV video
2️⃣ Click Encode
3️⃣ System generates a secure password
4️⃣ Encrypted video auto-downloads
5️⃣ Store the password (or reveal it using 👁 toggle)
6️⃣ For decode → upload encrypted video + enter password → Decode

✅ Decoded file auto-downloads

⚠️ Important Notes

Do not refresh page before decoding → password resets!

Store video password securely after encryption

Large videos may take longer due to encryption time

Browser may block Auto-Downloaded Encrypted video → click "Allow" or enable pop-ups

✅ Browser Compatibility
Browser	Status
Chrome	✅ Recommended
Edge	✅
Firefox	✅
Safari	⚠ Video download prompt may appear
🔒 Security

AES Encryption for Video

Messages never stored on server

Password required for decoding protected content

👨‍💻 Developer

This project is developed as part of a Cybersecurity / Steganography learning module.


✅ Future Improvements (optional)
✅ Add progress bar per-tab
✅ Support MP3 audio
✅ Improve video steganography performance
✅ Cloud deployment (Render / Railway)
