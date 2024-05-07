import os
from dotenv import load_dotenv
from wordpress_chatbot.helper import read_yaml 
from wordpress_chatbot import CONFIG_FILE_PATH
#######################################################################################
#                import libraries for text preprocessing
#######################################################################################

from langchain_community.document_transformers import Html2TextTransformer
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

######################################################################################
#              Embedding functions and functions and Vector store 
######################################################################################
# Import FAISS as the vector store
from langchain_community.vectorstores import FAISS
#Embedding
from langchain_openai import OpenAIEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings



class DocumentProcessor:
    def __init__(self, embedding_name):
        load_dotenv()
        self.embedding_name = embedding_name
        self.load_embedding_model()
        config_filepath = CONFIG_FILE_PATH
        self.config = read_yaml(config_filepath)

    def transform_document(self,post_title, post_content, post_id):
        """
        Transform the given post title and content into plain text.

        Args:
            post_title (str): The title of the post.
            post_content (str): The content of the post.
            post_id (str): The ID of the post.

        Returns:
            list of str: The transformed document(s) in plain text.

        Raises:
            ValueError: If the post_title, post_content, or post_id is empty or None.
            Exception: If any other error occurs during transformation.
        """
        try:
            if not post_title or not post_content or not post_id:
                raise ValueError("post_title, post_content, and post_id cannot be empty or None")

            # Create a document with page content and metadata
            document = [Document(page_content=post_title + post_content, metadata={"title": post_title, "post id": post_id})]

            # Transform the document from HTML to plain text
            html2text = Html2TextTransformer(ignore_links=False)
            docs_transformed = html2text.transform_documents(document)

            # Return the transformed documents
            return docs_transformed
        except Exception as e:
            return str(e)

    def documents_into_chunks(self,docs_transformed):
        """
        Args:
            docs_transformed (list of str): The transformed document(s) .

        Returns:
            list of str: The split text chunks.

        Note:
            Large Language Models (LLMs) often have token limits for text inputs. 
            Therefore, input texts need to be split into smaller chunks to 
            ensure they do not exceed these token limits when processed by the LLM.
        """
        try:
            # Initialize the RecursiveCharacterTextSplitter
            text_splitter = RecursiveCharacterTextSplitter(
                separators=["\n\n", "\n", " ", ""],
                chunk_size=1000,
                chunk_overlap=200,
                length_function=len
            )
            # Text splitting
            chunks = text_splitter.split_documents(documents=docs_transformed)
            return chunks
        except Exception as e:
            # Return error message if an exception occurs
            return str(e)
        
    def load_embedding_model(self):
        """
        Load the specified embedding model using the corresponding API key.
        Args:
            embedding_name (str): The name of the embedding model to load. Supported values: "openai" or "googleai".
        Returns:
            embeddings: An instance of the loaded embedding model.
        Raises:
            ValueError: If the specified embedding is not supported or if the required environment variable is not set.
        """
        # Define environment variable names for different embeddings
        embedding_env_vars = {
            "OpenAI": "OPENAI_API_KEY",
            "GoogleAI": "GOOGLE_API_KEY"
        }

        # Check if the embedding name is valid
        if self.embedding_name not in embedding_env_vars:
            raise ValueError(f"Unsupported embedding: {self.embedding_name}")

        # Get the environment variable name for the given embedding
        env_var_name = embedding_env_vars[self.embedding_name]

        # Check if the environment variable exists
        if env_var_name not in os.environ:
            raise ValueError(f"Environment variable {env_var_name} not found")

        # Get the API key from the environment variable
        api_key = os.getenv(env_var_name)

        # Initialize vector embedding based on the embedding name
        if self.embedding_name == "OpenAI":
            embeddings = OpenAIEmbeddings(api_key=api_key)
        elif self.embedding_name == "GoogleAI":
            embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=api_key)
        else:
            raise ValueError(f"Unsupported embedding: {self.embedding_name}")

        return embeddings

    def crate_and_load_vector_store(self, embeddings, chunks):
        """
        Create and load a vector store using the provided embeddings and chunks.
        If a vector store already exists at the specified path, the new vector database will be merged with the existing one.
        Args:
            embeddings: An instance of the embeddings model.
            chunks (list): A list of text chunks to be indexed.
        Returns:
            None

        Raises:
            Exception: If there is an error in loading or merging the vector stores.
        """
        # Get the path to the vector store
        vector_path = self.config.VECTOR_STORE_DIR
        # Create a new vector database from the provided chunks and embeddings
        new_db = FAISS.from_documents(chunks, embeddings)

        try:
            # Check if a vector store already exists
            if os.path.exists(vector_path):
                # Load the existing vector store
                local_db = FAISS.load_local(vector_path, embeddings)

                # Merge the new database with the existing one
                local_db.merge_from(new_db)

                # Save the merged vector store
                local_db.save_local(vector_path)
            else:
                # Save the new vector store if no existing store is found
                new_db.save_local(vector_path)
        except Exception as e:
            # Raise an exception if there is an error in loading or merging the vector stores
            raise Exception("Error in loading or merging vector stores: " + str(e))
