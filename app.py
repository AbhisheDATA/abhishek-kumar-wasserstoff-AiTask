from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import json
import os
from wordpress_chatbot.component.vectorstore import DocumentProcessor
from wordpress_chatbot.component.RAG_Chatbot import Chatbot

app = Flask(__name__)
CORS(app)

# File path for storing the data
DATA_FILE_PATH = 'webhook_data.json'

# Function to load data from the JSON file
def load_data():
    """Load data from the JSON file."""
    if os.path.exists(DATA_FILE_PATH):
        with open(DATA_FILE_PATH, 'r') as file:
            return json.load(file)
    else:
        return {}

# Function to save data to the JSON file
def save_data(data):
    """Save data to the JSON file."""
    with open(DATA_FILE_PATH, 'w') as file:
        json.dump(data, file, indent=4)  # Indent for better readability

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    """Handle incoming webhook requests."""
    # Check if the request contains JSON data
    if request.is_json:
        data = request.get_json()
        # Process the webhook payload
        post_id = data.get('post_id')
        post_title = data.get('post_title')
        post_content = data.get('post_content')
        post_url = data.get('post_url')
        print(f"Received webhook for post {post_id}: {post_title}")
        
        # Transform the document and create vector store
        document = DocumentProcessor('OpenAI')
        docs_transformed = document.transform_document(post_title, post_content, post_id)
        chunks = document.documents_into_chunks(docs_transformed)
        print(f"Number of chunks: {len(chunks)}")
        embedding = document.load_embedding_model()
        document.crate_and_load_vector_store(embedding, chunks)
        print("Vector store loaded successfully")
        
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

        # Send a response back to confirm receipt
        return jsonify({'message': 'Webhook received successfully'}), 200
    else:
        return jsonify({'error': 'Invalid JSON payload'}), 400

# Initialize chatbot and conversation QA chain
chatbot = Chatbot(llm_provider="OpenAI")
retriever = chatbot.vectorstore_retriver()
chain = chatbot.conversational_qa_chain(retriever)

@app.route("/get", methods=["GET", "POST"])
def chat():
    """Handle incoming chat messages and generate responses."""
    msg = request.form["msg"]
    input = msg
    print(input)
    response = chain.invoke({"question": input})
    print("Answer:", response["answer"])
    return str(response["answer"])

if __name__ == '__main__':
    app.run(debug=True)
