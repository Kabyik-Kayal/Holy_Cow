from flask import Flask, request, render_template, send_from_directory, flash, redirect, url_for, jsonify
import os
from werkzeug.utils import secure_filename
from config.paths import artifacts_path, uploaded_image_path
from src.generator import generate_image

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = str(artifacts_path)
app.config['SECRET_KEY'] = 'your-secret-key-here'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file selected')
        return redirect(url_for('index'))
    
    file = request.files['file']
    if file.filename == '':
        flash('No file selected')
        return redirect(url_for('index'))
    
    if file and file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
        filename = secure_filename(file.filename)
        file.save(uploaded_image_path)
        flash('File uploaded successfully!')
        return render_template('index.html', uploaded=True)
    else:
        flash('Please select a valid image file')
        return redirect(url_for('index'))

@app.route('/generate', methods=['POST'])
def generate():
    try:
        if not os.path.exists(uploaded_image_path):
            flash('Please upload an image first')
            return redirect(url_for('index'))
        
        generate_image()
        flash('Image generated successfully!')
        return render_template('index.html', uploaded=True, generated=True)
    except Exception as e:
        flash(f'Error generating image: {str(e)}')
        return render_template('index.html', uploaded=True)

@app.route('/artifacts/<filename>')
def artifacts(filename):
    return send_from_directory(artifacts_path, filename)

if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=5000)