from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
from urllib.parse import quote  # Replaces url_quote
import os
import time
import random

app = Flask(__name__)

# Configure allowed file types and upload folder
ALLOWED_EXTENSIONS = {'txt'}
UPLOAD_FOLDER = './uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Function to check file extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Create the uploads folder if it does not exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Route to render the form page
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle the form submission
@app.route('/run', methods=['POST'])
def run():
    if 'tokens' not in request.files or 'comments' not in request.files:
        return jsonify({"error": "Missing files"}), 400

    tokens_file = request.files['tokens']
    comments_file = request.files['comments']
    post_id = request.form['post_id']
    delay = int(request.form['delay'])
    
    # Save files
    if tokens_file and allowed_file(tokens_file.filename):
        filename = secure_filename(tokens_file.filename)
        tokens_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    
    if comments_file and allowed_file(comments_file.filename):
        filename = secure_filename(comments_file.filename)
        comments_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    # Here you would process the files
    tokens_path = os.path.join(app.config['UPLOAD_FOLDER'], tokens_file.filename)
    comments_path = os.path.join(app.config['UPLOAD_FOLDER'], comments_file.filename)

    # Example: Load tokens and comments
    with open(tokens_path, 'r') as f:
        tokens = f.readlines()
    
    with open(comments_path, 'r') as f:
        comments = f.readlines()

    # Simulating some work: Adding delay and posting comments
    log = []
    for token in tokens:
        for comment in comments:
            # Creating comment format: first name + comment + last name
            full_comment = f"FirstName {comment.strip()} LastName"
            log.append(f"Commenting on post {post_id} with: {full_comment}")
            time.sleep(delay + random.randint(0, 5))  # Adding random delay

    return jsonify({"log": log})

if __name__ == "__main__":
    # The port environment variable is set by the cloud service like Render
    port = int(os.environ.get("PORT", 5000))  # Default to 5000 if not set
    app.run(host="0.0.0.0", port=port, debug=False)  # Run with debug=False for production
