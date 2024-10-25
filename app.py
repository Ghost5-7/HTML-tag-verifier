from flask import Flask, request, render_template, jsonify
import os
import subprocess

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'htmlfile' not in request.files:
        return jsonify({'error': 'No file part'})
    file = request.files['htmlfile']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    if file:
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)
        
        # Run the C++ program
        result = subprocess.run(['./HTML_tags_verifier', filepath], capture_output=True, text=True)
        
        if result.returncode == 0:
            return jsonify({'message': 'Tags are properly balanced', 'details': result.stdout})
        else:
            return jsonify({'error': 'Tags are not balanced', 'details': result.stderr})

if __name__ == '__main__':
    app.run(debug=True)
