from flask import Flask, request, redirect, url_for
import os

uploads_html = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@uploads_html.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>HTML File Uploader</title>
    </head>
    <body>
        <h1>Upload HTML File</h1>
        <form action="/upload" method="post" enctype="multipart/form-data">
            <input type="file" name="htmlfile" accept=".html">
            <button type="submit">Upload</button>
        </form>
    </body>
    </html>
    '''

@uploads_html.route('/upload', methods=['POST'])
def upload_file():
    if 'htmlfile' not in request.files:
        return 'No file part'
    file = request.files['htmlfile']
    if file.filename == '':
        return 'No selected file'
    if file:
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)
        return f'File {file.filename} uploaded successfully!'

if __name__ == '__main__':
    uploads_html.run(debug=True)

