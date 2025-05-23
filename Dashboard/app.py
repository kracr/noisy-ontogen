import os
from flask import Flask, render_template, request, redirect, url_for, jsonify, send_from_directory
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
    noise_types = ['Intersection', 'Disjoint Axiom', 'Bottom Concept', 'Role Transitivity']  # Example dropdown entries
    file_name = os.listdir(app.config['UPLOAD_FOLDER'])[0]
    return render_template('noise_page.html', noise_types=noise_types, ontology_name=file_name)

# Generate Button Handler
@app.route('/generate', methods=['POST'])
def generate():
    noise_type = request.form['noise_type']
    noise_level = request.form['noise_level']
    print(f"\nSelected Noise Type: {noise_type}, Noise Level: {noise_level}\n")  # Print to console

    file_name = os.listdir(app.config['UPLOAD_FOLDER'])[0]
    original_file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
    noisy_file_name = f'noisy_{file_name}'
    noisy_file_path = os.path.join(app.config['UPLOAD_FOLDER'], noisy_file_name)

    if (noise_type == 'Intersection'):
        # Generate noisy ontology
        noise_gen = IntersectionNoiseGenerator(original_file_path)
        n = math.floor((int(noise_level) / 100) * len(noise_gen.intersection_classes))  # Calculate the number of noise entities to introduce
        noise_gen.introduce_noise(n)
        noise_gen.save_ontology(noisy_file_path)

        # Serve the noisy file for download
        response = send_from_directory(app.config['UPLOAD_FOLDER'], noisy_file_name, as_attachment=True)

        # Delete both files after download
        os.remove(original_file_path)
        os.remove(noisy_file_path)

        return response
    
    return None

if __name__ == '__main__':
    app.run(debug=True)
