from flask import Flask, request, render_template, send_from_directory, flash, redirect, url_for, jsonify
import os
from werkzeug.utils import secure_filename
from config.paths import artifacts_path, uploaded_image_path
from src.generator import generate_image
from utils.logger import get_logger

logger = get_logger(__name__)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = str(artifacts_path)
app.config['SECRET_KEY'] = 'your-secret-key-here'

def cleanup_temp_images():
    """Clean up temporary uploaded and generated images"""
    try:
        # Remove uploaded image
        if os.path.exists(uploaded_image_path):
            os.remove(uploaded_image_path)
        
        # Remove generated image
        generated_image_path = artifacts_path / "generated_image.png"
        if os.path.exists(generated_image_path):
            os.remove(generated_image_path)
    except Exception as e:
        # Log the error but don't fail the request
        print(f"Warning: Could not clean up temp images: {e}")

@app.route('/')
def index():
    # Don't automatically clean up images - let the frontend handle cleanup timing
    # Only cleanup if explicitly requested via query parameter
    if request.args.get('cleanup') == 'true':
        cleanup_temp_images()
        logger.info("Cleaned up temp images on explicit request")
    
    return render_template('index.html', uploaded=False, generated=False)

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
            error_msg = 'Please upload an image first'
            if request.headers.get('Content-Type') == 'application/json' or 'application/json' in request.headers.get('Accept', ''):
                return jsonify({'success': False, 'error': error_msg, 'is_api_error': False}), 400
            flash(error_msg)
            return redirect(url_for('index'))
        
        # Get the optional API key from the form
        user_api_key = request.form.get('api_key', '').strip()
        
        # Pass the API key to the generate_image function and get the path
        generated_image_path = generate_image(user_api_key if user_api_key else None)
        
        # Log successful generation
        logger.info(f"Image generated successfully at: {generated_image_path}")
        
        # Success response
        success_msg = 'Image generated successfully!'
        if request.headers.get('Content-Type') == 'application/json' or 'application/json' in request.headers.get('Accept', ''):
            return jsonify({'success': True, 'message': success_msg})
        
        flash(success_msg)
        return render_template('index.html', uploaded=True, generated=True)
        
    except Exception as e:
        error_message = str(e)
        logger.error(f"Error in generate route: {error_message}")
        
        # Check if the request expects JSON response (for AJAX requests)
        if request.headers.get('Content-Type') == 'application/json' or 'application/json' in request.headers.get('Accept', ''):
            return jsonify({
                'success': False,
                'error': 'Oops! Try again later or use your own API key'
            }), 400
        
        # For regular form submission, flash the error
        flash('Oops! Try again later or use your own API key')
        return render_template('index.html', uploaded=True)

@app.route('/artifacts/<filename>')
def artifacts(filename):
    return send_from_directory(str(artifacts_path), filename)

@app.route('/download/<filename>')
def download_and_cleanup(filename):
    """Serve file for download without cleanup"""
    try:
        # Check if file exists
        file_path = artifacts_path / filename
        logger.info(f"Attempting to download file: {file_path}")
        logger.info(f"File exists: {os.path.exists(file_path)}")
        
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            flash('File not found')
            return redirect(url_for('index'))
        
        logger.info(f"Serving file for download: {file_path}")
        # Serve the file for download - convert Path to string for Flask
        response = send_from_directory(str(artifacts_path), filename, as_attachment=True)
        
        # Set headers to ensure proper download behavior
        response.headers['Content-Disposition'] = f'attachment; filename=holy_cow_generated.png'
        response.headers['Content-Type'] = 'image/png'
        
        return response
    except Exception as e:
        logger.error(f"Error downloading file: {str(e)}")
        flash(f'Error downloading file: {str(e)}')
        return redirect(url_for('index'))

@app.route('/cleanup', methods=['POST'])
def cleanup_images():
    """Clean up temporary images - called when page is reloaded or navigated away"""
    cleanup_temp_images()
    return jsonify({'success': True})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(debug=False, host="0.0.0.0", port=port)