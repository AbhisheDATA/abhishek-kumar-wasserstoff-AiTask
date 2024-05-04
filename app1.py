from flask import Flask, request, jsonify
import json
import os
from langchain_core.documents import Document

app = Flask(__name__)

# File path for storing the data
DATA_FILE_PATH = 'webhook_data.json'

# Function to load data from the JSON file
def load_data():
    if os.path.exists(DATA_FILE_PATH):
        with open(DATA_FILE_PATH, 'r') as file:
            return json.load(file)
    else:
        return {}

# Function to save data to the JSON file
def save_data(data):
    with open(DATA_FILE_PATH, 'w') as file:
        json.dump(data, file, indent=4)  # Indent for better readability

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    # Check if the request contains JSON data
    if request.is_json:
        data = request.get_json()
        
        # Process the webhook payload
        post_id = data.get('post_id')
        post_title = data.get('post_title')
        post_content = data.get('post_content')
        post_url = data.get('post_url')
        document = Document(page_content=post_content, metadata={"title": post_title, "post id": post_id})
        print(document)
        # Load existing data
        existing_data = load_data()

        # Update existing data with new information
        existing_data[post_id] = {
            'post_title': post_title,
            'post_content': post_content,
            'post_url': post_url
        }

        # Save data to the JSON file
        save_data(existing_data)

        # Do something with the data (e.g., save it to a database)
        print(f"Received webhook for post {post_id}: {post_title}")

        # Send a response back to confirm receipt
        return jsonify({'message': 'Webhook received successfully'}), 200
    else:
        return jsonify({'error': 'Invalid JSON payload'}), 400

if __name__ == '__main__':
    app.run(debug=True)
