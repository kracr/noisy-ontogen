import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
from scripts.intersection import IntersectionNoiseGenerator
import math

app = Flask(__name__)

# Configure the upload folder
UPLOAD_FOLDER = 'temp/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Landing Page Route
@app.route('/')
def landing_page():
    return render_template('landing_page.html')

# Ontology Path Submission Handler
@app.route('/submit_path', methods=['POST'])
def submit_path():
    if 'ontology_file' not in request.files:
        return "No file part in the request", 400

    file = request.files['ontology_file']
    if file.filename == '':
        return "No file selected", 400

    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)  # Save file to temp/ folder
        print(f"\nOntology Path: {filepath}\n")  # Print saved file path to console
        return redirect(url_for('noise_page'))

# Noise Page Route
@app.route('/noise_page')
def noise_page():
    noise_types = ['Gaussian', 'Salt & Pepper', 'Poisson', 'Speckle']  # Example dropdown entries
    file_name = os.listdir(app.config['UPLOAD_FOLDER'])[0]
    return render_template('noise_page.html', noise_types=noise_types, ontology_name=file_name)

# Generate Button Handler
@app.route('/generate', methods=['POST'])
def generate():
    noise_type = request.form['noise_type']
    noise_level = request.form['noise_level']
    print(f"\nSelected Noise Type: {noise_type}, Noise Level: {noise_level}\n")  # Print to console

    return jsonify(success=True)

if __name__ == '__main__':
    app.run(debug=True)
