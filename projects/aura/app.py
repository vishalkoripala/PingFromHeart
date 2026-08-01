from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify
import os
import tempfile
from PIL import Image
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
ALLOWED_EXT = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'ico'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    message = request.form.get('message', 'I LOVE YOU JAANU💋')
    file = request.files.get('image')
    filename = None
    if file and allowed_file(file.filename):
        name = secure_filename(file.filename)
        dest = os.path.join(app.config['UPLOAD_FOLDER'], name)
        # ensure unique
        base, ext = os.path.splitext(name)
        i = 1
        while os.path.exists(dest):
            name = f"{base}_{i}{ext}"
            dest = os.path.join(app.config['UPLOAD_FOLDER'], name)
            i += 1
        file.save(dest)
        # resize for client convenience
        try:
            with Image.open(dest) as im:
                im.thumbnail((300, 300), Image.LANCZOS)
                im.save(dest)
        except Exception:
            pass
        filename = name
    return jsonify({'message': message, 'image': url_for('uploaded_file', filename=filename) if filename else None})


@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
