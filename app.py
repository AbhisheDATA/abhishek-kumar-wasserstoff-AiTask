from flask import Flask, request, jsonify,render_template
import json
import os
from wordpress_chatbot.component.vectorstore import DocumentProcessor
from wordpress_chatbot.component.RAG_Chatbot import Chatbot
from wordpress_chatbot import logger

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
        print(f"Received webhook for post {post_id}: {post_title}")
        '''
        object=DocumentProcessor('GoogleAI')
        docs_transformed=object.transform_document(post_title,post_content,post_id)
        chunks=object.documents_into_chunks(docs_transformed)
        print(f"number of chunks: {len(chunks)}")
        embedding=object.load_embedding_model()
        object.crate_and_load_vector_store(embedding,chunks)
        print("vector store created")
        '''
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
    
@app.route("/")
def index():
    return render_template('chat.html')

# Initialize the Chatbot instance
chatbot = Chatbot(llm_provider="GoogleAI")

# Retrieve the vector store and create a retriever
retriever = chatbot.vectorstore_retriver()
chain=chatbot.conversational_qa_chain(retriever)
    
@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    input = msg
    print(input)
    response=chain.invoke({"question": input})
    print("answer : ", response["answer"])
    return str(response["answer"])

if __name__ == '__main__':
    app.run(debug=True)
