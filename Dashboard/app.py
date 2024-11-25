from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

# Landing Page Route
@app.route('/')
def landing_page():
    return render_template('landing_page.html')

# Ontology Path Submission Handler
@app.route('/submit_path', methods=['POST'])
def submit_path():
    ontology_path = request.form['ontology_path']
    print(f"\nOntology Path: {ontology_path}\n")  # Print to console
    return redirect(url_for('noise_page'))

# Noise Page Route
@app.route('/noise_page')
def noise_page():
    noise_types = ['Gaussian', 'Salt & Pepper', 'Poisson', 'Speckle']  # Example dropdown entries
    return render_template('noise_page.html', noise_types=noise_types)

# Generate Button Handler
@app.route('/generate', methods=['POST'])
def generate():
    noise_type = request.form['noise_type']
    noise_level = request.form['noise_level']
    print(f"\nSelected Noise Type: {noise_type}, Noise Level: {noise_level}\n")  # Print to console
    return jsonify(success=True)

if __name__ == '__main__':
    app.run(debug=True)
