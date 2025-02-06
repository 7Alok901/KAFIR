from flask import Flask, render_template, request, jsonify
import os
import random
import time
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')  # Render the HTML form to allow users to upload text files

@app.route('/run', methods=['POST'])
def run():
    # Get files uploaded from the form
    tokens_file = request.files['tokens']
    comments_file = request.files['comments']
    post_id = request.form['post_id']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    delay = int(request.form['delay'])
    
    # Read the tokens and comments from the uploaded files
    tokens = tokens_file.read().decode('utf-8').splitlines()
    comments = comments_file.read().decode('utf-8').splitlines()

    log_output = []

    # Iterate through each token and comment
    for token in tokens:
        for comment in comments:
            # Add first and last name to each comment
            personalized_comment = f"{first_name} {comment} {last_name}"

            # Make the POST request to Facebook API
            response = requests.post(
                f"https://graph.facebook.com/{post_id}/comments",
                data={'message': personalized_comment, 'access_token': token}
            ).json()

            if 'id' in response:
                log_output.append(f"Successfully posted comment: {personalized_comment}")
            else:
                log_output.append(f"Error posting comment: {personalized_comment}, Error: {response.get('error', {}).get('message')}")
            
            time.sleep(delay)  # Delay before posting the next comment

    return jsonify({"log": log_output})  # Return the log as a response

if __name__ == "__main__":
    app.run(debug=True)
