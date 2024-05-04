from langchain_community.document_transformers import Html2TextTransformer
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

def transform_document(post_title, post_content, post_id):
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
        html2text = Html2TextTransformer()
        docs_transformed = html2text.transform_documents(document)

        # Return the transformed documents
        return docs_transformed
    except Exception as e:
        return str(e)


def documents_into_chunks(docs_transformed):
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
