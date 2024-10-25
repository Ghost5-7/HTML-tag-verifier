from flask import Flask, request, jsonify, render_template_string
from html.parser import HTMLParser
import uuid
import os
import traceback
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

class FileStore:
    def __init__(self, storage_dir='uploads'):
        self.storage_dir = storage_dir
        os.makedirs(storage_dir, exist_ok=True)

    def save_file(self, content):
        file_id = str(uuid.uuid4())
        file_path = os.path.join(self.storage_dir, f"{file_id}.html")
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return file_id

    def get_file(self, file_id):
        file_path = os.path.join(self.storage_dir, f"{file_id}.html")
        
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        
        return None

class HTMLValidator(HTMLParser):
    def __init__(self, html_content):
        super().__init__()
        self.stack = []
        self.errors = []
        self.html_content = html_content
        self.lines = html_content.split('\n')

    def handle_starttag(self, tag, attrs):
        self.stack.append((tag, self.getpos()))

    def handle_endtag(self, tag):
        if not self.stack:
            line, col = self.getpos()
            self.errors.append(f"Unexpected closing tag </{tag}> at line {line}, column {col}")
            return

        last_tag, _ = self.stack.pop()
        if last_tag != tag:
            line, col = self.getpos()
            self.errors.append(f"Mismatched tags: expected </{last_tag}>, found </{tag}> at line {line}, column {col}")

    def validate(self):
        self.feed(self.html_content)
        
        for tag, (line, col) in self.stack:
            self.errors.append(f"Unclosed tag <{tag}> at line {line}, column {col}")

        return len(self.errors) == 0, self.errors

file_store = FileStore()

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HTML Tag Verifier</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        h1 {
            color: #333;
        }
        #result {
            margin-top: 20px;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
        .error {
            color: #d00;
        }
        .success {
            color: #0a0;
        }
    </style>
</head>
<body>
    <h1>HTML Tag Verifier</h1>
    <form id="upload-form" enctype="multipart/form-data">
        <input type="file" id="htmlfile" name="htmlfile" accept=".html">
        <button type="submit">Verify Tags</button>
    </form>
    <div id="result"></div>
    <script>
        document.getElementById('upload-form').addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(this);
            fetch('/verify', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                const resultDiv = document.getElementById('result');
                if (data.message) {
                    resultDiv.innerHTML = `<p class="success">${data.message}</p>`;
                } else if (data.errors) {
                    const errorList = data.errors.map(error => `<li>${error}</li>`).join('');
                    resultDiv.innerHTML = `<p class="error">HTML is invalid:</p><ul>${errorList}</ul>`;
                } else if (data.error) {
                    resultDiv.innerHTML = `<p class="error">${data.error}</p>`;
                }
            })
            .catch(error => {
                console.error('Error:', error);
                document.getElementById('result').innerHTML = '<p class="error">An error occurred while processing the request.</p>';
            });
        });
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/verify', methods=['POST'])
def verify_html():
    try:
        app.logger.debug("Received a POST request to /verify")
        if 'htmlfile' not in request.files:
            app.logger.warning("No file part in the request")
            return jsonify({'error': 'No file part'}), 400
        
        file = request.files['htmlfile']
        app.logger.debug(f"Received file: {file.filename}")
        if file.filename == '':
            app.logger.warning("No selected file")
            return jsonify({'error': 'No selected file'}), 400
        
        if file and file.filename.endswith('.html'):
            app.logger.debug("Reading file content")
            file_content = file.read().decode('utf-8')
            app.logger.debug("Saving file")
            file_id = file_store.save_file(file_content)
            
            app.logger.debug("Validating HTML")
            validator = HTMLValidator(file_content)
            is_valid, errors = validator.validate()
            
            if is_valid:
                app.logger.debug("HTML is valid")
                return jsonify({'message': 'HTML is valid!', 'file_id': file_id})
            else:
                app.logger.debug(f"HTML is invalid. Errors: {errors}")
                return jsonify({'errors': errors, 'file_id': file_id})
        
        app.logger.warning("Invalid file type")
        return jsonify({'error': 'Invalid file type'}), 400
    except Exception as e:
        app.logger.error(f"An error occurred: {str(e)}")
        app.logger.error(traceback.format_exc())
        return jsonify({'error': 'An internal server error occurred'}), 500

if __name__ == '__main__':
    app.run(debug=True)